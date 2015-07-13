from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import app, db
from app.models import Player, Level, LevelInstance, LevelType, Task,\
    Event
from datetime import datetime
from flask import abort, jsonify, request, url_for

@app.route('/')
def hello_world():
    return 'Hello World!'

def get_player_json(player, public=True):
    data = {}
    data["id"] = player.id
    if public:
        data['api_url'] = url_for('get_player', id=data['id'], _external=True)
    for k, v in player.custom_values.iteritems():
        data[k] = v
    return data

@app.route('/worddomination1/api/player/', methods=['POST'])
def create_player():
    data = request.get_json()
    custom_values = {}
    for k, v in data.iteritems():
        custom_values[k] = v
    player = Player(custom_values=custom_values)
    db.session.add(player)
    db.session.commit()
    return jsonify(get_player_json(player)), 201

@app.route('/worddomination1/api/player/', methods=['GET'])
def get_all_players():
    players = Player.query.order_by(Player.id).all()
    if not players:
        abort(404)
    data = []
    for p in players:
        data.append(get_player_json(p))
    return jsonify({"data":data})

@app.route('/worddomination1/api/player/<int:id>', methods=['GET'])
def get_player(id):
    player = Player.query.get(id)
    if not player:
        abort(404)
    return jsonify(get_player_json(player))

@app.route('/worddomination1/api/player/<int:id>', methods=['PUT'])
def update_player(id):
    player = Player.query.get(id)
    if not player:
        abort(404)
    data = request.get_json()
    custom_values = {}
    for k, v in data.iteritems():
        custom_values[k] = v
    player.custom_values = custom_values
    db.session.commit()
    return jsonify(get_player_json(player))

@app.route('/worddomination1/api/player/<int:id>', methods=['DELETE'])
def delete_player(id):
    player = Player.query.get(id)
    if not player:
        abort(404)
    db.session.delete(player)
    db.session.commit()
    return "",

def get_level_json(level, public=True):
    data = {}
    data["id"] = level.id
    data["name"] = level.name
    data["description"] = level.description
    if public:
        data['api_url'] = url_for('get_level', id=data['id'], _external=True)
    for k, v in level.custom_values.iteritems():
        data[k] = v
    return data

@app.route('/worddomination1/api/level/', methods=['POST'])
def create_level():
    expected_values = ["name", "description"]
    data = request.get_json()
    name = data["name"]
    description = data["description"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    level = Level(name, description, custom_values=custom_values)
    db.session.add(level)
    db.session.commit()
    return jsonify(get_level_json(level)), 201

@app.route('/worddomination1/api/level/', methods=['GET'])
def get_all_levels():
    levels = Level.query.order_by(Level.id).all()
    if not levels:
        abort(404)
    data = []
    for l in levels:
        data.append(get_level_json(l))
    return jsonify({"data":data})

@app.route('/worddomination1/api/level/<int:id>', methods=['GET'])
def get_level(id):
    level = Level.query.get(id)
    if not level:
        abort(404)
    return jsonify(get_level_json(level))

@app.route('/worddomination1/api/level/<int:id>', methods=['PUT'])
def update_level(id):
    expected_values = ["name", "description"]
    level = Level.query.get(id)
    if not level:
        abort(404)
    data = request.get_json()
    level.name = data["name"]
    level.description = data["description"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    level.custom_values = custom_values
    db.session.commit()
    return jsonify(get_level_json(level))

@app.route('/worddomination1/api/level/<int:id>', methods=['DELETE'])
def delete_level(id):
    level = Level.query.get(id)
    if not level:
        abort(404)
    db.session.delete(level)
    db.session.commit()
    return "", 204

def get_level_type_json(level_type, public=True):
    data = {}
    data["id"] = level_type.id
    data["name"] = level_type.name
    data["description"] = level_type.description
    if public:
        data['api_url'] = url_for('get_level_type', id=data['id'], _external=True)
    for k, v in level_type.custom_values.iteritems():
        data[k] = v
    return data

@app.route('/worddomination1/api/level_type/', methods=['POST'])
def create_level_type():
    expected_values = ["name", "description"]
    data = request.get_json()
    name = data["name"]
    description = data["description"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    level_type = LevelType(name, description, custom_values=custom_values)
    db.session.add(level_type)
    db.session.commit()
    return jsonify(get_level_type_json(level_type)), 201

@app.route('/worddomination1/api/level_type/', methods=['GET'])
def get_all_level_types():
    level_types = LevelType.query.order_by(LevelType.id).all()
    if not level_types:
        abort(404)
    data = []
    for lt in level_types:
        data.append(get_level_type_json(lt))
    return jsonify({"data":data})

@app.route('/worddomination1/api/level_type/<int:id>', methods=['GET'])
def get_level_type(id):
    level_type = LevelType.query.get(id)
    if not level_type:
        abort(404)
    return jsonify(get_level_type_json(level_type))

@app.route('/worddomination1/api/level_type/<int:id>', methods=['PUT'])
def update_level_type(id):
    expected_values = ["name", "description"]
    level_type = LevelType.query.get(id)
    if not level_type:
        abort(404)
    data = request.get_json()
    level_type.name = data["name"]
    level_type.description = data["description"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    level_type.custom_values = custom_values
    db.session.commit()
    return jsonify(get_level_type_json(level_type))

@app.route('/worddomination1/api/level_type/<int:id>', methods=['DELETE'])
def delete_level_type(id):
    level_type = LevelType.query.get(id)
    if not level_type:
        abort(404)
    db.session.delete(level_type)
    db.session.commit()
    return "", 204

# @app.route('/worddomination1/api/type_assignment/', methods=['POST'])
# def create_task():
#     data = request.get_json()
#     name = data["name"]
#     description = data["description"]
#     type_assignment = TypeAssignment(name, description, custom_values=custom_values)
#     db.session.add(task)
#     db.session.commit()
#     return jsonify(get_task_json(task)), 201

def get_task_json(task, public=True):
    data = {}
    data["id"] = task.id
    data["name"] = task.name
    data["description"] = task.description
    if public:
        data['api_url'] = url_for('get_task', id=data['id'], _external=True)
    for k, v in task.custom_values.iteritems():
        data[k] = v
    return data

@app.route('/worddomination1/api/task/', methods=['POST'])
def create_task():
    expected_values = ["name", "description"]
    data = request.get_json()
    name = data["name"]
    description = data["description"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    task = Task(name, description, custom_values=custom_values)
    db.session.add(task)
    db.session.commit()
    return jsonify(get_task_json(task)), 201

@app.route('/worddomination1/api/task/', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.order_by(Task.id).all()
    if not tasks:
        abort(404)
    data = []
    for t in tasks:
        data.append(get_task_json(t))
    return jsonify({"data":data})

@app.route('/worddomination1/api/task/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if not task:
        abort(404)
    return jsonify(get_task_json(task))

@app.route('/worddomination1/api/task/<int:id>', methods=['PUT'])
def update_task(id):
    expected_values = ["name", "description"]
    task = Task.query.get(id)
    if not task:
        abort(404)
    data = request.get_json()
    task.name = data["name"]
    task.description = data["description"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    task.custom_values = custom_values
    db.session.commit()
    return jsonify(get_task_json(task))

@app.route('/worddomination1/api/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        abort(404)
    db.session.delete(task)
    db.session.commit()
    return "", 204

def get_event_json(event, public=True):
    data = {}
    data["id"] = event.id
    data["tid"] = event.tid
    data["name"] = event.name
    data["description"] = event.description
    data["skill_points"] = event.skill_points
    data["score_points"] = event.score_points
    data["skill_interval"] = event.skill_interval
    data["score_interval"] = event.score_interval
    if public:
        data['api_url'] = url_for('get_event', id=data['id'], _external=True)
    for k, v in event.custom_values.iteritems():
        data[k] = v
    return data

@app.route('/worddomination1/api/event/', methods=['POST'])
def create_event():
    expected_values = ["tid", "name", "description", "skill_points", "score_points", "skill_interval", "score_interval"]
    data = request.get_json()
    tid = data["tid"]
    name = data["name"]
    description = data["description"]
    skill_points = data["skill_points"]
    score_points = data["score_points"]
    skill_interval = data["skill_interval"]
    score_interval = data["score_interval"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    event = Event(tid, name, description, skill_points, score_points,
                  skill_interval, score_interval, custom_values=custom_values)
    db.session.add(event)
    db.session.commit()
    return jsonify(get_event_json(event)), 201

@app.route('/worddomination1/api/event/', methods=['GET'])
def get_all_events():
    events = Event.query.order_by(Task.id).all()
    if not events:
        abort(404)
    data = []
    for e in events:
        data.append(get_event_json(e))
    return jsonify({"data":data})

@app.route('/worddomination1/api/event/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get(id)
    if not event:
        abort(404)
    return jsonify(get_event_json(event))

@app.route('/worddomination1/api/event/<int:id>', methods=['PUT'])
def update_event(id):
    expected_values = ["tid", "name", "description", "skill_points", "score_points", "skill_interval", "score_interval"]
    event = Event.query.get(id)
    if not event:
        abort(404)
    data = request.get_json()
    event.tid = data["tid"]
    event.name = data["name"]
    event.description = data["description"]
    event.skill_points = data["skill_points"]
    event.score_points = data["score_points"]
    event.skill_interval = data["skill_interval"]
    event.score_interval = data["score_interval"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    event.custom_values = custom_values
    db.session.commit()
    return jsonify(get_event_json(event))

@app.route('/worddomination1/api/event/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get(id)
    if not event:
        abort(404)
    db.session.delete(event)
    db.session.commit()
    return "", 204

# @app.route('/worddomination1/api/level_instance/', methods=['POST'])
# def start_level_instance():
#     expected_values = ["level", "players", "start_time", "atempt", "end_time"]
#     data = request.get_json()
#     lid = data["lid"]
#     start_time = data.get("start_time", datetime.now())
#     players = data.get("players", [])
#     custom_values = {}
#     for k, v in data.iteritems():
#         if k not in expected_values:
#            custom_values[k] = v
#     atempt = 1
#     level_instance = LevelInstance(custom_values=custom_values)
#     db.session.add(player)
#     db.session.commit(
#     return "bla", 201
