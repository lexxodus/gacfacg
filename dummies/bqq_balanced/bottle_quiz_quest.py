from __future__ import unicode_literals

__author__ = 'lexxodus'

from dummies.bqq_balanced import event_handler
from dummies.bqq_balanced.game_objects import Answer, Level, Question, Player
from random import choice


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
        level_skill = event_handler.get_recent_level_skill(
            self.player.id, lid, last=2)
        if level_skill < -40:
            difficulty = "very easy"
        elif level_skill < -20:
            difficulty = "easy"
        elif level_skill < 20:
            difficulty = "medium"
        elif level_skill < 40:
            difficulty = "hard"
        else:
            difficulty = "very hard"
        level = Level(
            lid,
            data["pictures right"],
            data["pictures wrong"],
            int(data["spots"]),
            difficulty)
        return level

    def player_answers_question(self, answers, endtime=None):
        self.player.give_answers(answers, endtime)
        if self.level.rounds_left >= 0:
            self.player.ask_question(self.level.question)
            event_skill = event_handler.get_recent_event_skill(
                self.player.id, self.level.id, last=3)
            if event_skill:
                print(event_skill)
                if event_skill < -20:
                    difficulties = ["very easy"]
                elif event_skill < -10:
                    difficulties = ["very easy", "easy", "medium"]
                elif event_skill < 5:
                    difficulties = ["very easy", "easy", "medium", "hard", "very hard"]
                elif event_skill < 8:
                    difficulties = ["medium", "hard", "very hard"]
                else:
                    difficulties = ["very hard"]
                difficulty = choice(difficulties)
            else:
                difficulty = None
            self.level.generate_question(difficulty)
