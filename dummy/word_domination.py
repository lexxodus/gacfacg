from __future__ import unicode_literals
__author__ = 'lexxodus'

from dummy.game_objects import Answer, Base, Question, Quiz, Player, Team
import threading
from random import choice, randint


class WordDomination():

    WEAPONS_TO_QUESTION_DIFFICULTY = {
        "1d": "hard",
        "2d": "medium",
        "3d": "easy"
    }

    def __init__(self, base_amount, quiz):
        self.teams = []
        self.base = Base(base_amount)
        self.quiz = quiz

    def create_team(self, team_name):
        for t in self.teams:
            if t.name == team_name:
                raise Exception("Team %s already exists!" % team_name)
        team = Team(team_name)
        self.teams.append(team)
        return team

    def add_player_to_team(self, player_name, team):
        for t in self.teams:
            if t.player_name_in_team(player_name):
                raise Exception("Player %s already exists!" % player_name)
        player = Player(player_name)
        team.add_player(player)
        return player

    def player_shoots_player(self, player, target, weapon):
        player.hit_target(target, weapon)
        target.was_hit(player, weapon)
        question = self.quiz.load_question(self.WEAPONS_TO_QUESTION_DIFFICULTY[weapon])
        question_ready = threading.Event()
        answers_ready = threading.Event()
        quiz = threading.Thread(target=target.ask_question, args=(question, question_ready, answers_ready,))
        quiz.start()

    def player_answers_question(self, player, answers):
        player.answer_question(answers)
