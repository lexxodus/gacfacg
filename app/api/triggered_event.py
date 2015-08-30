from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import db
from app.api import api
from app.models import TriggeredEvent as TriggeredEventModel
from app.models import Participation as ParticipationModel
from app.models import LevelInstance as LevelInstanceModel
from app.models import LevelType as LevelTypeModel
from app.models import Level as LevelModel
from app.models import Event as EventModel
from datetime import datetime
from flask import abort, request
from flask.ext.restful import Resource

def get_triggered_event_json(triggered_event, public=False):
    data = {}
    data["id"] = triggered_event.id
    data["paid"] = triggered_event.paid
    data["eid"] = triggered_event.eid
    data["timestamp"] = triggered_event.timestamp.isoformat()
    data["given_skill_points"] = triggered_event.given_skill_points;
    data["given_score_points"] = triggered_event.given_score_points;
    if public:
        data['api_url'] = "%s%s" % (
            api.url_for(TriggeredEvent), triggered_event.id)
    if triggered_event.custom_values:
        for k, v in triggered_event.custom_values.iteritems():
            data[k] = v
    return data


class TriggeredEvent(Resource):

    def post(self):
        expected_values = ["paid", "eid", "timestamp"]
        required_values = ["paid", "eid"]
        data = request.get_json()
        if not all(v in data for v in required_values):
            abort(404)
        paid = data["paid"]
        eid = data["eid"]
        timestamp = data.get("timestamp", datetime.now())
        custom_values = {}
        for k, v in data.iteritems():
            if k not in expected_values:
               custom_values[k] = v
        try:
          triggered_event = TriggeredEventModel(paid, eid, timestamp, custom_values)
        except:
            abort(404)
        db.session.add(triggered_event)
        db.session.commit()
        return get_triggered_event_json(triggered_event), 201


    def get(self, id=None):
        if id:
            triggered_event = TriggeredEventModel.query.get(id)
            if not triggered_event:
                abort(404)
            return get_triggered_event_json(triggered_event)
        else:
            return self.get_all()

    def get_all(self):
        args = request.args
        query = TriggeredEventModel.query
        pids = args.getlist("pid")
        liids = args.getlist("liid")
        lids = args.getlist("lid")
        ltids = args.getlist("ltid")
        tids = args.getlist("tid")
        eids = args.getlist("eid")
        if pids or liids or lids or ltids:
            participations = ParticipationModel.query.with_entities(
                ParticipationModel.id)
            if pids:
                participations = participations.filter(
                    ParticipationModel.pid.in_(pids))
            if ltids or lids:
                level_instance = LevelInstanceModel.query
                if ltids:
                    levels = LevelModel.query.with_entities(
                        LevelModel.id).join(LevelModel.level_types).\
                        filter(LevelModel.level_types.in_(ltids)).all()
                    lids += levels
                if lids:
                    level_instances = level_instance.filter(
                        LevelInstanceModel.lid.in_(lids)).all()
                    liids += level_instances
            if liids:
                participations = participations.filter(
                    ParticipationModel.liid.in_(liids))
            query = query.filter(TriggeredEventModel.paid.in_(participations))
            if tids:
                tasks = EventModel.query.with_entities(
                    EventModel.id).filter(EventModel.tid_in(tids)).all()
                eids += tasks
            if eids:
                query = query.filter(TriggeredEventModel.eid.in_(eids))
        triggered_events = query.order_by(TriggeredEventModel.id).all()
        data = []
        for t in triggered_events:
            data.append(get_triggered_event_json(t))
        return data


    def put(self, id):
        expected_values = ["paid", "eid", "timestamp"]
        triggered_event = TriggeredEventModel.query.get(id)
        if not triggered_event:
            abort(404)
        data = request.get_json()
        if "paid" in data:
            triggered_event.paid = data["paid"]
        if "eid" in data:
            triggered_event.eid = data["eid"]
        if "timestamp" in data:
            triggered_event.timestamp = data["timestamp"]
        custom_values = {}
        for k, v in data.iteritems():
            if k not in expected_values:
                custom_values[k] = v
        triggered_event.custom_values = custom_values
        db.session.commit()
        return get_triggered_event_json(triggered_event)


    def delete(self, id):
        triggered_event = TriggeredEventModel.query.get(id)
        if not triggered_event:
            abort(404)
        db.session.delete(triggered_event)
        db.session.commit()
        return "", 204