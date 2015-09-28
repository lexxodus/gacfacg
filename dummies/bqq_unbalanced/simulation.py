from __future__ import unicode_literals
__author__ = 'lexxodus'

from datetime import datetime, timedelta
from dummies.bqq_unbalanced import event_handler
from dummies.bqq_unbalanced.bottle_quiz_quest import BottleQuizQuest
from random import choice, randint, random

class Simulation(object):

    def __init__(self):
        self.bqq = BottleQuizQuest()
        self.load_players()

    def answer_questions(self, player):
        while(self.bqq.level.rounds_left >= 0):
            answers, end_time = self.answer_question(player)
            self.bqq.player_answers_question(answers, end_time)
            self.calculate_et_skills(player)
        self.calculate_llt_skills(player)

    def answer_question(self, player):
        question = self.bqq.level.question
        given_answers = []
        right_answers = []
        wrong_answers = []
        for a in question.answers:
            if a.right:
                right_answers.append(a)
            else:
                wrong_answers.append(a)
        if player["skill"] == "strong":
            answer_very_easy = 0.90
            answer_easy = 0.80
            answer_medium = 0.70
            answer_hard = 0.60
            answer_very_hard = 0.50
        elif player["skill"] == "average":
            answer_very_easy = 0.80
            answer_easy = 0.65
            answer_medium = 0.50
            answer_hard = 0.35
            answer_very_hard = 0.20
        elif player["skill"] == "weak":
            answer_very_easy = 0.50
            answer_easy = 0.40
            answer_medium = 0.30
            answer_hard = 0.20
            answer_very_hard = 0.10
        rnd = random()
        correct = False
        if question.difficulty == "very easy":
            if rnd < answer_very_easy:
                correct = True
        elif question.difficulty == "easy":
            if rnd < answer_easy:
                correct = True
        elif question.difficulty == "medium":
            if rnd < answer_medium:
                correct = True
        elif question.difficulty == "hard":
            if rnd < answer_hard:
                correct = True
        elif question.difficulty == "very hard":
            if rnd < answer_very_hard:
                correct = True
        if correct:
            given_answers = right_answers
        else:
            for w in wrong_answers:
                if random() < 1.0 / len(question.answers):
                    print("answer wrong: %s" % w)
                    given_answers.append(w)
            if not given_answers:
                w = choice(wrong_answers)
                print("answer wrong: %s" % w)
                given_answers.append(w)
            for r in right_answers:
                if random() < 1.0 / len(question.answers):
                    print("answer right: %s" % r)
                    given_answers.append(r)
        response_time = timedelta(seconds=randint(5, 30))
        end_time = datetime.now() + response_time
        return given_answers, end_time

    def run_quiz(self):
        for p in self.players:
            self.bqq.start_level_instance(p["id"], 1)
            self.answer_questions(p)
            self.bqq.end_level_instance()

    def load_players(self):
        players = event_handler.get_all_players()
        self.players = []
        for i, p in enumerate(players):
            # give player a strength and weakness
            if i % 3 == 0:
                skill = "strong"
            if i % 3 == 1:
                skill = "average"
            if i % 3 == 2:
                skill = "weak"
            self.players.append({
                "id": p["id"],
                "skill": skill,
            })

    def calculate_et_skills(self, player, until=None):
        events = event_handler.get_events()
        tasks = event_handler.get_tasks()
        for k, v in tasks.iteritems():
            event_handler.calc_task_skill(player["id"], v, until)
        for k, v in events.iteritems():
            event_handler.calc_event_skill(player["id"], v, until)

    def calculate_llt_skills(self, player, until=None):
        levels = event_handler.get_levels()
        level_types = event_handler.get_level_types()
        for k, v in levels.iteritems():
            event_handler.calc_level_skill(player["id"], v, until)
        for k, v in level_types.iteritems():
            event_handler.calc_level_type_skill(player["id"], v, until)
