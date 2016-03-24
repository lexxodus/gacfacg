from __future__ import unicode_literals
from app import app
from flask import make_response, render_template, send_file
from api.player import Player
from api.level import Level
from api.level_type import LevelType
from api.task import Task
from api.event import Event
from api.level_instance import LevelInstance
from api.participation import Participation
from api.triggered_event import TriggeredEvent
from api.level_skill import LevelSkill
from api.level_type_skill import LevelTypeSkill
from api.task_skill import TaskSkill
from api.event_skill import EventSkill
import json
from StringIO import StringIO
from zipfile import ZipFile
# import tablib
__author__ = 'lexxodus'


@app.route('/')
@app.route('/entities')
@app.route('/histories')
@app.route('/player-add')
@app.route('/player-edit/<int:id>')
@app.route('/player-view/<int:id>')
@app.route('/level-add')
@app.route('/level-edit/<int:id>')
@app.route('/level-view/<int:id>')
@app.route('/level_type-add')
@app.route('/level_type-edit/<int:id>')
@app.route('/level_type-view/<int:id>')
@app.route('/event-add')
@app.route('/event-edit/<int:id>')
@app.route('/event-view/<int:id>')
@app.route('/task-add')
@app.route('/task-edit/<int:id>')
@app.route('/task-view/<int:id>')
@app.route('/level_instance-view/<int:id>')
@app.route('/participation-view/<int:id>')
@app.route('/triggered_event-view/<int:id>')
@app.route('/graphs')
def angular(id=None):
    # resp = make_response(open(app.root_path + '/templates/index.html').read())
    resp = make_response(render_template('index.html'))
    resp.mimetype = 'text/html'
    return resp

@app.route('/data-export')#, methods=['GET'])
def export_data():
    print("foo")

    player_json = Player().get_all()
    level_json = Level().get_all()
    level_type_json = LevelType().get_all()
    task_json = Task().get_all()
    event_json = Event().get_all()
    level_instance_json = LevelInstance().get_all()
    participation_json = Participation().get_all()
    triggered_event_json = TriggeredEvent().get_all()
    level_skill_json = LevelSkill().get_all()
    level_type_skill_json = LevelTypeSkill().get_all()
    task_skill_json = TaskSkill().get_all()
    event_skill_json = EventSkill().get_all()

    in_memory_file = StringIO()
    zip_file = ZipFile(in_memory_file, "w")
    zip_file.writestr("player.json", json.dumps(player_json))
    zip_file.writestr("level.json", json.dumps(level_json))
    zip_file.writestr("level-type.json", json.dumps(level_type_json))
    zip_file.writestr("task.json", json.dumps(task_json))
    zip_file.writestr("event.json", json.dumps(event_json))
    zip_file.writestr("level-instance.json", json.dumps(level_instance_json))
    zip_file.writestr("participation.json", json.dumps(participation_json))
    zip_file.writestr("triggered-event.json", json.dumps(triggered_event_json))
    zip_file.writestr("level-skill.json", json.dumps(level_skill_json))
    zip_file.writestr("level-type-skill.json", json.dumps(level_type_skill_json))
    zip_file.writestr("task-skill.json", json.dumps(task_skill_json))
    zip_file.writestr("event-skill.json", json.dumps(event_skill_json))
    zip_file.close()
    in_memory_file.seek(0)
    return send_file(in_memory_file, mimetype="application/zip", attachment_filename='game-data.zip', as_attachment=True)