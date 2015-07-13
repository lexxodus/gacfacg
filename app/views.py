from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import app, db
from app.models import Player, Level, LevelInstance
from datetime import datetime
from flask import abort, jsonify, request, url_for

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/worddomination1/api/player/', methods=['POST'])
def create_player():
    data = request.get_json()
    custom_values = {}
    for k, v in data.iteritems():
        custom_values[k] = v
    player = Player(custom_values=custom_values)
    db.session.add(player)
    db.session.commit()
    return "%s" % player.id, 201

@app.route('/worddomination1/api/player/', methods=['GET'])
def get_all_players():
    players = Player.query.order_by(Player.id).all()
    if not players:
        abort(404)
    data = []
    for p in players:
        e = {}
        e["id"] = p.id
        for k, v in p.custom_values.iteritems():
            e[k] = v
        data.append(make_public(e))
    return jsonify({"data":data})

@app.route('/worddomination1/api/player/<int:id>', methods=['GET'])
def get_player(id):
    player = Player.query.get(id)
    if not player:
        abort(404)
    data = {}
    data["id"] = player.id
    for k, v in player.custom_values.iteritems():
        data[k] = v
    return jsonify(make_public(data))

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
    return get_player(id)

@app.route('/worddomination1/api/player/<int:id>', methods=['DELETE'])
def delete_player(id):
    player = Player.query.get(id)
    if not player:
        abort(404)
    db.session.delete(player)
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

def make_public(item):
    item['api_url'] = url_for('get_player', id=item['id'], _external=True)
    return item