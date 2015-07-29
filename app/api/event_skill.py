from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import EventSkill as EventSkillModel
from dateutil import parser
from flask import abort, request
from flask.ext.restful import Resource

def get_event_skill_json(event_skill, public=True):
    data = {}
    data["id"] = event_skill.id
    data["pid"] = event_skill.pid
    data["eid"] = event_skill.eid
    data["calculated_on"] = event_skill.calculated_on.isoformat()
    data["considered_rows"] = event_skill.considered_rows
    data["skill_points"] = event_skill.skill_points
    if public:
        data['api_url'] = api.url_for(EventSkill)
    return data


class EventSkill(Resource):

    def post(self):
        required_values = ["pid", "eid"]
        data = request.get_json()
        if not all(v in data for v in required_values):
            abort(404)
        pid = data["pid"]
        eid = data["eid"]
        until = data.get("until", None)
        if until:
            until = parser.parse(until)
        event_skill = EventSkillModel(pid, eid, until)
        db.session.add(event_skill)
        db.session.commit()
        return get_event_skill_json(event_skill), 201

    def get(self, id=None):
        if id:
            task_skill = EventSkillModel.query.get(id)
            if not task_skill:
                abort(404)
            return get_event_skill_json(task_skill)
        else:
            return self.get_all()

    def get_all(self):
        event_skills = EventSkillModel.query.order_by(EventSkillModel.id).all()
        if not event_skills:
            abort(404)
        data = []
        for l in event_skills:
            data.append(get_event_skill_json(l))
        return data

    def delete(self, id):
        event_skill = EventSkillModel.query.get(id)
        if not event_skill:
            abort(404)
        db.session.delete(event_skill)
        db.session.commit()
        return "", 204
