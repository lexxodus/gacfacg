from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import Player as PlayerModel
from flask import abort, request
from flask.ext.restful import Resource

def get_player_json(player, public=False):
    data = {}
    data["id"] = player.id
    data["name"] = player.name
    if public:
        data['api_url'] = "%s%s" % (api.url_for(Player), player.id)
    if player.custom_values:
        for k, v in player.custom_values.iteritems():
            data[k] = v
    return data


class Player(Resource):
    def post(self):
        data = request.get_json()
        if "name" not in data:
            abort(404)
        name = data["name"]
        custom_values = {}
        for k, v in data.iteritems():
            custom_values[k] = v
        player = PlayerModel(name, custom_values)
        db.session.add(player)
        db.session.commit()
        return get_player_json(player), 201

    def get(self, id=None):
        if id:
            player = PlayerModel.query.get(id)
            if not player:
                abort(404)
            return get_player_json(player)
        else:
            return self.get_all()

    def get_all(self):
        players = PlayerModel.query.order_by(PlayerModel.id).all()
        if not players:
            abort(404)
        data = []
        for p in players:
            data.append(get_player_json(p))
        return data

    def put(self, id):
        player = PlayerModel.query.get(id)
        if not player:
            abort(404)
        data = request.get_json()
        if "name" not in data:
            abort(404)
        player.name = data["name"]
        custom_values = {}
        for k, v in data.iteritems():
            custom_values[k] = v
        player.custom_values = custom_values
        db.session.commit()
        return get_player_json(player)

    def delete(self, id):
        player = PlayerModel.query.get(id)
        if not player:
            abort(404)
        db.session.delete(player)
        db.session.commit()
        return "", 204