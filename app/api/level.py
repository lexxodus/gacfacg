from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import Level as LevelModel
from app.models import LevelType
from flask import abort, request
from flask.ext.restful import Resource

def get_level_json(level, public=False):
    data = {}
    data["id"] = level.id
    data["name"] = level.name
    data["description"] = level.description
    if public:
        data['api_url'] = "%s%s" % (api.url_for(Level), level.id)
    if level.custom_values:
        for k, v in level.custom_values.iteritems():
            data[k] = v
    return data


class Level(Resource):

    def post(self):
        expected_values = ["name", "description", "level_types"]
        data = request.get_json()
        if "name" not in data:
            abort(400)
        name = data["name"]
        description = data.get("description", "")
        level_types = data.get("level_types", [])
        for i, lt in enumerate(level_types):
            level_types[i] = LevelType.query.get(lt)
        custom_values = {}
        for k, v in data.iteritems():
            if k not in expected_values:
                custom_values[k] = v
        level = LevelModel(name, description, level_types, custom_values)
        db.session.add(level)
        db.session.commit()
        return get_level_json(level), 201

    def get(self, id=None):
        if id:
            level = LevelModel.query.get(id)
            if not level:
                abort(404)
            return get_level_json(level)
        else:
            return self.get_all()

    def get_all(self):
        levels = LevelModel.query.order_by(LevelModel.id).all()
        if not levels:
            abort(404)
        data = []
        for l in levels:
            data.append(get_level_json(l))
        return data

    def put(self, id):
        expected_values = ["name", "description"]
        level = LevelModel.query.get(id)
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
        return get_level_json(level)

    def delete(self, id):
        level = LevelModel.query.get(id)
        if not level:
            abort(404)
        db.session.delete(level)
        db.session.commit()
        return "", 204
