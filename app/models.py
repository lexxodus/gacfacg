from __future__ import unicode_literals
from datetime import datetime

__author__ = 'lexxodus'

from app import db
from sqlalchemy.dialects.postgresql import JSONB


class Player(db.Model):
    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    custom_values = db.Column(JSONB)

    levels = db.relationship('Level', backref='player')

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

    # levels = db.relationship('Level', backref='level_instance')
    # types = db.relationship('Types', secondary=types,
    #     backref=db.backref('leveltypes', lazy='dynamic'))

    def __init__(self, name, description, custom_values):
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

    def __init__(self, name, description, custom_values):
        self.name = name
        self.description = description
        self.custom_values = custom_values

    def __repr__(self):
        return "<lvltype: %s>" % self.name


types = db.Table(
    "types",
    db.Column('lid', db.Integer, db.ForeignKey('level.id')),
    db.Column('ltid', db.Integer, db.ForeignKey('level_type.id')),
)


class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())
    custom_values = db.Column(JSONB)

    def __init__(self, name, description, custom_values):
        self.name = name
        self.description = description
        self.custom_values = custom_values

    def __repr__(self):
        return "<task %s>" % self.name


class LevelInstance(db.Model):
    __tablename__ = "level_instance"

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey("player.id"))
    lid = db.Column(db.Integer, db.ForeignKey("level.id"))
    start_time = db.Column(db.DateTime(timezone=False))
    end_time = db.Column(db.DateTime(timezone=False))
    atempt = db.Column(db.Integer())
    custom_values = db.Column(JSONB)

    player = db.relationship("Player", foreign_keys="LevelInstance.pid")
    level = db.relationship("Level", foreign_keys="LevelInstance.lid")

    __table_args__ = (
        db.CheckConstraint(atempt >= 0, name='check_atempt_positive'),
    )

    def __init__(self, pid, lid, name, description, custom_values):
        self.pid = pid
        self.lid = lid
        self.name = name
        self.description = description
        self.custom_values = custom_values

    def __repr__(self):
        return "<player: %s, level: %s, atempt: %s>" % (self.player, self.level, self.atempt)


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Integer, db.ForeignKey("task.id"))
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())
    score_points = db.Column(db.Integer(), nullable=False)
    score_point_interval = db.Column(db.Integer(), nullable=False)
    skill_points = db.Column(db.Integer(), nullable=False)
    skill_point_interval = db.Column(db.Integer(), nullable=False)
    custom_values = db.Column(JSONB)

    __table_args__ = (
        db.CheckConstraint(score_point_interval >= 0, name='check_score_points_positive'),
    )

    task = db.relationship("Task", foreign_keys="Event.tid")

    def __init__(self, tid, name, description, custom_values):
        self.tid = tid
        self.name = name
        self.description = description
        self.custom_values = custom_values

    def __repr__(self):
        return "<event: %s>" % self.name


class TriggeredEvent(db.Model):
    __tablename__ = "triggered_event"

    id = db.Column(db.Integer, primary_key=True)
    liid = db.Column(db.Integer, db.ForeignKey("level_instance.id"))
    eid = db.Column(db.Integer, db.ForeignKey("event.id"))
    timestamp = db.Column(db.DateTime(timezone=False))
    custom_values = db.Column(JSONB)

    level_instance = db.relationship("LevelInstance", foreign_keys="TriggeredEvent.liid")
    event = db.relationship("Event", foreign_keys="TriggeredEvent.eid")

    def __init__(self, liid, eid, custom_values):
        self.liid = liid
        self.eid = eid
        self.timestamp = datetime.now()
        self.custom_values = custom_values

    def __repr__(self):
        return "<%s: %s, player: %s, level: %s, event: %s>" % (self.timestamp, self.level_instance.player, self.event)


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

    player = db.relationship("Player", foreign_keys="TriggeredEvent.pid")
    event = db.relationship("Event", foreign_keys="TriggeredEvent.eid")

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

    player = db.relationship("Player", foreign_keys="TriggeredEvent.pid")
    task = db.relationship("Task", foreign_keys="TriggeredEvent.tid")

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

    player = db.relationship("Player", foreign_keys="TriggeredEvent.pid")
    level = db.relationship("Level", foreign_keys="TriggeredEvent.lid")

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
    ltid = db.Column(db.Integer, db.ForeignKey("level.id"))
    calculated_on = db.Column(db.DateTime(timezone=False))
    considered_rows = db.Column(db.Integer())
    skill_points = db.Column(db.Integer())
    high_score = db.Column(db.Integer())
    custom_values = db.Column(JSONB)

    player = db.relationship("Player", foreign_keys="TriggeredEvent.pid")
    level = db.relationship("LevelType", foreign_keys="TriggeredEvent.ltid")

    def __init__(self, pid, ltid):
        self.pid = pid
        self.lid = ltid
        self.calculated_on = datetime.now()

    def __repr__(self):
        return "<player: %s, lvltype: %s, skill: %s, %s>" % (self.player, self.level_type, self.skill_points, self.calculated_on)