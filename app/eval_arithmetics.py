from __future__ import unicode_literals
__author__ = 'lexxodus'
# adoption of
# http://stackoverflow.com/questions/26505420/evaluate-math-equations-from-unsafe-user-input-in-python
# by http://stackoverflow.com/users/680727/aleksi-torhamo

from app import db
# from app.models import Event, Player, Level, LevelInstance, LevelType, \
#    Participation, Task, TriggeredEvent
import ast
from datetime import datetime
from dateutil import parser
import operator

_operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.div,
    ast.Pow: operator.pow,
}

class Evaluator(object):

    def __init__(self):
        self.calc_timedelta = False
        self.paid = 0
        self.eid = 0
        self.timestamp = None
        self.custom_values = None

    def _safe_eval(self, node):
        if isinstance(node, ast.Num):
            print(node.n)
            return node.n
        elif isinstance(node, ast.Name):
            print(node.id)
            return self._get_variables(node.id)
        elif isinstance(node, ast.BinOp):
            op = _operations[node.op.__class__] # KeyError -> Unsafe operation
            left = self._safe_eval(node.left)
            print(left)
            right = self._safe_eval(node.right)
            if self.calc_timedelta:
                assert op is operator.sub
                self.calc_timedelta = False
                return op(left, right).total_seconds()
            print(right)
            if isinstance(node.op, ast.Pow):
                assert right < 100
            return op(left, right)
        else:
            assert False, 'Unsafe operation'

    def _try_datetime(self, value):
        try:
            value = parser.parse(value)
        except ValueError:
            assert not self.calc_timedelta
        else:
            self.calc_timedelta = True
        return value

    def _get_variables(self, expr):
        parts = expr.split("__")
        if len(parts) != 2:
            raise Exception
        # only custom_values can apply
        if parts[0] == "player":
            player = Player.query.join(Participation).\
                filter(Participation.id == self.paid)[0]
            custom_value = self._try_datetime(player.custom_values[parts[1]])
            return custom_value
        elif parts[0] == "level":
            level = Level.query.join(LevelInstance, Participation).\
                filter(Participation.id == self.paid)[0]
            custom_value = self._try_datetime(level.custom_values[parts[1]])
            return custom_value
        elif parts[0] == "level_type":
            level_type = LevelType.query.join(
                Level, Level.level_types, LevelInstance, Participation).\
                filter(Participation.id == self.paid)[0]
            custom_value = self._try_datetime(
                level_type.custom_values[parts[1]])
            return custom_value
        elif parts[0] == "task":
            task = Task.query.join(Event).\
                filter(Event.id == self.eid)[0]
            custom_value = self._try_datetime(task.custom_values[parts[1]])
            return custom_value
        elif parts[0] == "level_instance":
            level_instance = LevelInstance.query.join(Participation).\
                filter(Participation.id == self.paid)[0]
            if parts[1] == "start_time":
                self.calc_timedelta = True
                return level_instance.start_time
            elif parts[1] == "end_time":
                self.calc_timedelta = True
                return level_instance.end_time
            else:
                custom_value = self._try_datetime(
                    level_instance.custom_values[parts[1]])
                return custom_value
        elif parts[0] == "event":
            event = Event.query.get(self.eid)
            print(event.name)
            if not self.calc_timedelta:
                if parts[1] == "skill_points":
                    return event.skill_points
                elif parts[1] == "score_points":
                    return event.score_points
            else:
                custom_value = self._try_datetime(
                    event.custom_values[parts[1]])
                return custom_value
        elif parts[0] == "participation":
            participation = Participation.query.get(Participation.id == self.paid)
            if parts[1] == "start_time":
                self.calc_timedelta = True
                return participation.start_time
            elif parts[1] == "end_time":
                self.calc_timedelta = True
                return participation.end_time
            else:
                custom_value = self._try_datetime(
                    participation.custom_values[parts[1]])
                return custom_value
        elif parts[0] == "triggered_event":
            if parts[1] == "timestamp":
                self.calc_timedelta = True
                return self.timestamp
            else:
                custom_value = self._try_datetime(
                    self.custom_values[parts[1]])
                return custom_value
        else:
            assert False, "Unknown Value: %s" % expr

    def safe_eval(self, expr, paid, eid, timestamp, custom_values=None):
        self.timestamp = timestamp
        self.custom_values = custom_values
        self.calc_timedelta = False
        self.paid = paid
        self.eid = eid
        node = ast.parse(expr, '<string>', 'eval').body
        return self._safe_eval(node)
