from gpigapp import Model as modelLib
import uuid
import random

def decide(Model):
    safeHouses = [safehouse for safehouse in Model.buildings if isinstance(safehouse, modelLib.Safehouse)]
    affectedBuildings = [affectedBuilding for affectedBuilding in Model.buildings if isinstance(affectedBuilding, modelLib.AffectedBuilding)]

    #Adding any unserviced buildings to the building priority list with their calculated priority
    for building in affectedBuildings:
        if(not any(building in subList for subList in Model.buildingPriorityList)):
            if building.estimatedOccupants == 0 and len(building.affectedOccupants) == 0:
                Model.buildings.remove(building)
                
            priority = calcPriority(building, safeHouses)
            Model.buildingPriorityList.append((priority, building))

    #Sort the list into priority order (bigger number is higher priority)
    Model.buildingPriorityList = sorted(Model.buildingPriorityList,reverse=True, key=lambda tup: tup[0])

    keepAssigning = True
    bpListIndex = 0
    #keep creating task and assigning them resources until there are not enough resources for the next task
    while(keepAssigning and bpListIndex < len(Model.buildingPriorityList)):
        building = Model.buildingPriorityList[bpListIndex][1]
        if building.taskAssigned == True or Model.buildingPriorityList[bpListIndex][0] == 0:
            bpListIndex += 1
            continue
        task = createTask(building, Model.resources, getClosestSafehouse(building, safeHouses)[0])
        if(task is not None):
            for resource in task.resources:
                Model.assignedResources.append(resource)
                Model.resources.remove(resource)
                building.taskAssigned = True
            Model.tasks.append(task)
            bpListIndex += 1
        else:
            keepAssigning = False
    #TODO: prevent creating tasks for buildings that currently have a task assigned, we currently dont remove them from the building priority list, atm if we did remove, they'd just get added back in

##
#Calculates the priority of a building based on its occupants and location
#Assignes a high priority for affected people, lots of people and buildings far from the safehouses
#Returns an int
def calcPriority(building, safehouses):
    priority = 0

    if building.estimatedOccupants == 0 and len(building.affectedOccupants) == 0:
        return 0

    priority += building.estimatedOccupants
    
    for occupant in building.affectedOccupants:
        priority += occupant.priority
    
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
            totalBoatCapacity += nextBoat.capacity
            assignedResources.append(nextBoat)
        else:
            return None

    resourcesIterator = iter(resources)
    for affOcc in building.affectedOccupants:
        nextParamedic = next((paramedic for paramedic in resourcesIterator if isinstance(paramedic, modelLib.Paramedic)), None)
        if(nextParamedic is not None):
            assignedResources.append(nextParamedic)
        else:
            return None

    return modelLib.Task(str(uuid.uuid4()), generateName(), assignedResources, [building, closestSafehouse], building.estimatedOccupants)

def generateName():
    taskNouns = ["Apple", "Apricot", "Avocado", "Avocado", "Banana", "Bilberry", "Blackberry", "Blackcurrant", "Blood orange", 
    "Blueberry", "Boysenberry", "Buddha's hand", "Cantaloupe", "Cherimoya", "Cherry", "Chico fruit", "Chili pepper", 
    "Clementine", "Cloudberry", "Coconut", "Corn kernel", "Crab apples", "Cranberry", "Cucumber", "Cucumber", "Currant",
    "Custard apple", "Damson", "Date", "Dragonfruit", "Durian", "Eggplant", "Elderberry", "Feijoa", "Fig", "Goji berry",
    "Gooseberry", "Grape", "Grapefruit", "Guava", "Honeyberry", "Honeydew", "Huckleberry", "Jabuticaba", "Jackfruit",
    "Jambul", "Jujube", "Juniper berry", "Kiwano", "Kiwifruit", "Kumquat", "Lemon", "Lime", "Longan", "Loquat",
    "Lychee", "Mandarine", "Mango", "Mangosteen", "Marionberry", "Melon", "Miracle fruit", "Mulberry", "Nance",
    "Nectarine", "Olive", "Olive", "Orange", "Papaya", "Passionfruit", "Pea", "Peach", "Pear", "Persimmon", 
    "Pineapple", "Plantain", "Plum", "Plumcot", "Pomegranate", "Pomelo", "Prune", "Pumpkin", "Purple mangosteen",
    "Quince", "Raisin", "Rambutan", "Raspberry", "Redcurrant", "Salak", "Salal berry", "Salmonberry", "Satsuma",
    "Soursop", "Squash", "Star fruit", "Strawberry", "Tamarillo", "Tamarind", "Tangerine", "Tomato", "Ugli fruit",
    "Watermelon", "Yuzu",]

    return "Task "+random.choice(taskNouns)+"-"+random.choice(taskNouns)







    