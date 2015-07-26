from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import Task as TaskModel
from flask import abort, request
from flask.ext.restful import Resource


def get_task_json(task, public=True):
    data = {}
    data["id"] = task.id
    data["name"] = task.name
    data["description"] = task.description
    if public:
        data['api_url'] = api.url_for(Task)
    for k, v in task.custom_values.iteritems():
        data[k] = v
    return data


class Task(Resource):

    def post(self):
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
        task = TaskModel(name, description, custom_values)
        db.session.add(task)
        db.session.commit()
        return get_task_json(task), 201

    def get(self, id=None):
        if id:
            task = TaskModel.query.get(id)
            if not task:
                abort(404)
            return get_task_json(task)
        else:
            return self.get_all()

    def get_all(self):
        tasks = TaskModel.query.order_by(TaskModel.id).all()
        if not tasks:
            abort(404)
        data = []
        for t in tasks:
            data.append(get_task_json(t))
        return data

    def put(self, id):
        expected_values = ["name", "description"]
        task = TaskModel.query.get(id)
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
        return get_task_json(task)

    def delete(self, id):
        task = TaskModel.query.get(id)
        if not task:
            abort(404)
        db.session.delete(task)
        db.session.commit()
        return "", 204
