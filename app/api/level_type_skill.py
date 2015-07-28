from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import LevelTypeSkill as LevelTypeSkillModel
from flask import abort, request
from flask.ext.restful import Resource

def get_level_type_skill_json(level_type_skill, public=True):
    data = {}
    data["id"] = level_type_skill.id
    data["pid"] = level_type_skill.pid
    data["ltid"] = level_type_skill.ltid
    data["calculated_on"] = level_type_skill.calculated_on.isoformat()
    data["considered_rows"] = level_type_skill.considered_rows
    data["skill_points"] = level_type_skill.skill_points
    data["high_score"] = level_type_skill.high_score
    if public:
        data['api_url'] = api.url_for(LevelTypeSkill)
    return data


class LevelTypeSkill(Resource):

    def post(self):
        required_values = ["pid", "ltid"]
        data = request.get_json()
        if not all(v in data for v in required_values):
            abort(404)
        pid = data["pid"]
        ltid = data["ltid"]
        level_type_skill = LevelTypeSkillModel(pid, ltid)
        db.session.add(level_type_skill)
        db.session.commit()
        return get_level_type_skill_json(level_type_skill), 201

    def get(self, id=None):
        if id:
            level_skill = LevelTypeSkillModel.query.get(id)
            if not level_skill:
                abort(404)
            return get_level_type_skill_json(level_skill)
        else:
            return self.get_all()

    def get_all(self):
        level_type_skills = LevelTypeSkillModel.query.order_by(LevelTypeSkillModel.id).all()
        if not level_type_skills:
            abort(404)
        data = []
        for l in level_type_skills:
            data.append(get_level_type_skill_json(l))
        return data

    def delete(self, id):
        level_type_skill = LevelTypeSkillModel.query.get(id)
        if not level_type_skill:
            abort(404)
        db.session.delete(level_type_skill)
        db.session.commit()
        return "", 204