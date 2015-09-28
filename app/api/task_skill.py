from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import TaskSkill as TaskSkillModel
from datetime import datetime, timedelta
from dateutil import parser
from flask import abort, request
from flask.ext.restful import Resource

def get_task_skill_json(task_skill, public=False):
    data = {}
    data["id"] = task_skill.id
    data["pid"] = task_skill.pid
    data["tid"] = task_skill.tid
    data["calculated_on"] = task_skill.calculated_on.isoformat()
    data["considered_rows"] = task_skill.considered_rows
    data["skill_points"] = task_skill.skill_points
    if public:
        data['api_url'] = "%s%s" % (api.url_for(TaskSkill), task_skill.id)
    return data


class TaskSkill(Resource):

    def post(self):
        required_values = ["pid", "tid"]
        data = request.get_json()
        if not all(v in data for v in required_values):
            abort(404)
        pid = data["pid"]
        tid = data["tid"]
        until = data.get("until", None)
        if until:
            until = parser.parse(until)
        task_skill = TaskSkillModel(pid, tid, until)
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
        args = request.args
        task_skills = TaskSkillModel.query
        pids = args.getlist("pid")
        tids = args.getlist("tid")
        interval = args.get("interval", None)
        last = args.get("last", None)
        if pids:
            task_skills = task_skills.filter(TaskSkillModel.pid.in_(pids))
        if tids:
            task_skills = task_skills.filter(TaskSkillModel.tid.in_(tids))
        if interval:
            interval = int(interval)
            task_skills = task_skills.filter(TaskSkillModel.calculated_on >= datetime.now() - timedelta(seconds=interval))
        if last:
            task_skills = task_skills.order_by(TaskSkillModel.calculated_on.desc()).limit(last)
        else:
            task_skills = task_skills.order_by(TaskSkillModel.calculated_on).all()
        data = []
        for l in task_skills:
            data.append(get_task_skill_json(l))
        return data

    def delete(self, id):
        task_skill = TaskSkillModel.query.get(id)
        if not task_skill:
            abort(404)
        db.session.delete(task_skill)
        db.session.commit()
        return "", 204
