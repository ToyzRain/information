import logging
from flask import session, current_app
from flask_script import Manager
from info import create_app

app = create_app("development")
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
