from __future__ import unicode_literals
__author__ = 'lexxodus'

from dummy import event_handler
from dummy.game_objects import Answer, Base, Question, Quiz, Player, Team

class WordDomination(object):

    WEAPONS_TO_QUESTION_DIFFICULTY = {
        "1d": "hard",
        "2d": "medium",
        "3d": "easy"
    }

    def __init__(self, bases, quiz):
        self.teams = []
        self.bases = []
        self.bases = bases
        self.quiz = quiz

    def create_player(self, name, clan=None):
        id, api_url = event_handler.create_player(name, clan)
        return Player(id, name, clan, api_url)

    def load_player(self, id):
        player = event_handler.get_player(id)
        return Player(id, player["name"], player["clan"], player["api_url"])

    def create_team(self, team_name):
        for t in self.teams:
            if t.name == team_name:
                raise Exception("Team %s already exists!" % team_name)
        team = Team(team_name)
        self.teams.append(team)
        return team

    def add_player_to_team(self, player, team):
        for t in self.teams:
            if t.player(player):
                raise Exception("Player %s already exists!" % player.name)
        player.assign_to_team(team)
        team.add_player(player)

    def player_shoots_player(self, player, target, weapon):
        player.hit_target(target, weapon)
        target.was_hit(player, weapon)
        question = self.quiz.load_question(self.WEAPONS_TO_QUESTION_DIFFICULTY[weapon])
        target.ask_question(question)

    def player_answers_question(self, player, answers):
        player.answer_question(answers)

    def player_captures_base(self, player, base, supporters, defenders):
        player.captured(base)
        base.captured(player.team)
        for s in supporters:
            s.assisted(player, base)
        for d in defenders:
            d.failed_to_defend(base, player)

    def player_defends_base(self, player, defender, hit_attackers, base):
        player.defended(base)
        for p in defender:
            p.assisted_defender(player, base)
