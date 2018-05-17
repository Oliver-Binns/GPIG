from flask import Flask
from flask_socketio import SocketIO
from gpigapp import Ooda

app = Flask(__name__, instance_relative_config=True)
app.config["SECRET_KEY"] = "cabbage"
app.config.from_object("config")
app.config.from_pyfile("config.py")

# import logging
# logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s][%(levelname)s] - %(funcName)s: %(message)s')

ooda = Ooda.Ooda() #create an instance of the loop at the app level
socketio = SocketIO(app)

import gpigapp.views