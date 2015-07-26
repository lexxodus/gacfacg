from __future__ import unicode_literals
__author__ = 'lexxodus'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import restful

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app)

# imported afterwards as flask instance is needed by this module
from app import models, views
from app.api import api
