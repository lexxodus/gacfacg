from __future__ import unicode_literals
__author__ = 'lexxodus'

from dummies.wd_balanced import event_handler
from dummies.wd_balanced.game_objects import Answer, Base, Question, Quiz, Player, Team
from dummies.wd_balanced.word_domination import WordDomination
from random import choice, randint, random, shuffle
import string


class Simulation(object):

    ACTIONS = ["shooting", "surviving", "assisting", "quiz solving", "base capturing", "base defense"]

    def __init__(self):
        quiz = self.generate_quiz()
        self.wd = WordDomination(1, quiz)
        self.events = event_handler.get_events()
        self.tasks = event_handler.get_tasks()
        self.levels = event_handler.get_levels()
        self.level_types = event_handler.get_level_types()

    def start_level(self):
        self.wd.start_level_instance()

    def end_level(self):
        self.wd.end_level_instance()

    def create_players(self, amount):
        for p in range(1, amount + 1):
            name = "Player %s" % p
            # is in clan
            if random() < 0.3:
                clan_letters = []
                for i in range(3):
                    clan_letters.append(choice(string.ascii_uppercase))
                clan ="".join(clan_letters)
            else:
                clan = None
            self.wd.create_player(name, clan)

    def load_players(self, max_amount):
        players = event_handler.get_all_players()[:max_amount]
        # assign each player to a team
        self.players = []
        # create teams
        self.create_teams()
        for i, p in enumerate(players):
            # assign player round robbin
            team = self.teams.keys()[i % len(self.teams.keys())]
            # give player a strength and weakness
            strength = self.ACTIONS[i % len(players)]
            weakness = self.ACTIONS[-(i+1) % len(players)]
            player = self.wd.load_player(p["id"])
            self.wd.add_player_to_team(player, team)
            self.players.append({
                "player": player,
                "team": team,
                "strength": strength,
                "weakness": weakness,
                "location": None,
            })
            print(player.name, strength, weakness)
            self.teams[team].append(p)

    def create_teams(self, amount=2):
        self.teams = {}
        for t in range(amount):
            team = self.wd.create_team("Team %s" % t)
            self.teams[team] = []
        return self.teams

    def generate_quiz(self):
        questions = []
        for q in range(12):
            answers = []
            has_right = False
            for a in range(4):
                if a == 3 and not has_right:
                    answers.append(Answer("Answer %s" % a, True))
                    break
                if not has_right and random() < 0.25:
                    answers.append(Answer("Answer %s" % a, True))
                    has_right = True
                else:
                    answers.append(Answer("Answer %s" % a, False))
            if q < 4:
                difficulty = "easy"
            elif q < 8:
                difficulty = "medium"
            else:
                difficulty = "hard"
            questions.append(Question("Question %s" % q, difficulty, answers))
        return Quiz(questions)

    def calculate_et_skills(self, player, until=None):
        for k, v in self.tasks.iteritems():
            event_handler.calc_task_skill(player, v, until)
        for k, v in self.events.iteritems():
            event_handler.calc_event_skill(player, v, until)

    def calculate_llt_skills(self, player, until=None):
        for k, v in self.levels.iteritems():
            event_handler.calc_level_skill(player, v, until)
        for k, v in self.level_types.iteritems():
            event_handler.calc_level_type_skill(player, v, until)

    def run_rounds(self, amount):
        for event in range(amount):
            self.perform_actions()
            if not event % 10:
                for p in event_handler.get_all_players():
                    self.calculate_et_skills(p["id"])
        for p in event_handler.get_all_players():
            self.calculate_llt_skills(p["id"])

    def perform_actions(self):
        player_locations = self.get_new_player_positions()
        wolves = [v[0]["player"] for (k, v) in player_locations.iteritems()
                  if len(v) == 1]
        shot_players = []
        for k, v in player_locations.iteritems():
            if k and v:
                shot_players += self.fight_for_location(k, v, wolves)
        for p in self.players:
            if p not in shot_players:
                p["player"].active = True

    def fight_for_location(self, location, players, lone_wolves):
        teams = {}
        team_points = {}
        available_players = list(players)
        shot_players = []
        shuffle(players)
        for p in players:
            if len(available_players) > 1 and p in available_players:
                target, weapon = self.action_shoot(p, available_players, location)
                if target:
                    available_players.remove(target)
                    shot_players.append(target)
        for p in available_players:
            if not teams.has_key(p["team"]):
                teams[p["team"]] = []
                team_points[p["team"]] = 0
            teams[p["team"]].append(p)
        for k, v in teams.iteritems():
            if location.owned_by is k:
                for p in v:
                    if p["strength"] == "base defending":
                        team_points[k] += 21
                    elif p["weakness"] == "base defending":
                        team_points[k] += 6
                    else:
                        team_points[k] += 11
            else:
                for p in v:
                    if p["strength"] == "base capturing":
                        team_points[k] += 20
                    elif p["weakness"] == "base capturing":
                        team_points[k] += 5
                    else:
                        team_points[k] += 10
        winner = None
        presence = -1
        for k, v in team_points.iteritems():
            if v > presence:
                winner = k
                presence = v
        failed_defenders = []
        for k, v in teams.iteritems():
            if k is not winner:
                failed_defenders += v
        failed_defenders = [p["player"] for p in failed_defenders]
        if location.owned_by is not winner:
            conquerer = choice(teams[winner])["player"]
            supporters = [p["player"] for p in teams[winner]
                          if p["player"] is not conquerer]
            self.wd.player_captures_base(
                conquerer, location, supporters,
                failed_defenders, lone_wolves)
        else:
            recapturer = choice(teams[winner])["player"]
            defenders = [p["player"] for p in teams[winner]
                         if p["player"] is not recapturer]
            self.wd.player_defends_base(
                recapturer, location, defenders)
        return shot_players

    def get_new_player_positions(self):
        player_locations = {}
        for b in self.wd.level.bases:
            player_locations[b] = []
            player_locations[None] = []
        assisting = []
        wandering = []
        for p in self.players:
            if p["player"].active:
                if p["strength"] == "assisting":
                    assisting.append(p)
                elif p["weakness"]  == "assisting":
                    wandering.append(p)
                else:
                    if random() < 0.75:
                        location = choice(self.wd.level.bases)
                    else:
                        location = None
                    p["location"] = location
                    player_locations[location].append(p)
        for a in assisting:
            if random() < 0.75:
                if random() < 0.75:
                    for l in player_locations:
                        if l:
                            location = l
                            break
                else:
                    location = choice(self.wd.level.bases)
            else:
                location = None
            a["location"] = location
            player_locations[location].append(a)
        for w in wandering:
            if random() < 0.75:
                location = None
            else:
                location = choice(self.wd.level.bases)
            w["location"] = location
            player_locations[location].append(w)
        for l in player_locations:
            print("l: %s, p: %s" % (l, [str(x["player"]) for x in player_locations[l]]))
        return player_locations

    def action_shoot(self, player, possible_targets, location):
        for t in possible_targets:
            if player["team"] is not t["team"]:
                will_shoot = True
                break
        enemy_shot = False
        if player["strength"] == "shooting":
            # randomly missed shots
            miss_limit = 5
            genereal_hit_chance = 0.7
            enemy_hit_chance = 0.9
            weapon_hit_chance_3d = 1.0
            weapon_hit_chance_2d = 0.9
            weapon_hit_chance_1d = 0.8
        elif player["weakness"] == "shooting":
            # randomly missed shots
            miss_limit = 20
            genereal_hit_chance = 0.3
            enemy_hit_chance = 0.6
            weapon_hit_chance_3d = 1.0
            weapon_hit_chance_2d = 0.8
            weapon_hit_chance_1d = 0.6
        else:
            # randomly missed shots
            miss_limit = 10
            genereal_hit_chance = 0.5
            enemy_hit_chance = 0.9
            weapon_hit_chance_3d = 1.0
            weapon_hit_chance_2d = 0.7
            weapon_hit_chance_1d = 0.4
        weapons = ["1d", "2d", "3d"]
        hit_skill = event_handler.get_recent_event_skill(self.events["hit"], 60)
        if hit_skill > 50:
            weapons.remove("3d")
        if hit_skill > 30:
            weapons.remove("2d")
        if hit_skill < 20:
            weapons.remove("1d")
        if hit_skill < 10:
            weapons.remove("2d")
        weapon = choice(weapons)
        teamhit_skill = event_handler.get_recent_event_skill(self.events["teamhit"], 60)
        if teamhit_skill > -30:
            player["player"].teamhit = True
        else:
            player["player"].teamhit = False
        if weapon == "3d":
            accuracy =  weapon_hit_chance_3d
        elif weapon == "2d":
            accuracy =  weapon_hit_chance_2d
        else:
            accuracy =  weapon_hit_chance_1d
        miss_limit += miss_limit * (1 - accuracy)
        for s in range(randint(1, int(miss_limit))):
            player["player"].misses()
        if random() < genereal_hit_chance * accuracy:
            if random() < enemy_hit_chance:
                enemy_shot = True
        else:
            return None, None
        friendly_team = player["team"]
        real_targets = []
        for p in possible_targets:
            if enemy_shot:
                if p["team"] is not friendly_team:
                    real_targets.append(p)
            else:
                if p["team"] is friendly_team and p is not player:
                    real_targets.append(p)
        if not real_targets:
            return None, None
        target = choice(real_targets)
        if target["strength"] == "surviving":
            dodge = 0.4
        elif target["weakness"] == "surviving":
            dodge = 0.1
        else:
            dodge = 0.2
        if random() < dodge:
            return None, None
        self.wd.player_shoots_player(player["player"], target["player"], weapon, location)
        answers = self.answer_question(target["player"].question, target)
        target["player"].give_answers(answers)
        return target, weapon

    def answer_question(self, question, player):
        given_answers = []
        right_answers = []
        wrong_answers = []
        for a in question.answers:
            if a.right:
                right_answers.append(a)
            else:
                wrong_answers.append(a)
        rnd_right = random()
        if player["strength"] == "quiz solving":
            easy_right_chance = 0.9
            medium_right_chance = 0.8
            hard_right_chance = 0.7
        elif player["weakness"] == "quiz solving":
            easy_right_chance = 0.7
            medium_right_chance = 0.5
            hard_right_chance = 0.3
        else:
            easy_right_chance = 0.8
            medium_right_chance = 0.6
            hard_right_chance = 0.4
        if question.difficulty == "easy":
            if rnd_right < easy_right_chance:
                given_answers = right_answers
            else:
                for w in wrong_answers:
                    if random < 0.4:
                        given_answers.append(w)
                if not given_answers:
                    given_answers.append(choice(wrong_answers))
                if random < easy_right_chance:
                    given_answers.append(choice(right_answers))
        elif question.difficulty == "medium":
            if rnd_right < medium_right_chance:
                given_answers = right_answers
            else:
                for w in wrong_answers:
                    if random < 0.4:
                        given_answers.append(w)
                if not given_answers:
                    given_answers.append(choice(wrong_answers))
                if random < medium_right_chance:
                    given_answers.append(choice(right_answers))
        else:
            if rnd_right < hard_right_chance:
                given_answers = right_answers
            else:
                for w in wrong_answers:
                    if random < 0.4:
                        given_answers.append(w)
                if not given_answers:
                    given_answers.append(choice(wrong_answers))
                if random < hard_right_chance:
                    given_answers.append(choice(right_answers))
        return given_answers