from gpigapp import Model as modelLib
from gpigapp import Decide as decideLib
from gpigapp import Sim as simLib
from flask_socketio import emit
import json
import time

class Ooda():
    def __init__(self):
        self.model = modelLib.Model.loadFakeModel()
        self.loop = False
        self.sim = simLib.Sim()

    def observe(self):
        # Fetch data
        pass

    def orient(self):
        pass

    def decide(self):
        decideLib.decide(self.model)
    
    def act(self):
        return self.model.getFrontendModel()

    def oodaLoop(self):
        self.loop = True

        while(self.loop):
            self.observe()
            self.orient()
            self.decide()
            self.act()
            self.sim.simStep(self.model)# update sim/model
            time.sleep(0.01)

    def oodaLoopStop(self):
        self.loop = False