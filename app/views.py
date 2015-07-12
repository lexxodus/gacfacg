from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import app, db
from app.models import Player, Level, LevelInstance
from datetime import datetime
from flask import jsonify, request

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/worddomination1/api/player/', methods=['POST'])
def create_player():
    data = request.get_json()
    print(data)
    custom_values = {}
    for k, v in data.iteritems():
        custom_values[k] = v
    player = Player(custom_values=custom_values)
    db.session.add(player)
    db.session.commit()
    return "%s" % player.id, 201

@app.route('/worddomination1/api/level_instance/', methods=['POST'])
def start_level_instance():
    expected_values = ["level", "players", "start_time", "atempt", "end_time"]
    data = request.get_json()
    print(data)
    level = data["level"]
    start_time = data.get("start_time", datetime.now())
    players = data.get("players", [])
    custom_values = {}
    for k, v in data.iteritems():
        if k not in expected_values:
           custom_values[k] = v
    atempt = 1
    return "bla", 201