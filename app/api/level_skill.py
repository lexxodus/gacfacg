from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import LevelSkill as LevelSkillModel
from datetime import datetime, timedelta
from dateutil import parser
from flask import abort, request
from flask.ext.restful import Resource

def get_level_skill_json(level_skill, public=False):
    data = {}
    data["id"] = level_skill.id
    data["pid"] = level_skill.pid
    data["lid"] = level_skill.lid
    data["calculated_on"] = level_skill.calculated_on.isoformat()
    data["considered_rows"] = level_skill.considered_rows
    data["skill_points"] = level_skill.skill_points
    data["high_score"] = level_skill.high_score
    data["attempt"] = level_skill.attempt
    if public:
        data['api_url'] = "%s%s" % (api.url_for(LevelSkill), level_skill.id)
    return data


class LevelSkill(Resource):

    def post(self):
        required_values = ["pid", "lid"]
        data = request.get_json()
        if not all(v in data for v in required_values):
            abort(404)
        pid = data["pid"]
        lid = data["lid"]
        until = data.get("until", None)
        if until:
            until = parser.parse(until)
        level_skill = LevelSkillModel(pid, lid, until)
        db.session.add(level_skill)
        db.session.commit()
        return get_level_skill_json(level_skill), 201

    def get(self, id=None):
        if id:
            level_skill = LevelSkillModel.query.get(id)
            if not level_skill:
                abort(404)
            return get_level_skill_json(level_skill)
        else:
            return self.get_all()

    def get_all(self):
        args = request.args
        level_skills = LevelSkillModel.query
        pids = args.getlist("pid")
        lids = args.getlist("lid")
        interval = args.getlist("interval")
        last = args.get("last", None)
        if pids:
            level_skills = level_skills.filter(LevelSkillModel.pid.in_(pids))
        if lids:
            level_skills = level_skills.filter(LevelSkillModel.lid.in_(lids))
        if interval:
            level_skills = level_skills.filter(LevelSkillModel.calculated_on >= datetime.now() - timedelta(seconds=interval))
        if last:
            level_skills = level_skills.order_by(LevelSkillModel.calculated_on.desc()).limit(last)
        else:
            level_skills = level_skills.order_by(LevelSkillModel.calculated_on).all()
        data = []
        for l in level_skills:
            data.append(get_level_skill_json(l))
        return data

    def delete(self, id):
        level_skill = LevelSkillModel.query.get(id)
        if not level_skill:
            abort(404)
        db.session.delete(level_skill)
        db.session.commit()
        return "", 204
