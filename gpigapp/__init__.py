from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, instance_relative_config=True)
app.config["SECRET_KEY"] = "cabbage"
app.config.from_object("config")
app.config.from_pyfile("config.py")

import logging
logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s][%(levelname)s] - %(funcName)s: %(message)s')

socketio = SocketIO(app)

import gpigapp.views