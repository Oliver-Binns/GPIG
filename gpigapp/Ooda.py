import Model as modelLib
import Decide as decideLib
from gpigapp import socketio

class Ooda():
    def __init__(self):
        self.model = modelLib.Model(None, None, None, None)
        self.loop = False

    @socketio.on("observe")
    def observe(self):
        # Fetch data
        pass

    @socketio.on("orient")
    def orient(self):
        pass

    @socketio.on("decide")
    def decide(self):
        pass
    
    @socketio.on("act")
    def act(self):
        #push tasks to front end
        pass

    @socketio.on("loopStart")
    def oodaLoop(self):
        self.loop = True

        while(self.loop):
            self.observe()
            self.orient()
            self.decide()
            self.act()
            # update sim/model

    @socketio.on("loopStop")
    def oodaLoopStop(self):
        self.loop = False






ooda = Ooda()