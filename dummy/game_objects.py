from __future__ import unicode_literals
__author__ = 'lexxodus'

from datetime import datetime
from event_handler import get_events, trigger_event
from random import choice
import time


class GameObjects(object):

    def __init__(self):
        self.events = get_events()

class Answer(GameObjects):

    def __init__(self, answer, right):
        super(Answer, self).__init__()
        self.answer = answer
        self.right = right

    def __str__(self):
        return self.answer


class Base(GameObjects):

    def __init__(self, number):
        super(Base, self).__init__()
        self.number = number
        self.owned_by = None

    def __str__(self):
        return "Base %s" % self.number

    def captured(self, team):
        self.owned_by = team
        print("%s was captured by %s" % (self, team))


class Level(GameObjects):

    def __init__(self, id, vision, terrain, base_amount):
        super(Level, self).__init__()
        self.id = id
        self.lid = None
        self.vision = vision
        self.terrain = terrain
        self.bases = self.generate_bases(base_amount)

    def generate_bases(self, amount):
        bases = []
        for b in range(1, amount):
            bases.append(Base(b))
        return bases


class Player(GameObjects):

    def __init__(self, id, name, clan=None):
        super(Player, self).__init__()
        self.id = id
        self.name = name
        self.answers = None
        self.question = None
        self.team = None
        self.active = True
        self.participation = None
        if clan:
            self.clan = clan

    def assign_to_team(self, team):
        self.team = team

    def player_in_team(self, team):
        return team

    def hit_target(self, target, weapon, base=None):
        # send triggered_event
        if self.team is not target.team:
            trigger_event(self.participation, self.events["hit"],
                          target=target.id, weapon=weapon)
            print("%s hit %s with %s" % (self, target, weapon))
        else:
            trigger_event(self.participation, self.events["teamhit"],
                          target=target.id, weapon=weapon)
            print("%s teamhit %s with %s" % (self, target, weapon))

    def misses(self):
        trigger_event(self.participation, self.events["neverhit"])
        print("%s misses" % self)

    def captured(self, base):
        trigger_event(self.participation, self.events["base captured"],
                      base=str(base))
        print("%s captured %s" % (self, base))

    def assisted(self, player, base):
        trigger_event(self.participation, self.events["base assist"],
                      base=str(base), player=player.id)
        print("%s assisted %s capturing %s" % (self, player, base))

    def failed_to_defend(self, base, player):
        trigger_event(self.participation, self.events["weak defender"],
                      base=str(base), player=player.id)
        print("%s failed to defend %s against %s" % (self, base, player))

    def defended(self, base):
        trigger_event(self.participation, self.events["base defended"],
                      base=str(base))
        print("%s defended %s" % (self, base))

    def assisted_defender(self, defender, base):
        print("%s assisted %s defending %s" % (self, defender, base))

    def was_hit(self, player, weapon, base=None):
        # send triggered_event
        if base:
            trigger_event(self.participation, self.events["hit in action"],
                          player=player.id, weapon=weapon, base=str(base))
            print("%s was hit by %s with %s while defending %s" %
                  (self, player, weapon, base))
        else:
            trigger_event(self.participation, self.events["teamhit"],
                          player=player.id, weapon=weapon)
            print("%s was hit by %s with %s" % (self, player, weapon))

    def ask_question(self, question):
        print("%s is asked %s a %s question" %
              (self, question, question.difficulty))
        self.question = question

    def give_answers(self, answers):
        self.answers = answers
        # evaluate answer
        answered_correctly = True
        for a in answers:
            if a.right:
                # send right answer
                print("%s answered %s correctly with %s" % (self, self.question, a))
            else:
                self.active = False
                answered_correctly = False
                # send wrong answer
                print("%s answered %s wrong with %s" % (self, self.question, a))
        answers_str = [str(a) for a in answers]
        answer_options = [str(a) for a in self.question.answers]
        correct_answers = [str(a) for a in self.question.answers if a.right]
        if answered_correctly:
            trigger_event(self.participation, self.events["correct answer"],
                          given_answers=answers_str, question=str(self.question),
                          answer_options=answer_options,
                          difficulty=self.question.difficulty,
                          correct_answers=correct_answers)
        else:
            trigger_event(self.participation, self.events["wrong answer"],
                          given_answers=answers_str, question=str(self.question),
                          answer_options=answer_options,
                          difficulty=self.question.difficulty,
                          correct_answers=correct_answers)
        return answered_correctly

    def __str__(self):
        return self.name


class Question(GameObjects):

    def __init__(self, question, difficulty, answers):
        super(Question, self).__init__()
        self.question = question
        self.difficulty = difficulty
        self.answers = answers

    def __str__(self):
        return self.question


class Quiz(GameObjects):

    def __init__(self, questions):
        super(Quiz, self).__init__()
        self.questions = questions

    def load_question(self, difficulty):
        questions = [
            q for q in self.questions if q.difficulty == difficulty
        ]
        return choice(questions)

class Team(GameObjects):

    def __init__(self, team_name):
        super(Team, self).__init__()
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

    def get_players(self):
        return self._player[:]

    def __str__(self):
        return self.name
