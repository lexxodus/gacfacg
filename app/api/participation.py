from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import Participation as ParticipationModel
from datetime import datetime
from flask import abort, request
from flask.ext.restful import Resource


def get_participation_json(participation, public=False):
    data = {}
    data["id"] = participation.id
    data["pid"] = participation.pid
    data["liid"] = participation.liid
    data["start_time"] = participation.start_time.isoformat()
    data["end_time"] = participation.end_time.isoformat()\
        if participation.end_time else None
    if public:
        data['api_url'] = "%s%s" % (
            api.url_for(Participation), participation.id)
    if participation.custom_values:
        for k, v in participation.custom_values.iteritems():
            data[k] = v
    return data

class Participation(Resource):

    def post(self):
        expected_values = ["pid", "liid", "start_time", "end_time"]
        required_values = ["pid", "liid"]
        data = request.get_json()
        if not all(v in data for v in required_values):
            abort(404)
        pid = data["pid"]
        liid = data["liid"]
        start_time = data.get("start_time", datetime.now())
        end_time = data.get("end_time", None)
        custom_values = {}
        for k, v in data.iteritems():
            if k not in expected_values:
               custom_values[k] = v
        participation = ParticipationModel(
            pid, liid, start_time, end_time, custom_values)
        db.session.add(participation)
        db.session.commit()
        return get_participation_json(participation), 201


    def get(self, id=None):
        if id:
            participation = ParticipationModel.query.get(id)
            if not participation:
                abort(404)
            return get_participation_json(participation)
        else:
            return self.get_all()

    def get_all(self):
        participations = ParticipationModel.query.order_by(
            ParticipationModel.id).all()
        if not participations:
            abort(404)
        data = []
        for pa in participations:
            data.append(get_participation_json(pa))
        return data

    def put(self, id):
        expected_values = ["pid", "liid", "start_time", "end_time"]
        participation = ParticipationModel.query.get(id)
        if not participation:
            abort(404)
        data = request.get_json()
        if "pid" in data:
            participation.pid = data["pid"]
        if "lid" in data:
            participation.liid = data["liid"]
        if "start_time" in data:
            participation.start_time = data["start_time"]
        if "end_time" in data:
            participation.end_time = data["end_time"]
        custom_values = {}
        for k, v in data.iteritems():
            if k not in expected_values:
                custom_values[k] = v
        participation.custom_values = custom_values
        db.session.commit()
        return get_participation_json(participation)

    def delete(self, id):
        participation = Participation.query.get(id)
        if not participation:
            abort(404)
        db.session.delete(participation)
        db.session.commit()
        return "", 204