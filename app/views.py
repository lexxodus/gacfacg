from __future__ import unicode_literals
__author__ = 'lexxodus'

from app import app

@app.route('/')
def hello_world():
    return 'Hello World!'