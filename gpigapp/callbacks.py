from gpigapp import socketio
from flask_socketio import emit
import base64
import numpy
import cv2

@socketio.on("loadBeforeImage")
def loadBeforeImage(img):
    if img == {}:
        #use Brookshire Harvey image as default
        with open("data/harvey-brookshire-before.jpg", "rb") as imageFile:
            b64img = base64.b64encode(imageFile.read())
            emit("displayBeforeImage", b64img.decode())
    else:
        print("TODO: store image on server, then update client with displayBeforeImage")

@socketio.on("loadAfterImage")
def loadAfterImage(img):
    if img == {}:
        #use Brookshire Harvey image as default
        with open("data/harvey-brookshire-after.jpg", "rb") as imageFile:
            b64img = base64.b64encode(imageFile.read())
            emit("displayAfterImage", b64img.decode())
    else:
        print("TODO: store image on server, then update client with displayAfterImage")