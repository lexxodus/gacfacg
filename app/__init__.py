from __future__ import unicode_literals
from flask.ext.cors import CORS
__author__ = 'lexxodus'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app)
# CORS(app, resources=r'/api/*', allow_headers='Content-Type')
app.debug = True
app.config.from_object('app.config')
db = SQLAlchemy(app)

# imported afterwards as flask instance is needed by this module
from app import models, views
from app.api import api
