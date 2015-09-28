from __future__ import unicode_literals
__author__ = 'lexxodus'

from datetime import datetime
from dummies.bqq_unbalanced.event_handler import get_events, trigger_event
from random import choice


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

class Level(GameObjects):

    def __init__(self, id, pictures_right, pictures_wrong, spots, difficulty=None, rounds=10):
        super(Level, self).__init__()
        self.id = id
        self.liid = None
        self.pictures = {
            "right": pictures_right.strip().split(","),
            "wrong": pictures_wrong.strip().split(","),
        }
        self.spots = int(spots)
        self.question = None
        self.rounds_left = rounds
        self.generate_question(difficulty)

    def generate_question(self, difficulty=None):
        answers = []
        if not difficulty:
            difficulty = choice(["very easy", "easy", "medium", "hard", "very hard"])
        if difficulty == "very easy":
            question = "Find the refreshment with 0 per cent alc!"
            answers = self.generate_answers(1);
        elif difficulty == "easy":
            question = "Find the two refreshments with 0 per cent alc!"
            answers = self.generate_answers(2);
        if difficulty == "medium":
            question = "Find the three refreshments with 0 per cent alc!"
            answers = self.generate_answers(3);
        elif difficulty == "hard":
            question = "Find the four refreshments with 0 per cent alc!"
            answers = self.generate_answers(4);
        elif difficulty == "very hard":
            question = "Find the five refreshments with 0 per cent alc!"
            answers = self.generate_answers(5);
        self.question = Question(question, difficulty, answers)
        self.rounds_left -= 1

    def generate_answers(self, right):
        used_pictures = []
        answers = []
        while len(answers) < right:
            picture = choice(self.pictures["right"])
            if picture not in used_pictures:
                used_pictures.append(picture)
                answers.append(Answer(picture, True))
        while len(answers) < self.spots:
            picture = choice(self.pictures["wrong"])
            if picture not in used_pictures:
                used_pictures.append(picture)
                answers.append(Answer(picture, False))
        return answers


class Player(GameObjects):

    def __init__(self, id, name):
        super(Player, self).__init__()
        self.id = id
        self.name = name
        self.answers = None
        self.question = None
        self.cnt_wright_answers = 0
        self.cnt_wrong_answers = 0
        self.paid = None

    def ask_question(self, question):
        print("%s is asked %s a %s question" %
              (self, question, question.difficulty))
        self.question = question
        self.question_starttime = datetime.now()

    def give_answers(self, answers, endtime=None):
        if not endtime:
            endtime = datetime.now()
        response_time = endtime - self.question_starttime
        self.answers = answers
        # evaluate answer
        right_answers = []
        wrong_answers = []
        for a in answers:
            if a.right:
                right_answers.append(a)
                print("%s answered %s correctly with %s" % (self, self.question, a))
            else:
                wrong_answers.append(a)
                print("%s answered %s wrong with %s" % (self, self.question, a))
        answer_options = [str(a) for a in self.question.answers]
        trigger_event(self.paid, self.events["answer given"],
                      question=str(self.question),
                      right_answers=[str(a) for a in right_answers],
                      right_answers_amount=len(right_answers),
                      wrong_answers=[str(a) for a in wrong_answers],
                      wrong_answers_amount=len(wrong_answers),
                      answer_options=answer_options,
                      difficulty=self.question.difficulty,
                      response_time=response_time.seconds
        )

    def __str__(self):
        return "%s" % self.name


class Question(GameObjects):

    def __init__(self, question, difficulty, answers):
        super(Question, self).__init__()
        self.question = question
        self.difficulty = difficulty
        self.answers = answers

    def __str__(self):
        return self.question
