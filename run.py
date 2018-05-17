#!flask/bin/python
from gpigapp import socketio, app, callbacks, Ooda

if __name__ == '__main__':
    socketio.run(app)