from __future__ import unicode_literals
from datetime import datetime

__author__ = 'lexxodus'

from app import db
from sqlalchemy.dialects.postgresql import JSONB


class Player(db.Model):
    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    custom_values = db.Column(JSONB)

    def __init__(self, custom_values=None):
        self.custom_values = custom_values

    def __repr__(self):
        return "<player: %s>" % self.id


class Level(db.Model):
    __tablename__ = "level"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())
    custom_values = db.Column(JSONB)
#     level_types = db.relationship("LevelType",
#                     secondary=type_assignment)

    def __init__(self, name, description, custom_values=None):
        self.name = name
        self.description = description
        self.custom_values = custom_values

    def __repr__(self):
        return "<lvl: %s>" % self.name


class LevelType(db.Model):
    __tablename__ = "level_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())
    custom_values = db.Column(JSONB)

    def __init__(self, name, description, custom_values=None):
        self.name = name
        self.description = description
        self.custom_values = custom_values

    def __repr__(self):
        return "<lvltype: %s>" % self.name


type_assignment = db.Table(
    "type_assignment",
    db.Column('lid', db.Integer, db.ForeignKey('level.id')),
    db.Column('ltid', db.Integer, db.ForeignKey('level_type.id')),
)


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
    score_interval = db.Column(db.Integer(), nullable=False)
    skill_points = db.Column(db.Integer(), nullable=False)
    skill_interval = db.Column(db.Integer(), nullable=False)
    custom_values = db.Column(JSONB)

    __table_args__ = (
        db.CheckConstraint(score_interval >= 0, name='check_score_points_positive'),
    )

    task = db.relationship("Task", foreign_keys="Event.tid")

    def __init__(self, tid, name, description, skill_points, score_points,
                 skill_points_interval=1, score_point_interval=1,
                 custom_values=None):
        self.tid = tid
        self.name = name
        self.description = description
        self.skill_points = skill_points
        self.score_points = score_points
        self.skill_point_interval = skill_points_interval
        self.score_point_interval = score_point_interval
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
    atempt = db.Column(db.Integer())
    custom_values = db.Column(JSONB)

    player = db.relationship("Player", foreign_keys="Participation.pid")
    level_instance = db.relationship("LevelInstance", foreign_keys="Participation.liid")

    __table_args__ = (
        db.CheckConstraint(atempt >= 0, name='check_atempt_positive'),
    )

    def __init__(self, pid, liid, start_time, atempt, end_time=None, custom_values=None):
        self.pid = pid
        self.liid = liid
        self.start_time = start_time
        self.end_time = end_time
        self.atempt = atempt
        self.custom_values = custom_values

    def __repr__(self):
        return "<pid: %s, liid: %s, atempt: %s" % (self.pid, self.liid, self.atempt)


class TriggeredEvent(db.Model):
    __tablename__ = "triggered_event"

    id = db.Column(db.Integer, primary_key=True)
    paid = db.Column(db.Integer, db.ForeignKey("participation.id"))
    eid = db.Column(db.Integer, db.ForeignKey("event.id"))
    timestamp = db.Column(db.DateTime(timezone=False))
    custom_values = db.Column(JSONB)

    participation = db.relationship("Participation", foreign_keys="TriggeredEvent.paid")
    event = db.relationship("Event", foreign_keys="TriggeredEvent.eid")

    def __init__(self, paid, eid, timestamp=None, custom_values=None):
        self.paid = paid
        self.eid = eid
        self.timestamp = timestamp
        self.custom_values = custom_values

    def __repr__(self):
        return "<%s, participation: %s, event: %s>" % (self.timestamp, self.paid, self.event)


class EventSkill(db.Model):
    __tablename__ = "event_skill"

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("player.id"))
    eid = db.Column(db.Integer, db.ForeignKey("event.id"))
    calculated_on = db.Column(db.DateTime(timezone=False))
    considered_rows = db.Column(db.Integer())
    skill_points = db.Column(db.Integer())
    high_score = db.Column(db.Integer())
    custom_values = db.Column(JSONB)

    player = db.relationship("Player", foreign_keys="EventSkill.pid")
    event = db.relationship("Event", foreign_keys="EventSkill.eid")

    def __init__(self, pid, eid):
        self.pid = pid
        self.eid = eid
        self.calculated_on = datetime.now()

    def __repr__(self):
        return "<player: %s, event: %s, skill: %s, %s>" % (self.player, self.event, self.skill_points, self.calculated_on)


class TaskSkill(db.Model):
    __tablename__ = "task_skill"

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("player.id"))
    tid = db.Column(db.Integer, db.ForeignKey("task.id"))
    calculated_on = db.Column(db.DateTime(timezone=False))
    considered_rows = db.Column(db.Integer())
    skill_points = db.Column(db.Integer())
    high_score = db.Column(db.Integer())
    custom_values = db.Column(JSONB)

    player = db.relationship("Player", foreign_keys="TaskSkill.pid")
    task = db.relationship("Task", foreign_keys="TaskSkill.tid")

    def __init__(self, pid, tid):
        self.pid = pid
        self.tid = tid
        self.calculated_on = datetime.now()

    def __repr__(self):
        return "<player: %s, task: %s, skill: %s, %s>" % (self.player, self.task, self.skill_points, self.calculated_on)


class LevelSkill(db.Model):
    __tablename__ = "level_skill"

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("player.id"))
    lid = db.Column(db.Integer, db.ForeignKey("level.id"))
    calculated_on = db.Column(db.DateTime(timezone=False))
    considered_rows = db.Column(db.Integer())
    skill_points = db.Column(db.Integer())
    high_score = db.Column(db.Integer())
    custom_values = db.Column(JSONB)

    player = db.relationship("Player", foreign_keys="LevelSkill.pid")
    level = db.relationship("Level", foreign_keys="LevelSkill.lid")

    def __init__(self, pid, lid):
        self.pid = pid
        self.lid = lid
        self.calculated_on = datetime.now()

    def __repr__(self):
        return "<player: %s, level: %s, skill: %s, %s>" % (self.player, self.level, self.skill_points, self.calculated_on)


class LevelTypeSkill(db.Model):
    __tablename__ = "level_type_skill"

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("player.id"))
    ltid = db.Column(db.Integer, db.ForeignKey("level_type.id"))
    calculated_on = db.Column(db.DateTime(timezone=False))
    considered_rows = db.Column(db.Integer())
    skill_points = db.Column(db.Integer())
    high_score = db.Column(db.Integer())
    custom_values = db.Column(JSONB)

    player = db.relationship("Player", foreign_keys="LevelTypeSkill.pid")
    level = db.relationship("LevelType", foreign_keys="LevelTypeSkill.ltid")

    def __init__(self, pid, ltid):
        self.pid = pid
        self.lid = ltid
        self.calculated_on = datetime.now()

    def __repr__(self):
        return "<player: %s, lvltype: %s, skill: %s, %s>" % (self.player, self.level_type, self.skill_points, self.calculated_on)