from gpigapp import socketio, ooda
from gpigapp import Ooda
from flask_socketio import emit
import base64
import numpy
import cv2
import json_tricks

@socketio.on("loadBeforeImage")
def loadBeforeImage(img):
    if img == {}:
        #use Wharton Harvey image as default
        with open("data/harvey-wharton-before.jpg", "rb") as imageFile:
            b64img = base64.b64encode(imageFile.read())
            emit("displayBeforeImage", b64img.decode())
    else:
        print("TODO: store image on server, then update client with displayBeforeImage")

@socketio.on("loadAfterImage")
def loadAfterImage(img):
    if img == {}:
        #use Wharton Harvey image as default
        with open("data/harvey-wharton-after.jpg", "rb") as imageFile:
            b64img = base64.b64encode(imageFile.read())
            emit("displayAfterImage", b64img.decode())
    else:
        print("TODO: store image on server, then update client with displayAfterImage")

@socketio.on("loadMapImage")
def loadAfterImage(img):
    if img == {}:
        #use Wharton Harvey image as default
        with open("data/harvey-wharton-map.jpg", "rb") as imageFile:
            b64img = base64.b64encode(imageFile.read())
            emit("displayMapImage", b64img.decode())
    else:
        print("TODO: store image on server, then update client with displayMapImage")

@socketio.on("observe")
def observe():
    ooda.observe()

@socketio.on("decide")
def decide():
    ooda.decide()

@socketio.on("act")
def act():
    socketio.emit("updateModel", json_tricks.dumps(ooda.act(), primitives=True))

@socketio.on("stepSim")
def stepSim():
    socketio.emit("updateModel", json_tricks.dumps(ooda.stepSim(), primitives=True))

@socketio.on("acceptTask")
def acceptTask(uid):
    ooda.acceptTask(uid)

@socketio.on("rejectTask")
def rejectTask(uid):
    ooda.rejectTask(uid)

@socketio.on("changeSpeed")
def changespeed(speed):
    ooda.changeSimAgentSpeed(speed)

@socketio.on("resetSim")
def resetSim():
    ooda.resetSim()
