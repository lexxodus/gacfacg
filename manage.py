from __future__ import unicode_literals
from flask_collect import Collect
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from app import app, db

__author__ = 'lexxodus'

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

collect = Collect()
collect.init_app(app)
collect.init_script(manager)

if __name__ == '__main__':
    manager.run()
