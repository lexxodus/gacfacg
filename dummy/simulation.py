from __future__ import unicode_literals
__author__ = 'lexxodus'

from dummy.game_objects import Answer, Base, Question, Quiz, Player, Team
from dummy.word_domination import WordDomination
from random import choice, randint, random


class Simulation():

    ACTIONS = ["shooting", "surviving", "assisting", "quiz solving", "base capturing", "base defense"]
    INITIAL_ACTIONS = ["shoot", "base capture"]

    def __init__(self):
        self.teams = {}
        self.sim_players = {}
        self.bases = self.generate_bases()
        self.quiz = self.generate_quiz()
        self.wd = WordDomination(self.bases, self.quiz)
        for t in range(2):
            team_name = "Team %s" % t
            team = self.wd.add_team(team_name)
            self.teams[team] = []
            for p in range(0+t*3,3+t*3):
                player_name = "Player %s" % p
                player = self.wd.add_player_to_team(player_name, team)
                self.sim_players[player] = {
                    "weakness": "Weakness %s" % self.ACTIONS[p],
                    "team": team
                }
                self.teams[team].append(player)

    def generate_quiz(self):
        questions = []
        for q in range(12):
            answers = []
            has_right = False
            for a in range(4):
                if a == 3 and not has_right:
                    answers.append(Answer("Answer %s" % a, True))
                    break
                if not has_right and randint(0, 3) == 0:
                    answers.append(Answer("Answer %s" % a, True))
                    has_right = True
                else:
                    answers.append(Answer("Answer %s" % a, False))
            if q < 4:
                difficulty = "easy"
            if q < 8:
                difficulty = "medium"
            else:
                difficulty = "hard"
            questions.append(Question("Question %s" % q, difficulty, answers))
        return Quiz(questions)

    def generate_bases(self):
        bases = []
        for b in range(3):
            bases.append(Base(b))
        return bases


    def perform_actions(self):
        for event in range(120):
            player = choice(list(self.sim_players))
            self.perform_initial_action(self, player)

        for w in self.weaknesses:
            pass

    def perform_initial_action(self, player):
        action = choice(self.INITIAL_ACTIONS)
        if action == "shoot":
            enemy_shot = False
            hit = False
            weapon = "3d"
            if self.sim_players[player]["weakness"] == self.ACTIONS["shooting"]:
                if random() < 0.3:
                    hit = True
                    if random() < 0.6:
                        enemy_shot = True
                rnd = random()
                if rnd < 0.4:
                   if rnd < 0.3:
                       weapon = "2d"
                   else:
                       weapon = "1d"
            else:
                if random() < 0.5:
                    hit = True
                    if random() < 0.9:
                        enemy_shot = True
                weapon = "%sd" % randint(1,3)
            if hit:
                friendly_team = self.sim_players[player]["team"]
                if enemy_shot:
                    for t in self.teams():
                       if t is not friendly_team:
                           target = choice(self.team[t])
                           break
                else:
                    for t in self.teams():
                        if t is friendly_team:
                            allies = [p for p in t if p != player]
                            target = choice(self.allies)
                            break
                self.wd.player_shoots_player(player, target, weapon)
                target.question_ready.wait()
                answers = self.answer_question(target.question, target)
                target.give_answers(answers)

        if action == "base capture":
            pass


    def answer_question(self, question, player):
        given_answers = []
        right_answers = []
        wrong_answers = []
        for a in question.answers:
            if a.right:
                right_answers.append(a)
        rnd_right = random()
        rnd_wrong = random()
        if self.sim_players[player]["weakness"] == self.ACTIONS["quiz solving"]:
            if question.difficulty == "easy":
                for a in right_answers:
                    if rnd_right < 0.6:
                        given_answers.append(a)
                for a in wrong_answers:
                    if rnd_wrong < 0.4:
                        given_answers.append(a)
            elif question.difficulty == "medium":
                for a in right_answers:
                    if rnd_right < 0.4:
                        given_answers.append(a)
                for a in wrong_answers:
                    if rnd_wrong < 0.6:
                        given_answers.append(a)
            else:
                for a in right_answers:
                    if rnd_right < 0.2:
                        given_answers.append(a)
                for a in wrong_answers:
                    if rnd_wrong < 0.8:
                        given_answers.append(a)
        else:
            if question.difficulty == "easy":
                for a in right_answers:
                    if rnd_right < 0.9:
                        given_answers.append(a)
                for a in wrong_answers:
                    if rnd_wrong < 0.1:
                        given_answers.append(a)
            elif question.difficulty == "medium":
                for a in right_answers:
                    if rnd_right < 0.7:
                        given_answers.append(a)
                for a in wrong_answers:
                    if rnd_wrong < 0.3:
                        given_answers.append(a)
            else:
                for a in right_answers:
                    if rnd_right < 0.5:
                        given_answers.append(a)
                for a in wrong_answers:
                    if rnd_wrong < 0.5:
                        given_answers.append(a)
        return given_answers
