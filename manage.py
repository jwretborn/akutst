from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from application import app, db
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/akutst"

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()