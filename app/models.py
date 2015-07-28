from __future__ import unicode_literals
from datetime import datetime

__author__ = 'lexxodus'

from app import db
from app.eval_arithmetics import Evaluator
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func


class Player(db.Model):
    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    custom_values = db.Column(JSONB)

    def __init__(self, custom_values=None):
        self.custom_values = custom_values

    def __repr__(self):
        return "<player: %s>" % self.id


type_assignment = db.Table(
    "type_assignment",
    db.Column('lid', db.Integer, db.ForeignKey('level.id')),
    db.Column('ltid', db.Integer, db.ForeignKey('level_type.id')),
)


class Level(db.Model):
    __tablename__ = "level"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())
    level_types = db.relationship("LevelType",
                                  secondary=type_assignment)
    custom_values = db.Column(JSONB)

    def __init__(self, name, description, level_types, custom_values=None):
        self.name = name
        self.description = description
        if level_types:
            for lt in level_types:
                self.level_types.append(lt)
        self.custom_values = custom_values

    def __repr__(self):
        return "<lvl: %s>" % self.name


class LevelType(db.Model):
    __tablename__ = "level_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())
    custom_values = db.Column(JSONB)

    def __init__(self, name, description, levels=None, custom_values=None):
        self.name = name
        self.description = description
        self.custom_values = custom_values
        if levels:
            self.assign_to_level(levels)

    def __repr__(self):
        return "<lvltype: %s>" % self.name

    def assign_to_level(self, levels):
        for l in levels:
            level = l.query.get(l)
            level.level_types.append(self)



class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())
    custom_values = db.Column(JSONB)

    def __init__(self, name, description, custom_values=None):
        self.name = name
        self.description = description
        self.custom_values = custom_values

    def __repr__(self):
        return "<task %s>" % self.name


class LevelInstance(db.Model):
    __tablename__ = "level_instance"

    id = db.Column(db.Integer, primary_key=True)
    lid = db.Column(db.Integer, db.ForeignKey("level.id"))
    start_time = db.Column(db.DateTime(timezone=False))
    end_time = db.Column(db.DateTime(timezone=False))
    custom_values = db.Column(JSONB)

    level = db.relationship("Level", foreign_keys="LevelInstance.lid")

    def __init__(self, lid, start_time, end_time=None, custom_values=None):
        self.lid = lid
        self.start_time = start_time
        self.end_time = end_time
        self.custom_values = custom_values

    def __repr__(self):
        return "<%s, level: %s>" % (self.start_time, self.level)

class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Integer, db.ForeignKey("task.id"))
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())
    score_points = db.Column(db.Integer(), nullable=False)
    score_rule = db.Column(db.String())
    score_interval = db.Column(db.Integer(), nullable=False)
    skill_points = db.Column(db.Integer(), nullable=False)
    skill_rule = db.Column(db.String())
    skill_interval = db.Column(db.Integer(), nullable=False)
    custom_values = db.Column(JSONB)

    __table_args__ = (
        db.CheckConstraint(score_interval >= 0, name='check_score_points_positive'),
    )

    task = db.relationship("Task", foreign_keys="Event.tid")

    def __init__(self, tid, name, description, skill_points, score_points,
                 skill_interval=1, score_interval=1,
                 custom_values=None):
        self.tid = tid
        self.name = name
        self.description = description
        self.skill_points = skill_points
        self.score_points = score_points
        self.skill_interval = skill_interval
        self.score_interval = score_interval
        self.custom_values = custom_values

    def __repr__(self):
        return "<event: %s>" % self.name


class Participation(db.Model):
    __tablename__ = "participation"

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("player.id"))
    liid = db.Column(db.Integer, db.ForeignKey("level_instance.id"))
    start_time = db.Column(db.DateTime(timezone=False))
    end_time = db.Column(db.DateTime(timezone=False))
    custom_values = db.Column(JSONB)

    player = db.relationship("Player", foreign_keys="Participation.pid")
    level_instance = db.relationship("LevelInstance", foreign_keys="Participation.liid")

    def __init__(self, pid, liid, start_time=None, end_time=None, custom_values=None):
        self.pid = pid
        self.liid = liid
        self.start_time = start_time
        self.end_time = end_time
        self.custom_values = custom_values

    def __repr__(self):
        return "<pid: %s, liid: %s>" % (self.pid, self.liid)


class TriggeredEvent(db.Model):
    __tablename__ = "triggered_event"

    id = db.Column(db.Integer, primary_key=True)
    paid = db.Column(db.Integer, db.ForeignKey("participation.id"))
    eid = db.Column(db.Integer, db.ForeignKey("event.id"))
    timestamp = db.Column(db.DateTime(timezone=False))
    given_skill_points = db.Column(db.Integer, nullable=False)
    given_score_points = db.Column(db.Integer, nullable=False)
    custom_values = db.Column(JSONB)

    participation = db.relationship("Participation", foreign_keys="TriggeredEvent.paid")
    event = db.relationship("Event", foreign_keys="TriggeredEvent.eid")

    def __init__(self, paid, eid, timestamp=None, custom_values=None):
        self.paid = paid
        self.eid = eid
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.now()
        self.amount = 0
        self.custom_values = custom_values
        self.calc_given_points()

    def __repr__(self):
        return "<%s, participation: %s, event: %s>" % (self.timestamp, self.paid, self.event)

    def parse_rule(self, rule):
        e = Evaluator()
        return e.safe_eval(rule, self.paid, self.eid, self.timestamp)

    def calc_given_points(self):
        event = Event.query.get(self.eid)
        self.calc_given_skill_points(event)
        self.calc_given_score_points(event)

    def calc_given_skill_points(self, event):
        rule = event.skill_rule
        base_points = event.skill_points
        interval = event.skill_interval
        if rule:
            points = self.parse_rule(rule)
        else:
            points = base_points
        gives_points = True
        if interval != 1:
            if not self.amount:
                pid = Participation.query.get(self.paid).pid
                liid = Participation.query.get(self.paid).liid
                paids = db.session.query(Participation.id). \
                    filter(Participation.liid == liid).\
                    filter(Participation.pid == pid)
                self.amount = 1 + TriggeredEvent.query.\
                    filter(TriggeredEvent.paid.in_(paids)).\
                    filter(TriggeredEvent.eid == self.eid).count()
            print(self.amount)
            gives_points = not bool(self.amount % interval)
            print(interval, gives_points)
        self.given_skill_points = points if gives_points else 0

    def calc_given_score_points(self, event):
        rule = event.score_rule
        base_points = event.score_points
        interval = event.score_interval
        if rule:
            points = self.parse_rule(rule)
        else:
            points = base_points
        gives_points = True
        if interval != 1:
            if not self.amount:
                pid = Participation.query.get(self.paid).pid
                liid = Participation.query.get(self.paid).liid
                paids = db.session.query(Participation.id). \
                    filter(Participation.liid == liid).\
                    filter(Participation.pid == pid)
                self.amount = 1 + TriggeredEvent.query.\
                    filter(TriggeredEvent.paid.in_(paids)).\
                    filter(TriggeredEvent.eid == self.eid).count()
            print(self.amount)
            gives_points = not bool(self.amount % interval)
            print(interval, points)
        self.given_score_points = points if gives_points else 0

class EventSkill(db.Model):
    __tablename__ = "event_skill"

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("player.id"))
    eid = db.Column(db.Integer, db.ForeignKey("event.id"))
    calculated_on = db.Column(db.DateTime(timezone=False))
    considered_rows = db.Column(db.Integer())
    skill_points = db.Column(db.Integer())

    player = db.relationship("Player", foreign_keys="EventSkill.pid")
    event = db.relationship("Event", foreign_keys="EventSkill.eid")

    def __init__(self, pid, eid):
        self.pid = pid
        self.eid = eid
        considered_rows, skill_points = self.calc_event_skill()
        self.calculated_on = datetime.now()
        self.considered_rows = considered_rows
        self.skill_points = skill_points

    def __repr__(self):
        return "<player: %s, event: %s, skill: %s, %s>" % (self.player, self.event, self.skill_points, self.calculated_on)

    def calc_event_skill(self):
        query = db.session.query(func.count(TriggeredEvent.id),
                                 func.sum(Event.skill_points)).\
            join(Participation).\
            filter(Participation.pid == self.pid).\
            filter(TriggeredEvent.eid == self.eid)
        return query.all()[0]


class TaskSkill(db.Model):
    __tablename__ = "task_skill"

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("player.id"))
    tid = db.Column(db.Integer, db.ForeignKey("task.id"))
    calculated_on = db.Column(db.DateTime(timezone=False))
    considered_rows = db.Column(db.Integer())
    skill_points = db.Column(db.Integer())
    custom_values = db.Column(JSONB)

    player = db.relationship("Player", foreign_keys="TaskSkill.pid")
    task = db.relationship("Task", foreign_keys="TaskSkill.tid")

    def __init__(self, pid, tid):
        self.pid = pid
        self.tid = tid
        considered_rows, skill_points = self.calc_task_skill()
        self.calculated_on = datetime.now()
        self.considered_rows = considered_rows
        self.skill_points = skill_points

    def __repr__(self):
        return "<player: %s, task: %s, skill: %s, %s>" % (self.player, self.task, self.skill_points, self.calculated_on)

    def calc_task_skill(self):
        query = db.session.query(func.count(TriggeredEvent.id),
                                 func.sum(Event.skill_points)).\
            join(Participation).\
            join(Event).\
            filter(Participation.pid == self.pid).\
            filter(Event.tid == self.tid)
        return query.all()[0]


class LevelSkill(db.Model):
    __tablename__ = "level_skill"

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("player.id"))
    lid = db.Column(db.Integer, db.ForeignKey("level.id"))
    calculated_on = db.Column(db.DateTime(timezone=False))
    considered_rows = db.Column(db.Integer())
    skill_points = db.Column(db.Integer())
    high_score = db.Column(db.Integer())
    attempt = db.Column(db.Integer())

    player = db.relationship("Player", foreign_keys="LevelSkill.pid")
    level = db.relationship("Level", foreign_keys="LevelSkill.lid")

    __table_args__ = (
        db.CheckConstraint(attempt >= 0, name='check_attempt_positive'),
    )

    def __init__(self, pid, lid):
        self.pid = pid
        self.lid = lid
        considered_rows, skill_points, score_points, attempt = self.calc_level_skill()
        self.calculated_on = datetime.now()
        self.considered_rows = considered_rows
        self.skill_points = skill_points
        self.high_score = score_points
        self.attempt = attempt

    def __repr__(self):
        return "<player: %s, level: %s, skill: %s, %s>" %\
               (self.player, self.level, self.skill_points, self.calculated_on)

    def calc_level_skill(self):
        query1 = db.session.query(
            func.count(TriggeredEvent.id),
            func.sum(Event.skill_points)).\
            join(Participation).\
            join(LevelInstance).\
            join(Event).\
            filter(Participation.pid == self.pid).\
            filter(LevelInstance.lid == self.lid)
        query2 = db.session.query(
            func.sum(TriggeredEvent.given_score_points)).\
            join(Participation).\
            join(LevelInstance).\
            filter(Participation.pid == self.pid).\
            filter(LevelInstance.lid == self.lid).\
            group_by(LevelType.id).order_by(desc("sum_1"))
        query3 = db.session.query(func.count(LevelInstance.id)). \
            join(Participation). \
            filter(Participation.pid == self.pid). \
            filter(LevelInstance.lid == self.lid)
        considered_rows, skill_points = query1.all()[0]
        score_points = query2.all()[0]
        attempt = query3.all()[0]
        return considered_rows, skill_points, score_points, attempt


class LevelTypeSkill(db.Model):
    __tablename__ = "level_type_skill"

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("player.id"))
    ltid = db.Column(db.Integer, db.ForeignKey("level_type.id"))
    calculated_on = db.Column(db.DateTime(timezone=False))
    considered_rows = db.Column(db.Integer())
    skill_points = db.Column(db.Integer())
    high_score = db.Column(db.Integer())

    player = db.relationship("Player", foreign_keys="LevelTypeSkill.pid")
    level = db.relationship("LevelType", foreign_keys="LevelTypeSkill.ltid")

    def __init__(self, pid, ltid):
        self.pid = pid
        self.ltid = ltid
        considered_rows, skill_points, score_points =\
            self.calc_level_type_skill()
        self.calculated_on = datetime.now()
        self.considered_rows = considered_rows
        self.skill_points = skill_points
        self.high_score = score_points

    def __repr__(self):
        return "<player: %s, lvltype: %s, skill: %s, %s>" % (self.player, self.level_type, self.skill_points, self.calculated_on)

    def calc_level_type_skill(self):
        query1 = db.session.query(
            func.count(TriggeredEvent.id),
            func.sum(TriggeredEvent.given_skill_points).label("sum_1")).\
            join(Participation).\
            join(LevelInstance).\
            join(Level).\
            join(Level.level_types).\
            filter(Participation.pid == self.pid).\
            filter(LevelType.id == self.ltid)
        query2 = db.session.query(
            func.sum(TriggeredEvent.given_score_points)).\
            join(Participation).\
            join(LevelInstance).\
            join(Level).\
            join(Level.level_types).\
            filter(Participation.pid == self.pid).\
            filter(LevelType.id == self.ltid).\
            group_by(LevelType.id).order_by(desc("sum_1"))
        considered_rows, skill_points = query1.all()[0]
        score_points = query2.all()[0]
        return considered_rows, skill_points, score_points