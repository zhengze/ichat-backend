import os
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate
from dotenv import load_dotenv, find_dotenv
#from gevent.pywsgi import WSGIServer
#from geventwebsocket.handler import WebSocketHandler
from chat import create_app, db
from chat.resources import socketio


dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
load_dotenv(dotenv_path=dotenv_path)
load_dotenv(find_dotenv())
app = create_app(os.getenv('FLASK_CONFIG'))
Migrate(app, db)
manager = Manager(app)
RUN_HOST = os.getenv('FLASK_RUN_HOST')
RUN_PORT = int(os.getenv('FLASK_RUN_PORT'))
#server = Server(host=RUN_HOST, port=RUN_PORT)
#manager.add_command('runserver', server)
socket_server = socketio.run(app=app, host=RUN_HOST, port=RUN_PORT)
manager.add_command('runserver', socket_server)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
    #http_server = WSGIServer((RUN_HOST, RUN_PORT), app, handler_class=WebSocketHandler)
    # http_server.serve_forever()
    #socketio.run(app, host='0.0.0.0', port=RUN_PORT)
