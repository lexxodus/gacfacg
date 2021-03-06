from __future__ import unicode_literals
__author__ = 'lexxodus'
# adaptation of
# http://stackoverflow.com/questions/26505420/evaluate-math-equations-from-unsafe-user-input-in-python
# by http://stackoverflow.com/users/680727/aleksi-torhamo

from app import db
import models
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
            return node.n
        elif isinstance(node, ast.Name):
            return self._get_variables(node.id)
        elif isinstance(node, ast.BinOp):
            op = _operations[node.op.__class__] # KeyError -> Unsafe operation
            left = self._safe_eval(node.left)
            right = self._safe_eval(node.right)
            if self.calc_timedelta:
                assert op is operator.sub
                self.calc_timedelta = False
                return op(left, right).total_seconds()
            if isinstance(node.op, ast.Pow):
                assert right < 100
            return op(left, right)
        else:
            assert False, 'Unsafe operation'

    def _try_datetime(self, value):
        try:
            value = parser.parse(value)
        except AttributeError:
            assert not self.calc_timedelta
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
            player = models.Player.query.join(models.Participation).\
                filter(models.Participation.id == self.paid).first()
            custom_value = self._try_datetime(player.custom_values[parts[1]])
            return float(custom_value)
        elif parts[0] == "level":
            level = models.Level.query.join(models.LevelInstance, models.Participation).\
                filter(models.Participation.id == self.paid).first()
            custom_value = self._try_datetime(level.custom_values[parts[1]])
            return float(custom_value)
        elif parts[0] == "level_type":
            level_type = models.LevelType.query.join(
                models.Level, models.Level.level_types, models.LevelInstance, models.Participation).\
                filter(models.Participation.id == self.paid).first()
            custom_value = self._try_datetime(
                level_type.custom_values[parts[1]])
            return float(custom_value)
        elif parts[0] == "task":
            task = models.Task.query.join(models.Event).\
                filter(models.Event.id == self.eid).first()
            custom_value = self._try_datetime(task.custom_values[parts[1]])
            return float(custom_value)
        elif parts[0] == "level_instance":
            level_instance = models.LevelInstance.query.join(models.Participation).\
                filter(models.Participation.id == self.paid).first()
            if parts[1] == "start_time":
                self.calc_timedelta = True
                return level_instance.start_time
            elif parts[1] == "end_time":
                self.calc_timedelta = True
                return level_instance.end_time
            else:
                custom_value = self._try_datetime(
                    level_instance.custom_values[parts[1]])
                return float(custom_value)
        elif parts[0] == "event":
            event = models.Event.query.get(self.eid)
            if not self.calc_timedelta:
                if parts[1] == "skill_points":
                    return event.skill_points
                if parts[1] == "skill_interval":
                    return event.skill_interval
                elif parts[1] == "score_points":
                    return event.score_points
                elif parts[1] == "score_interval":
                    return event.score_interval
            else:
                custom_value = self._try_datetime(
                    event.custom_values[parts[1]])
                return float(custom_value)
        elif parts[0] == "participation":
            participation = models.Participation.query.get(models.Participation.id == self.paid)
            if parts[1] == "start_time":
                self.calc_timedelta = True
                return participation.start_time
            elif parts[1] == "end_time":
                self.calc_timedelta = True
                return participation.end_time
            else:
                custom_value = self._try_datetime(
                    participation.custom_values[parts[1]])
                return float(custom_value)
        elif parts[0] == "triggered_event":
            if parts[1] == "timestamp":
                self.calc_timedelta = True
                return self.timestamp
            else:
                custom_value = self._try_datetime(
                    self.custom_values[parts[1]])
                return float(custom_value)
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
