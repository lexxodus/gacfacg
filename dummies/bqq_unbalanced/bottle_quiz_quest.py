from __future__ import unicode_literals
__author__ = 'lexxodus'

from dummies.bqq_unbalanced import event_handler
from dummies.bqq_unbalanced.game_objects import Answer, Level, Question, Player

class BottleQuizQuest(object):

    def start_level_instance(self, player_id, level_id):
        self.player = self.load_player(player_id)
        self.level = self.load_level(level_id)
        self.level.liid = event_handler.create_level_instance(level_id)
        data = event_handler.login_player_into_level_instance(
            player_id, self.level.liid)
        self.player.paid = data["id"]
        if self.level.rounds_left >= 0:
            self.player.ask_question(self.level.question)

    def end_level_instance(self):
        event_handler.end_level_instance(self.level.liid, self.player)

    def load_player(self, pid):
        data = event_handler.get_player(pid)
        player = Player(pid, data["name"])
        return player

    def load_level(self, lid):
        data = event_handler.get_level(lid)
        level = Level(lid, data["pictures right"], data["pictures wrong"], int(data["spots"]))
        return level

    def player_answers_question(self, answers, endtime=None):
        self.player.give_answers(answers, endtime)
        if self.level.rounds_left >= 0:
            self.player.ask_question(self.level.question)
            self.level.generate_question()
