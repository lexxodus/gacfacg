from __future__ import unicode_literals
__author__ = 'lexxodus'

from datetime import datetime
from random import choice
import time


class Answer(object):

    def __init__(self, answer, right):
        self.answer = answer
        self.right = right

    def __str__(self):
        return self.answer

class Base(object):

    def __init__(self, number):
        self.number = number
        self.owned_by = None

    def __str__(self):
        return self.number

class Player(object):

    def __init__(self, name, clan=None):
        self.name = name
        self.answers = None
        self.question = None
        if clan:
            self.clan = clan

    def hit_target(self, target, weapon):
        # send triggered_event
        print("%s hit %s with %s" % (self, target, weapon))

    def was_hit(self, player, weapon):
        pass
        # send triggered_event
        print("%s was hit by %s with %s" % (self, player, weapon))

    def ask_question(self, question):
        print("%s is asked %s a %s question" % (self, question, question.difficulty))
        self.question = question

    def give_answers(self, answers):
        self.answers = answers
        # evaluate answer
        for a in answers:
            if a.right:
                # send right answer
                print("%s answered %s correctly with %s" % (self, self.question, a))
            else:
                # send wrong answer
                print("%s answered %s wrong with %s" % (self, self.question, a))

    def __str__(self):
        return self.name


class Question(object):

    def __init__(self, question, difficulty, answers):
        self.question = question
        self.difficulty = difficulty
        self.answers = answers

    def __str__(self):
        return self.question


class Quiz(object):

    def __init__(self, questions):
        self.questions = questions

    def load_question(self, difficulty):
        questions = [
            q for q in self.questions if q.difficulty == difficulty
        ]
        return choice(questions)



class Team(object):

    def __init__(self, team_name):
        self.name = team_name
        self._player = []

    def add_player(self, player):
        self._player.append(player)

    def player_in_team(self, player):
        if player in self._player:
            return True
        else:
            return False

    def player_name_in_team(self, player_name):
        for p in self._player:
            if p.name == player_name:
                return True
        return False

    def __str__(self):
        return self.name
