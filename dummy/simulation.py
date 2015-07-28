from __future__ import unicode_literals
__author__ = 'lexxodus'

from dummy import event_handler
from dummy.game_objects import Answer, Base, Question, Quiz, Player, Team
from dummy.word_domination import WordDomination
from random import choice, randint, random, shuffle
import string


class Simulation(object):

    ACTIONS = ["shooting", "surviving", "assisting", "quiz solving", "base capturing", "base defense"]
    INITIAL_ACTIONS = ["shoot", "base capture"]

    def __init__(self):
        quiz = self.generate_quiz()
        self.wd = WordDomination(1, quiz)

    def start_level(self):
        self.wd.start_level_instance()

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

    def calculate_et_skills(self, player):
        events = event_handler.get_events
        for a in self.ACTIONS:
            pass
        for e in events:
            pass

    def perform_actions(self, amount):
        for event in range(amount):
            player = choice(self.players)
            self.perform_initial_action(player)
            for p in self.players:
                self.calculate_et_skills(p)

    def perform_initial_action(self, player):
        if not player["player"].active:
            player["player"].active = True
            return
        action = choice(self.INITIAL_ACTIONS)
        if action == "shoot":
            self.action_shoot(player)
        if action == "base capture":
            self.capture_base(player)


    def capture_base(self, player):
        if player["strength"] == "base capturing":
            atempt_chance = 0.9
        elif player["weakness"] == "base capturing":
            atempt_chance = 0.5
        else:
            atempt_chance = 0.7
        if random() < atempt_chance:
            player_locations = {}
            for b in self.wd.level.bases:
                player_locations[b] = []
                player_locations[None] = []
            for p in self.players:
                if p["player"].active and random() < 0.6:
                    location = choice(self.wd.level.bases)
                else:
                    location = None
                p["location"] = location
                player_locations[location].append(p)
            success_rate = 0
            location = player["location"]
            supporters = []
            defense = []
            hit_attackers = []
            if location:
                for p in player_locations[location]:
                    # tries to shoot enemy player last player is removed
                    if random() < 0.2:
                        if len(player_locations[location]) > 1:
                            target, weapon = self.action_shoot(p, player_locations[location])
                            if target:
                                hit_player = target
                                player_locations[location].remove(p)
                                if hit_player["team"] is player["team"]:
                                    hit_attackers.append(hit_player)
                            continue
                    if p["team"] is player["team"]:
                        if p is not player:
                            supporters.append(p["player"])
                        if p["strength"] == "assisting":
                            capture_aid = 20
                        elif p["weakness"] == "assisting":
                            capture_aid = 5
                        else:
                            capture_aid = 10
                    else:
                        defense.append(p)
                        if p["strength"] == "base defense":
                            capture_aid = -16
                        elif p["weakness"] == "base defense":
                            capture_aid = -4
                        else:
                            capture_aid = -8
                    success_rate += capture_aid
                if success_rate > 0 and random() < 0.7:
                    # success and reward
                    defenders = [p["player"] for p in defense]
                    self.wd.player_captures_base(
                        player["player"], location, supporters, defenders)
                elif  len(defense) > 0:
                    # fail
                    attackers = list(supporters)
                    attackers.append(player["player"])
                    recapturer = None
                    defenders = []
                    for p in defense:
                        if p["team"] is not player["team"]:
                            recapture_chance = 0.0
                            if p["strength"] == "base defense":
                                recapture_chance = (1.0 / len(defense)) * 2.0
                            elif p["weakness"] == "base defense":
                                recapture_chance = (1.0 / len(defense)) / 2.0
                            if random() < recapture_chance:
                                recapturer = p["player"]
                                defense.remove(p)
                            else:
                                defenders.append(p["player"])
                    if not recapturer:
                        recapturer = choice(defense)["player"]
                    self.wd.player_defends_base(
                        recapturer, defenders, hit_attackers, location)

            # unfreeze players
            for p in self.players:
                p["player"].active = True

    def action_shoot(self, player, possible_targets=None):
        if possible_targets:
            # there are no enemy players, he will not shoot
            will_shoot = False
            for t in possible_targets:
                if player["team"] is not t["team"]:
                    will_shoot = True
                    break
            if not will_shoot:
                return None, None
        enemy_shot = False
        weapon = "3d"
        if player["strength"] == "shooting":
            # randomly missed shots
            miss_limit = 5
            genereal_hit_chance = 0.7
            enemy_hit_chance = 0.9
            weapon_chance_3d = 0.2
            # if not 3d
            weapon_chance_2d = 0.3
        elif player["weakness"] == "shooting":
            # randomly missed shots
            miss_limit = 20
            genereal_hit_chance = 0.3
            enemy_hit_chance = 0.6
            weapon_chance_3d = 0.6
            # if not 3d
            weapon_chance_2d = 0.7
        else:
            # randomly missed shots
            miss_limit = 10
            genereal_hit_chance = 0.5
            enemy_hit_chance = 0.9
            weapon_chance_3d = 0.33
            # if not 3d
            weapon_chance_2d = 0.5
        for s in range(randint(1, miss_limit)):
            player["player"].misses()
        if random() < genereal_hit_chance:
            if random() < enemy_hit_chance:
                enemy_shot = True
        else:
            return None, None
        rnd = random()
        if rnd < 1 - weapon_chance_3d:
           if rnd < weapon_chance_2d:
               weapon = "2d"
           else:
               weapon = "1d"
        friendly_team = player["team"]
        if possible_targets:
            nearby_targets = possible_targets
        else:
            nearby_targets = self.players
        real_targets = []
        if enemy_shot:
            for p in nearby_targets:
                if p["team"] is not friendly_team:
                    real_targets.append(p)
        else:
            for p in nearby_targets:
                if p["team"] is friendly_team and p is not player:
                    real_targets.append(p)
        for p in real_targets:
            if player["strength"] == "surviving":
                if random() < (1.0 / len(real_targets)) / 3:
                    target = p
                    real_targets.remove(p)
                    break
            elif player["weakness"] == "surviving":
                if random() < (1.0 / len(real_targets)) * 3:
                    target = p
                    real_targets.remove(p)
                    break
        if not "target" in locals():
            if not real_targets:
                return None, None
            target = choice(real_targets)
        self.wd.player_shoots_player(player["player"], target["player"], weapon)
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