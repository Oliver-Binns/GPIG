from gpigapp import Model as modelLib

def decide(Model):
    safeHouses = [safehouse for safehouse in Model.buildings if isinstance(safehouse, modelLib.Safehouse)]
    affectedBuildings = [affectedBuilding for affectedBuilding in Model.buildings if isinstance(affectedBuilding, modelLib.AffectedBuilding)]

    #Adding any unserviced buildings to the building priority list with their calculated priority
    for building in affectedBuildings:
        if(building.isServiced == False and not any(building in subList for subList in Model.buildingPriorityList)):
            priority = calcPriority(building, safeHouses)
            Model.buildingPriorityList.append((priority, building))

    #Sort the list into priority order (bigger number is higher priority)
    Model.buildingPriorityList = sorted(Model.buildingPriorityList,reverse=True, key=lambda tup: tup[0])

    keepAssigning = True
    bpListIndex = 0
    #keep creating task and assigning them resources until there are not enough resources for the next task
    while(keepAssigning):
        task = createTask(Model.buildings[bpListIndex], Model.resources, getClosestSafehouse(Model.buildings[bpListIndex], safeHouses)[0])
        if(task is not None):
            for resource in task.resources:
                Model.resources.remove(resource)
            Model.tasks.append(task)
            bpListIndex += 1
        else:
            keepAssigning = False

##
#Calculates the priority of a building based on its occupants and location
#Assignes a high priority for affected people, lots of people and buildings far from the safehouses
#Returns an int
def calcPriority(building, safehouses):
    priority = 0
    
    for occupant in building.affectedOccupants:
        priority += occupant.priority

    priority += building.estimatedOccupants
    
    priority += 1*getClosestSafehouse(building, safehouses)[1]

    return priority

##
#Gets the safehouse closest to a building
#Used for calculating a building priority
#Returns a tuple of a safehouse and the distance
def getClosestSafehouse(building, safehouses):
    locBuild = building.location.get()
    minDist = -1
    for safehouse in safehouses:
        locSafe = safehouse.location.get()
        dist = ((locBuild[0] - locSafe[0])**2 + (locBuild[1] - locSafe[1])**2)**0.5
        if(dist < minDist or minDist == -1):
            minDist = dist
            bestSafe = safehouse
    return (bestSafe, minDist)


def createTask(building, resources, closestSafehouse):

    assignedResources = []

    totalBoatCapacity = 0
    resourcesIterator = iter(resources)
    while(totalBoatCapacity < building.estimatedOccupants):
        nextBoat = next((boat for boat in resourcesIterator if isinstance(boat, modelLib.Boat)), None)
        if(nextBoat is not None):
            totalBoatCapacity += boat.capacity
            assignedResources.add(boat)
        else:
            return None

    resourcesIterator = iter(resources)
    for affOcc in building.affectedOccupants:
        nextParamedic = next((paramedic for paramedic in resourcesIterator if isinstance(paramedic, modelLib.Paramedic)), None)
        if(nextParamedic is not None):
            assignedResources.add(nextParamedic)
        else:
            return None

    return Task(assignedResources, [building, closestSafehouse])










    