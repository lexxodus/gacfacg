from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import LevelSkill as LevelSkillModel
from flask import abort, request
from flask.ext.restful import Resource

def get_level_skill_json(level_skill, public=True):
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
        data['api_url'] = api.url_for(LevelSkill)
    return data


class LevelSkill(Resource):

    def post(self):
        required_values = ["pid", "lid"]
        data = request.get_json()
        if not all(v in data for v in required_values):
            abort(404)
        pid = data["pid"]
        lid = data["lid"]
        level_skill = LevelSkillModel(pid, lid)
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
        level_skills = LevelSkillModel.query.order_by(LevelSkillModel.id).all()
        if not level_skills:
            abort(404)
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