from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import LevelInstance as LevelInstanceModel
from datetime import datetime
from flask import abort, request
from flask.ext.restful import Resource


def get_level_instance_json(level_instance, public=True):
    data = {}
    data["id"] = level_instance.id
    data["lid"] = level_instance.lid
    data["start_time"] = level_instance.start_time
    data["end_time"] = level_instance.end_time
    if public:
        data['api_url'] = api.url_for(LevelInstance)
    for k, v in level_instance.custom_values.iteritems():
        data[k] = v
    return data

class LevelInstance(Resource):

    def post(self):
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
        level_instance = LevelInstanceModel(lid, start_time, end_time, custom_values)
        db.session.add(level_instance)
        db.session.commit()
        return get_level_instance_json(level_instance), 201

    def get(self, id=None):
        if id:
            level_instance = LevelInstance.query.get(id)
            if not level_instance:
                abort(404)
            return get_level_instance_json(level_instance)
        else:
            return self.get_all()

    def get_all(self):
        level_instances = LevelInstanceModel.query.order_by(LevelInstance.id).all()
        if not level_instances:
            abort(404)
        data = []
        for li in level_instances:
            data.append(get_level_instance_json(level_instances))
        return data

    def put(self, id):
        expected_values = ["lid", "start_time", "end_time"]
        level_instance = LevelInstanceModel.query.get(id)
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
        return get_level_instance_json(level_instance)

    def delete(self, id):
        level_instance = LevelInstanceModel.query.get(id)
        if not level_instance:
            abort(404)
        db.session.delete(level_instance)
        db.session.commit()
        return "", 204