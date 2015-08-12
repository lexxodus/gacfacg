from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import app
from flask.ext import restful

api = restful.Api(app)

from app.api.event import Event
from app.api.event_skill import EventSkill
from app.api.level import Level
from app.api.level_instance import LevelInstance
from app.api.level_skill import LevelSkill
from app.api.level_type import LevelType
from app.api.level_type_skill import LevelTypeSkill
from app.api.participation import Participation
from app.api.player import Player
from app.api.task import Task
from app.api.task_skill import TaskSkill
from app.api.triggered_event import TriggeredEvent

ROOT_URL = "/api/"
api.add_resource(
    Event,
    ROOT_URL + "event/",
    ROOT_URL + "event/<int:id>",
)
api.add_resource(
    Player,
    ROOT_URL + "player/",
    ROOT_URL + "player/<int:id>",
)
api.add_resource(
    Level,
    ROOT_URL + "level/",
    ROOT_URL + "level/<int:id>",
    )
api.add_resource(
    LevelType,
    ROOT_URL + "level_type/",
    ROOT_URL + "level_type/<int:id>",
    )
api.add_resource(
    Task,
    ROOT_URL + "task/",
    ROOT_URL + "task/<int:id>",
    )
api.add_resource(
    LevelInstance,
    ROOT_URL + "level_instance/",
    ROOT_URL + "level_instance/<int:id>",
    )
api.add_resource(
    Participation,
    ROOT_URL + "participation/",
    ROOT_URL + "participation/<int:id>",
    )
api.add_resource(
    TriggeredEvent,
    ROOT_URL + "triggered_event/",
    ROOT_URL + "triggered_event/<int:id>",
    )
api.add_resource(
    LevelSkill,
    ROOT_URL + "level_skill/",
    ROOT_URL + "level_skill/<int:id>",
    )
api.add_resource(
    LevelTypeSkill,
    ROOT_URL + "level_type_skill/",
    ROOT_URL + "level_type_skill/<int:id>",
    )
api.add_resource(
    TaskSkill,
    ROOT_URL + "task_skill/",
    ROOT_URL + "task_skill/<int:id>",
    )
api.add_resource(
    EventSkill,
    ROOT_URL + "event_skill/",
    ROOT_URL + "event_skill/<int:id>",
    )
# api.add_resource(
#     EventSkill,
#     ROOT_URL + "player/<int:pid>/level/",
#     ROOT_URL + "player/<int:pid>/level/<int:lid>",
#     ROOT_URL + "player/<int:pid>/level_type/",
#     ROOT_URL + "player/<int:pid>/level_type/<int:ltid>",
#     ROOT_URL + "player/<int:pid>/task/",
#     ROOT_URL + "player/<int:pid>/task/<int:tid>",
#     ROOT_URL + "player/<int:pid>/event/",
#     ROOT_URL + "player/<int:pid>/event/<int:eid>",
#     )
