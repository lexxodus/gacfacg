from __future__ import unicode_literals
__author__ = 'lexxodus'

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
import os

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()