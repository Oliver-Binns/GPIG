#!flask/bin/python
from gpigapp import socketio, app, callbacks

if __name__ == '__main__':
    socketio.run(app)