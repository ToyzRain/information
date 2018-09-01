from flask_script import Manager
from info import create_app

app = create_app("development")

manager = Manager(app)


@app.route('/')
def index():
    return "hello_world"


if __name__ == '__main__':
    manager.run()
