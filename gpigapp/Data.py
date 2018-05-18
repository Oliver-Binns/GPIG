from gpigapp import Model 
import csv

# Paths to our fictional DBs
resourcesPath = "data/mock_db/resources.csv"
buildingsPath = "data/mock_db/affectedBuildings.csv"
safeHousesPath = "data/mock_db/safeHouses.csv"
peoplePath = "data/mock_db/people.csv"

def getResources():
    """
    Returns a list of lists of resources [Boats, Responders, Paramedics]
    """
    boats = []
    paramedics = []
    responders = []
    with open(resourcesPath, 'r') as res:
        resources = csv.reader(res, dialect='excel')
        
        # Skip header row
        next(resources)
        
        for row in resources:
            location = Model.Location(float(row[1]), float(row[2])) 
            
            if row[3] == "Boat":
                boats.append( Model.Boat(location, int(row[4])) )
                continue
            if row[3] == "Responder":
                responders.append( Model.Responder(location) )
                continue
            if row[3] == "Paramedic":
                paramedics.append( Model.Paramedic(location) )

    return [boats, responders, paramedics]

def getSafeHouses():
    """
    Returns a list of safe houses
    """
    safeHouses = []
    with open(safeHousesPath, 'r') as sh:
        safe = csv.reader(sh, dialect='excel')
        
        # Skip header row
        next(safe)
        
        for row in safe:
            location = Model.Location(float(row[1]), float(row[2]))
            impacted = True
            if row[3] == 0:
                impacted = False
            capacity = int(row[5])    
            safeHouses.append( Model.Safehouse(location, impacted, capacity))

    return safeHouses

def getBuildings():
    """
    Returns a list of possibly affected buildings
    """
    affected = {}
    buildings = []

    with open(peoplePath, 'r') as pep:
        people = csv.reader(pep, dialect='excel')
        next(people)

        for row in people:
            name = Model.Name(row[3], row[4])
            dob = row[5]
            priority = int(row[7])
            if row[6] == "Affected":
                affected[int(row[0])] = Model.AffectedPerson(name, dob, priority)
                continue
            if row[6] == "Vulnerable":
                affected[int(row[0])] = Model.VulnerablePerson(name, dob, priority)
                continue
            if row[6] == "Injured":
                affected[int(row[0])] = Model.InjuredPerson(name, dob, priority)
                continue

    with open(buildingsPath, 'r') as ab:
        affectedBuildings = csv.reader(ab, dialect='excel')
        
        # Skip header row
        next(affectedBuildings)
        
        for row in affectedBuildings:
            location = Model.Location(float(row[1]), float(row[2]))
            impacted = True
            if row[3] == 0:
                impacted = False
            estimatedOccupants = int(row[5])   
            occupants = row[7].split(',')

            if occupants[0] != '':
                affectedOccupants = [affected[x] for x in map(int, occupants)] 
            else:
                affectedOccupants = []

            buildings.append( Model.AffectedBuilding(location, impacted, estimatedOccupants, affectedOccupants))

    return buildings
