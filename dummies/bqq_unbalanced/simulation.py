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
            chance = 0.90
        elif player["skill"] == "average":
            chance = 0.75
        elif player["skill"] == "weak":
            chance = 0.60
        for r in right_answers:
            if random() < chance:
                print("answer right: %s" % r)
                given_answers.append(r)
                if chance > 0.15:
                    chance -= 0.15
        wrong_selection = wrong_answers[:]
        while len(given_answers) < len(right_answers) and wrong_selection:
            answer = choice(wrong_selection)
            print("answer wrong: %s" % answer)
            given_answers.append(answer)
            wrong_selection.remove(answer)
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
