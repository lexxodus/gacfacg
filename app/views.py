from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import app
from flask import make_response

@app.route('/')
@app.route('/entities')
@app.route('/histories')
@app.route('/player-add')
@app.route('/player-edit/<int:id>')
@app.route('/player-view/<int:id>')
@app.route('/level-add')
@app.route('/level-edit/<int:id>')
@app.route('/level-view/<int:id>')
@app.route('/level_type-add')
@app.route('/level_type-edit/<int:id>')
@app.route('/level_type-view/<int:id>')
@app.route('/event-add')
@app.route('/event-edit/<int:id>')
@app.route('/event-view/<int:id>')
@app.route('/task-add')
@app.route('/task-edit/<int:id>')
@app.route('/task-view/<int:id>')
@app.route('/level_instance-view/<int:id>')
@app.route('/participation-view/<int:id>')
@app.route('/triggered_event-view/<int:id>')
def angular(id=None):
    resp = make_response(open('app/templates/index.html').read())
    resp.mimetype = 'text/html'
    return resp
