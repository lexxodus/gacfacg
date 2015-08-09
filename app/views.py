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
def angular(id=None):
    resp = make_response(open('app/templates/index.html').read())
    resp.mimetype = 'text/html'
    return resp
