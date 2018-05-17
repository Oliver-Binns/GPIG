from gpigapp import Model as modelLib#, Decide as decideLib
from flask_socketio import emit
import json

class Ooda():
    def __init__(self):
        self.model = modelLib.Model(None, None, None, None)
        self.loop = False

    def observe(self):
        # Fetch data
        pass

    def orient(self):
        pass

    def decide(self):
        pass
    
    def act(self):
        return self.model.tasks

    def oodaLoop(self):
        self.loop = True

        while(self.loop):
            self.observe()
            self.orient()
            self.decide()
            self.act()
            # update sim/model

    def oodaLoopStop(self):
        self.loop = False