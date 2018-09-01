import logging
from flask import session, current_app
from flask_script import Manager
from info import create_app
from flask_migrate import MigrateCommand, Migrate
from info import db

app = create_app("development")
manager = Manager(app)

Migrate(app, db)
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()
