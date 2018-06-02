from gpigapp import Model as modelLib
from gpigapp import Decide as decideLib
from gpigapp import Sim as simLib
from flask_socketio import emit
import json
import time

class Ooda():
    def __init__(self):
        self.model, self.additional = modelLib.Model.loadFakeModel()
        self.loop = False
        self.sim = simLib.Sim()

    def observe(self):

        if len(self.model.buildings) < 5:
            # Fetch new data
            
            # Call additional.getMoreData(samples) where samples is the number of data 
            # points you want to add. Can be 0. You could do a random here so it looks more
            # dynamic. It returns None when no more builidngs left or when called with 0.

            buildings, persons = self.additional.getMoreData(2)

            # Add new data if not None
            if buildings != None:
                self.model.buildings += buildings
                self.model.affectedPersons += persons

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