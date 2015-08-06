from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import app, db
# from app.models import Player, Level, LevelInstance, LevelType, Task,\
#     Event, Participation, TriggeredEvent, EventSkill
# from datetime import datetime
from flask import abort, jsonify, request, url_for, make_response, render_template

#@app.route('/history')
#@app.route('/entities')
@app.route('/')
def hello_world():
    resp = make_response(render_template('index.html'))
    resp.mimetype = 'text/html'
    return resp
