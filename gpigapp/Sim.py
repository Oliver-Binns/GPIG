from gpigapp import Model as modelLib
import datetime
import time
import numpy

class Sim():
        def __init__(self):
            self.lastTime = datetime.datetime.now()
            self.agentspeed = 4 #speed for agents to move at
            self.printDebugInfo = False

        def __elapsed_ms__(self, start, end):
            return (end-start).total_seconds()*1000


        def simStep(self, model):
            elapsed = self.__elapsed_ms__(self.lastTime, datetime.datetime.now())

            tasksToRemove = []

            for task in model.tasks:
                for resource in task.resources:

                    # resource locations
                    if(resource.moving == False and resource.location != task.destinations[0].location):
                        resource.startLocation = resource.location

                        start = numpy.array((resource.startLocation.x(), resource.startLocation.y()))
                        end = numpy.array((task.destinations[0].location.x(), task.destinations[0].location.y()))

                        resource.distanceToTravel = numpy.linalg.norm(start-end)

                        if(resource.distanceToTravel <=0): #avoid div by 0
                            break
                        resource.directionToTravel = (end - start)/resource.distanceToTravel
                        
                        resource.moving = True
                    else:
                        start = numpy.array((resource.startLocation.x(), resource.startLocation.y()))
                        current = numpy.array((resource.location.x(), resource.location.y()))

                        current += resource.directionToTravel * elapsed * self.agentspeed # calculate new position

                        distanceFromStart = numpy.linalg.norm(start-current)
                        if(distanceFromStart >= resource.distanceToTravel): # if we're at or past the destination, snap to
                            resource.location.set(task.destinations[0].location.x(), task.destinations[0].location.y())
                            resource.moving = False
                            self.customPrint("resource at dest")
                        else:
                            resource.location.set(current[0], current[1]) # update resource object location

                # update destination if all resources in task are there
                if(all(not res.moving for res in task.resources)): 
                    task.destinations.pop(0)
                    self.customPrint("newDest")

                    if(len(task.destinations) == 0): #task finished
                        self.customPrint("task finished")
                        tasksToRemove.append(task)
                        
            # Remove the finished tasks          
            if(len(tasksToRemove)>0):
                for task in tasksToRemove:
                    resToReallocate = task.resources
                    model.resources+=resToReallocate #add resources to resources list
                    model.tasks.remove(task) #remove task

         
        def customPrint(self, printVal):
            if(self.printDebugInfo):
                print(printVal)