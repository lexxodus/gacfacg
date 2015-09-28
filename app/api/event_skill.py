from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import EventSkill as EventSkillModel
from datetime import datetime, timedelta
from dateutil import parser
from flask import abort, request
from flask.ext.restful import Resource

def get_event_skill_json(event_skill, public=False):
    data = {}
    data["id"] = event_skill.id
    data["pid"] = event_skill.pid
    data["eid"] = event_skill.eid
    data["calculated_on"] = event_skill.calculated_on.isoformat()
    data["considered_rows"] = event_skill.considered_rows
    data["skill_points"] = event_skill.skill_points
    if public:
        data['api_url'] = "%s%s" % (api.url_for(EventSkill), event_skill.id)
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
        args = request.args
        event_skills = EventSkillModel.query
        pids = args.getlist("pid")
        eids = args.getlist("eid")
        interval = args.get("interval", None)
        last = args.get("last", None)
        if pids:
            event_skills = event_skills.filter(EventSkillModel.pid.in_(pids))
        if eids:
            event_skills = event_skills.filter(EventSkillModel.eid.in_(eids))
        if interval:
            event_skills = event_skills.filter(EventSkillModel.calculated_on >= datetime.now() - timedelta(seconds=interval))
        if last:
            event_skills = event_skills.order_by(EventSkillModel.calculated_on.desc()).limit(last)
        else:
            event_skills = event_skills.order_by(EventSkillModel.calculated_on).all()
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
