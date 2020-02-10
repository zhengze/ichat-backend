from flask import Flask
from flask_cors import CORS
from flask_script import Manager, Server
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, send
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import config
from .database import db
from .resources import chat_bp, socketio


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name or 'default'])
    CORS(app)
    jwt = JWTManager()
    jwt.init_app(app)
    db.init_app(app)
    socketio.init_app(app)

    app.register_blueprint(chat_bp)

    return app
