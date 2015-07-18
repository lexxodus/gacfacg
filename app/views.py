from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import app, db
from app.models import Player, Level, LevelInstance, LevelType, Task,\
    Event, Participation, TriggeredEvent, EventSkill
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
    player = Player(custom_values)
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
    if "name" in data:
        player.name = data["name"]
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
    expected_values = ["name", "description", "level_types"]
    data = request.get_json()
    if "name" not in data:
        abort(400)
    name = data["name"]
    description = data.get("description", "")
    level_types = data.get("level_types", None)
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    level = Level(name, description, level_types, custom_values)
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
    if "name" in data:
        level.name = data["name"]
    if "description" in data:
        level.description = data["description"]
    if "level_types" in data:
        level.level_types = data["level_types"]
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
    if "name" not in data:
        abort(400)
    name = data["name"]
    description = data.get("description", "")
    levels = data.get("levels", None)
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    level_type = LevelType(name, description, levels, custom_values)
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
    if "name" in data:
        level_type.name = data["name"]
    if "description" in data:
        level_type.description = data["description"]
    if "levels" in data:
        level_type.assign_to_level(data["levels"])
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
    if "name" not in data:
        abort(400)
    name = data["name"]
    description = data.get("description", "")
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    task = Task(name, description, custom_values)
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
    if "name" in data:
        task.name = data["name"]
    if "description" in data:
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
    required_values = ["tid", "name"]
    data = request.get_json()
    if not all(v in data for v in required_values):
        abort(400)
    tid = data["tid"]
    name = data["name"]
    description = data.get("description", "")
    skill_points = data.get("skill_points", 0)
    score_points = data.get("score_points", 0)
    skill_interval = data.get("skill_interval", 1)
    score_interval = data.get("score_interval", 1)
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    event = Event(tid, name, description, skill_points, score_points,
                  skill_interval, score_interval, custom_values)
    db.session.add(event)
    db.session.commit()
    return jsonify(get_event_json(event)), 201

@app.route('/worddomination1/api/event/', methods=['GET'])
def get_all_events():
    events = Event.query.order_by(Event.id).all()
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
    if "tid" in data:
        event.tid = data["tid"]
    if "name" in data:
        event.name = data["name"]
    if "description" in data:
        event.description = data["description"]
    if "skill_points" in data:
        event.skill_points = data["skill_points"]
    if "score_points" in data:
        event.score_points = data["score_points"]
    if "skill_interval" in data:
        event.skill_interval = data["skill_interval"]
    if "score_interval" in data:
        event.score_interval = data.get["score_interval"]
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

def get_level_instance_json(level_instance, public=True):
    data = {}
    data["id"] = level_instance.id
    data["lid"] = level_instance.lid
    data["start_time"] = level_instance.start_time
    data["end_time"] = level_instance.end_time
    if public:
        data['api_url'] = url_for('get_level_instance', id=data['id'], _external=True)
    for k, v in level_instance.custom_values.iteritems():
        data[k] = v
    return data

@app.route('/worddomination1/api/level_instance/', methods=['POST'])
def create_level_instance():
    expected_values = ["lid", "start_time", "end_time"]
    data = request.get_json()
    if "lid" not in data:
        abort(404)
    lid = data["lid"]
    start_time = data.get("start_time", datetime.now())
    end_time = data.get("end_time", None)
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
           custom_values[k] = v
    level_instance = LevelInstance(lid, start_time, end_time, custom_values)
    db.session.add(level_instance)
    db.session.commit()
    return jsonify(get_level_instance_json(level_instance)), 201

@app.route('/worddomination1/api/level_instance/', methods=['GET'])
def get_all_level_instances():
    level_instances = LevelInstance.query.order_by(LevelInstance.id).all()
    if not level_instances:
        abort(404)
    data = []
    for li in level_instances:
        data.append(get_level_instance_json(level_instances))
    return jsonify({"data":data})

@app.route('/worddomination1/api/level_instance/<int:id>', methods=['GET'])
def get_level_instance(id):
    level_instance = LevelInstance.query.get(id)
    if not level_instance:
        abort(404)
    return jsonify(get_level_instance_json(level_instance))

@app.route('/worddomination1/api/level_instance/<int:id>', methods=['PUT'])
def update_level_instance(id):
    expected_values = ["lid", "start_time", "end_time"]
    level_instance = LevelInstance.query.get(id)
    if not level_instance:
        abort(404)
    data = request.get_json()
    if "lid" in data:
        level_instance.lid = data["lid"]
    if "start_time" in data:
        level_instance.start_time = data["start_time"]
    if "end_time" in data:
        level_instance.end_time = data["end_time"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    level_instance.custom_values = custom_values
    db.session.commit()
    return jsonify(get_level_instance_json(level_instance))

@app.route('/worddomination1/api/level_instance/<int:id>', methods=['DELETE'])
def delete_level_instance(id):
    level_instance = LevelInstance.query.get(id)
    if not level_instance:
        abort(404)
    db.session.delete(level_instance)
    db.session.commit()
    return "", 204

def get_participation_json(participation, public=True):
    data = {}
    data["id"] = participation.id
    data["pid"] = participation.pid
    data["liid"] = participation.liid
    data["start_time"] = participation.start_time
    data["end_time"] = participation.end_time
    if public:
        data['api_url'] = url_for('get_participation', id=data['id'], _external=True)
    for k, v in participation.custom_values.iteritems():
        data[k] = v
    return data

@app.route('/worddomination1/api/participation/', methods=['POST'])
def create_participation():
    expected_values = ["pid", "liid", "start_time", "end_time"]
    required_values = ["pid", "liid"]
    data = request.get_json()
    for v in required_values:
        if v not in data:
            abort(404)
    pid = data["pid"]
    liid = data["liid"]
    start_time = data.get("start_time", datetime.now())
    end_time = data.get("end_time", None)
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
           custom_values[k] = v
    participation = Participation(pid, liid, start_time, end_time, custom_values)
    db.session.add(participation)
    db.session.commit()
    return jsonify(get_participation_json(participation)), 201

@app.route('/worddomination1/api/participation/', methods=['GET'])
def get_all_participations():
# TODO: Offer filters
    participations = Participation.query.order_by(Participation.id).all()
    if not participations:
        abort(404)
    data = []
    for pa in participations:
        data.append(get_participation_json(pa))
    return jsonify({"data":data})

@app.route('/worddomination1/api/participation/<int:id>', methods=['GET'])
def get_participation(id):
    participation = Participation.query.get(id)
    if not participation:
        abort(404)
    return jsonify(get_paricipation_json(participation))

@app.route('/worddomination1/api/participaton/<int:id>', methods=['PUT'])
def update_participation(id):
    expected_values = ["pid", "liid", "start_time", "end_time"]
    participation = Participation.query.get(id)
    if not participation:
        abort(404)
    data = request.get_json()
    if "pid" in data:
        participation.pid = data["pid"]
    if "lid" in data:
        participation.liid = data["liid"]
    if "start_time" in data:
        participation.start_time = data["start_time"]
    if "end_time" in data:
        participation.end_time = data["end_time"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    participation.custom_values = custom_values
    db.session.commit()
    return jsonify(get_participation_json(participation))

@app.route('/worddomination1/api/participation/<int:id>', methods=['DELETE'])
def delete_participation(id):
    participation = Participation.query.get(id)
    if not participation:
        abort(404)
    db.session.delete(participation)
    db.session.commit()
    return "", 204

def get_triggered_event_json(triggered_event, public=True):
    data = {}
    data["id"] = triggered_event.id
    data["paid"] = triggered_event.paid
    data["eid"] = triggered_event.eid
    data["timestamp"] = triggered_event.time_stamp
    if public:
        data['api_url'] = url_for('get_triggered_event', id=data['id'], _external=True)
    for k, v in triggered_event.custom_values.iteritems():
        data[k] = v
    return data

@app.route('/worddomination1/api/triggered_event/', methods=['POST'])
def create_triggered_event():
    expected_values = ["paid", "eid", "timestamp"]
    required_values = ["paid", "eid"]
    data = request.get_json()
    if not all(v in data for v in required_values):
        abort(404)
    paid = data["paid"]
    eid = data["eid"]
    time_stamp = data.get("timestamp", datetime.now())
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
           custom_values[k] = v
    triggered_event = LevelInstance(paid, eid, time_stamp, custom_values)
    db.session.add(triggered_event)
    db.session.commit()
    return jsonify(get_triggered_event_json(triggered_event)), 201

@app.route('/worddomination1/api/triggered_event/', methods=['GET'])
def get_all_triggered_events():
    args = request.args
    query = TriggeredEvent.query
    pids = args.getlist("pid")
    liids = args.getlist("liid")
    lids = args.getlist("lid")
    ltids = args.getlist("ltid")
    tids = args.getlist("tid")
    eids = args.getlist("eid")
    if pids or liids or lids or ltids:
        participations = Participation.query.with_entities(Participation.id)
        if pids:
            participations = Participation.query.with_entities(Participation.id).filter(Participation.pid in pids)
        if ltids or lids:
            level_instance = LevelInstance.query
            if ltids:
                levels = Level.query.with_entities(Level.id).filter(ltids in ltids).all()
                lids += levels
            if lids:
                level_instances = level_instance.filter(LevelInstance.lid in lids).all()
                liids += level_instances
        if liids:
            participations = participations.filter(Participation.pid in liids)
        query = query.filter(TriggeredEvent.paid in participations)
        if tids:
            tasks = Event.query.with_entities(Event.id).filter(Event.tid in tids).all()
            eids += tasks
        if eids:
            query = query.filter(TriggeredEvent.eid in eids)
    triggered_events = query.order_by(TriggeredEvent.id).all()
    if not triggered_events:
        abort(404)
    data = []
    for t in triggered_events:
        data.append(get_triggered_event_json(t))
    return jsonify({"data":data})

@app.route('/worddomination1/api/triggered_event/<int:id>', methods=['GET'])
def get_triggered_event(id):
    triggered_event = TriggeredEvent.query.get(id)
    if not triggered_event:
        abort(404)
    return jsonify(get_triggered_event_json(triggered_event))

@app.route('/worddomination1/api/triggered_event/<int:id>', methods=['PUT'])
def update_triggered_event(id):
    expected_values = ["paid", "eid", "timestamp"]
    triggered_event = TriggeredEvent.query.get(id)
    if not triggered_event:
        abort(404)
    data = request.get_json()
    if "paid" in data:
        triggered_event.paid = data["lid"]
    if "eid" in data:
        triggered_event.eid = data["eid"]
    if "timestamp" in data:
        triggered_event.timestamp = data["timestamp"]
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
            custom_values[k] = v
    triggered_event.custom_values = custom_values
    db.session.commit()
    return jsonify(get_triggered_event_json(triggered_event))

@app.route('/worddomination1/api/triggered_event/<int:id>', methods=['DELETE'])
def delete_triggered_event(id):
    triggered_event = TriggeredEvent.query.get(id)
    if not triggered_event:
        abort(404)
    db.session.delete(triggered_event)
    db.session.commit()
    return "", 204


def get_event_skill_json(event_skill, public=True):
    data = {}
    data["id"] = event_skill.id
    data["paid"] = event_skill.paid
    data["eid"] = event_skill.eid
    data["calculated_on"] = event_skill.calculated_on
    data["considered_rows"] = event_skill.considered_rows
    data["skill_points"] = event_skill.skill_points
    data["score_points"] = event_skill.score_points
    if public:
        data['api_url'] = url_for('get_triggered_event', id=data['id'], _external=True)
    return data

@app.route('/worddomination1/api/event_skill/', methods=['POST'])
def calculate_event_skill():
    required_values = ["pid", "eid"]
    data = request.get_json()
    if not all(v in data for v in required_values):
        abort(404)
    pid = data["pid"]
    eid = data["eid"]
    event_skill = EventSkill(pid, eid)
    db.session.add(event_skill)
    db.session.commit()
    return jsonify(get_event_skill_json(event_skill)), 201

# @app.route('/worddomination1/api/event_skill/', methods=['GET'])
# def get_all_event_skill():
#     args = request.args
#     query = EventSkill.query
#     pids = args.getlist("pid")
#     liids = args.getlist("liid")
#     lids = args.getlist("lid")
#     ltids = args.getlist("ltid")
#     tids = args.getlist("tid")
#     eids = args.getlist("eid")
#     if pids or liids or lids or ltids:
#         participations = Participation.query.with_entities(Participation.id)
#         if pids:
#             participations = Participation.query.with_entities(Participation.id).filter(Participation.pid in pids)
#         if ltids or lids:
#             level_instance = LevelInstance.query
#             if ltids:
#                 levels = Level.query.with_entities(Level.id).filter(ltids in ltids).all()
#                 lids += levels
#             if lids:
#                 level_instances = level_instance.filter(LevelInstance.lid in lids).all()
#                 liids += level_instances
#         if liids:
#             participations = participations.filter(Participation.pid in liids)
#         query = query.filter(TriggeredEvent.paid in participations)
#         if tids:
#             tasks = Event.query.with_entities(Event.id).filter(Event.tid in tids).all()
#             eids += tasks
#         if eids:
#             query = query.filter(TriggeredEvent.eid in eids)
#     triggered_events = query.order_by(TriggeredEvent.id).all()
#     if not triggered_events:
#         abort(404)
#     data = []
#     for t in triggered_events:
#         data.append(get_triggered_event_json(t))
#     return jsonify({"data":data})
#
# @app.route('/worddomination1/api/triggered_event/<int:id>', methods=['GET'])
# def get_triggered_event(id):
#     triggered_event = TriggeredEvent.query.get(id)
#     if not triggered_event:
#         abort(404)
#     return jsonify(get_triggered_event_json(triggered_event))
#
# @app.route('/worddomination1/api/triggered_event/<int:id>', methods=['PUT'])
# def update_triggered_event(id):
#     expected_values = ["paid", "eid", "timestamp"]
#     triggered_event = TriggeredEvent.query.get(id)
#     if not triggered_event:
#         abort(404)
#     data = request.get_json()
#     if "paid" in data:
#         triggered_event.paid = data["lid"]
#     if "eid" in data:
#         triggered_event.eid = data["eid"]
#     if "timestamp" in data:
#         triggered_event.timestamp = data["timestamp"]
#     custom_values = {}
#     for k, v in data.iteritems():
#         if k not in expected_values:
#             custom_values[k] = v
#     triggered_event.custom_values = custom_values
#     db.session.commit()
#     return jsonify(get_triggered_event_json(triggered_event))
#
# @app.route('/worddomination1/api/triggered_event/<int:id>', methods=['DELETE'])
# def delete_triggered_event(id):
#     triggered_event = TriggeredEvent.query.get(id)
#     if not triggered_event:
#         abort(404)
#     db.session.delete(triggered_event)
#     db.session.commit()
#     return "", 204
