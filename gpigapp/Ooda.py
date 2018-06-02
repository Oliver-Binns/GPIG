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

        if self.model.buildings.count<5:
            # Fetch new data
            # Add new data if not None
        pass

    def orient(self):
        pass

    def decide(self):
        decideLib.decide(self.model)
    
    def act(self):
        return self.model.getFrontendModel()

    def oodaLoop(self):
        self.loop = False

        while(self.loop):
            self.observe()
            self.orient()
            self.decide()
            self.act()
            self.sim.simStep(self.model)# update sim/model
            time.sleep(0.01)

    def oodaLoopStop(self):
        self.loop = False

    def stepSim(self):
        self.sim.simStep(self.model)# update sim/model
        return self.model.getFrontendModel()

    def acceptTask(self, uid):
        taskToAccept = next(task for task in self.model.tasks if task.ID == uid)
        taskToAccept.active = True

    def rejectTask(self,uid):
        taskToRemove = next(task for task in self.model.tasks if task.ID == uid)
        self.sim.removeTask(self.model, taskToRemove)

    def changeSimAgentSpeed(self, speed):
        self.sim.agentspeed = speed

    def resetSim():
        self.model = modelLib.Model.loadFakeModel()