import os
import flask
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from dotenv import load_dotenv, find_dotenv
from chat import create_app, db, models
from chat.resources import socketio


dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
load_dotenv(dotenv_path=dotenv_path)
load_dotenv(find_dotenv())
app = create_app(os.getenv('FLASK_CONFIG'))
Migrate(app, db)
manager = Manager(app)
RUN_HOST = os.getenv('FLASK_RUN_HOST')
RUN_PORT = int(os.getenv('FLASK_RUN_PORT'))
server = Server(host=RUN_HOST, port=RUN_PORT)
#manager.add_command('runserver', server)
#server = socketio.run(app=app, host=RUN_HOST, port=RUN_PORT)
manager.add_command('runserver', server)
manager.add_command('db', MigrateCommand)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, models=models)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def run():
    #socketio.run(flask.current_app, host=RUN_HOST, port=RUN_PORT, use_reloader=False)
    socketio.run(app, host=RUN_HOST, port=RUN_PORT)


if __name__ == '__main__':
    manager.run()
    #socketio.run(app, host=RUN_HOST, port=RUN_PORT)
