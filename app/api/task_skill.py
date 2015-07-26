from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import TaskSkill as TaskSkillModel
from flask import abort, request
from flask.ext.restful import Resource

def get_task_skill_json(task_skill, public=True):
    data = {}
    data["id"] = task_skill.id
    data["pid"] = task_skill.pid
    data["tid"] = task_skill.tid
    data["calculated_on"] = task_skill.calculated_on.isoformat()
    data["considered_rows"] = task_skill.considered_rows
    data["skill_points"] = task_skill.skill_points
    if public:
        data['api_url'] = api.url_for(TaskSkill)
    return data


class TaskSkill(Resource):

    def post(self):
        required_values = ["pid", "tid"]
        data = request.get_json()
        if not all(v in data for v in required_values):
            abort(404)
        pid = data["pid"]
        tid = data["tid"]
        task_skill = TaskSkillModel(pid, tid)
        db.session.add(task_skill)
        db.session.commit()
        return get_task_skill_json(task_skill), 201

    def get(self, id=None):
        if id:
            task_skill = TaskSkillModel.query.get(id)
            if not task_skill:
                abort(404)
            return get_task_skill_json(task_skill)
        else:
            return self.get_all()

    def get_all(self):
        level_skills = TaskSkillModel.query.order_by(TaskSkillModel.id).all()
        if not level_skills:
            abort(404)
        data = []
        for l in level_skills:
            data.append(get_task_skill_json(l))
        return data

    def delete(self, id):
        task_skill = TaskSkillModel.query.get(id)
        if not task_skill:
            abort(404)
        db.session.delete(task_skill)
        db.session.commit()
        return "", 204
