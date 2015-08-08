from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import app
from flask import make_response, render_template

@app.route('/')
@app.route('/entities')
@app.route('/histories')
@app.route('/player-add')
@app.route('/level-add')
def angular():
    resp = make_response(render_template('index.html'))
    resp.mimetype = 'text/html'
    return resp
