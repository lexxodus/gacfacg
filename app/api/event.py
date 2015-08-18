from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import Event as EventModel
from flask import abort, request
from flask.ext.restful import Resource


def get_event_json(event, public=False):
    data = {}
    data["id"] = event.id
    data["tid"] = event.tid
    data["name"] = event.name
    data["description"] = event.description
    data["skill_points"] = event.skill_points
    data["score_points"] = event.score_points
    data["skill_interval"] = event.skill_interval
    data["score_interval"] = event.score_interval
    data["skill_rule"] = event.skill_rule
    data["score_rule"] = event.score_rule
    if public:
        data['api_url'] = "%s%s" % (api.url_for(Event), event.id)
    if event.custom_values:
        for k, v in event.custom_values.iteritems():
            data[k] = v
    return data

class Event(Resource):

    def post(self):
        expected_values = ["tid", "name", "description", "skill_points", "score_points", "skill_interval", "score_interval"]
        required_values = ["tid", "name"]
        data = request.get_json()
        if not all(v in data for v in required_values):
            abort(400)
        tid = data["tid"]
        name = data["name"]
        description = data.get("description", "")
        skill_points = data.get("skill_points", 0)
        score_points = data.get("score_points", 0)
        skill_interval = data.get("skill_interval", 1)
        score_interval = data.get("score_interval", 1)
        custom_values = {}
        for k, v in data.iteritems():
            if k not in expected_values:
                custom_values[k] = v
        event = EventModel(tid, name, description, skill_points, score_points,
                      skill_interval, score_interval, custom_values)
        db.session.add(event)
        db.session.commit()
        return get_event_json(event), 201

    def get(self, id=None):
        if id:
            event = EventModel.query.get(id)
            if not event:
                abort(404)
            return get_event_json(event)
        else:
            return self.get_all()

    def get_all(self):
        events = EventModel.query.order_by(EventModel.id).all()
        data = []
        for e in events:
            data.append(get_event_json(e))
        return data

    def put(self, id):
        expected_values = ["tid", "name", "description", "skill_points",
                           "score_points", "skill_interval",
                           "score_interval", "skill_rule", "score_rule"]
        event = EventModel.query.get(id)
        if not event:
            abort(404)
        data = request.get_json()
        if "tid" in data:
            event.tid = data["tid"]
        if "name" in data:
            event.name = data["name"]
        if "description" in data:
            event.description = data["description"]
        if "skill_points" in data:
            event.skill_points = data["skill_points"]
        if "score_points" in data:
            event.score_points = data["score_points"]
        if "skill_interval" in data:
            event.skill_interval = data["skill_interval"]
        if "score_interval" in data:
            event.score_interval = data["score_interval"]
        custom_values = {}
        for k, v in data.iteritems():
            if k not in expected_values:
                custom_values[k] = v
        event.custom_values = custom_values
        db.session.commit()
        return get_event_json(event)

    def delete(self, id):
        event = EventModel.query.get(id)
        if not event:
            abort(404)
        db.session.delete(event)
        db.session.commit()
        return "", 204
