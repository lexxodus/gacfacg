from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import LevelType as LevelTypeModel
from flask import abort, request
from flask.ext.restful import Resource


def get_level_type_json(level_type, public=True):
    data = {}
    data["id"] = level_type.id
    data["name"] = level_type.name
    data["description"] = level_type.description
    if public:
        data['api_url'] = "%s%s" % (api.url_for(LevelType), level_type.id)
    if level_type.custom_values:
        for k, v in level_type.custom_values.iteritems():
            data[k] = v
    return data


class LevelType(Resource):

    def post(self):
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
        level_type = LevelTypeModel(name, description, levels, custom_values)
        db.session.add(level_type)
        db.session.commit()
        return get_level_type_json(level_type), 201

    def get(self, id=None):
        if id:
            level_type = LevelTypeModel.query.get(id)
            if not level_type:
                abort(404)
            return get_level_type_json(level_type)
        else:
            return self.get_all()

    def get_all(self):
        level_types = LevelTypeModel.query.order_by(LevelTypeModel.id).all()
        if not level_types:
            abort(404)
        data = []
        for lt in level_types:
            data.append(get_level_type_json(lt))
        return data

    def put(self, id):
        expected_values = ["name", "description"]
        level_type = LevelTypeModel.query.get(id)
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
        return get_level_type_json(level_type)

    def delete(self, id):
        level_type = LevelTypeModel.query.get(id)
        if not level_type:
            abort(404)
        db.session.delete(level_type)
        db.session.commit()
        return "", 204
