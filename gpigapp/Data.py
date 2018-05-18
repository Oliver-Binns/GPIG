from gpigapp import Model
import csv

# Paths to our fictional DBs
resourcesPath = "data/mock_db/resources.csv"
buildingsPath = "data/mock_db/affectedBuildings.csv"
safeHousesPath = "data/mock_db/safeHouses.csv"
peoplePath = "data/mock_db/people.csv"

def getResources():
    """
    Returns a list of resources.
    """
    resources = []
    
    with open(resourcesPath, 'r') as re:
        res = csv.reader(re, dialect='excel')
        
        # Skip header row
        next(res)
        
        for row in res:
            location = Model.Location(float(row[1]), float(row[2])) 
            
            if row[3] == "Boat":
                resources.append( Model.Boat(location, int(row[4])) )
                continue
            if row[3] == "Responder":
                resources.append( Model.Responder(location) )
                continue
            if row[3] == "Paramedic":
                resources.append( Model.Paramedic(location) )

    return resources

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
    affected = getAffectedPersons()
    buildings = []

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

def getAffectedPersons():
    """
    Returns a dict of affected people (a dict to be able to mathc them with buildings)
    """
    affected = {}

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

    return affected

def getPopulatedModel():
    tasks = []
    resources = getResources()
    affectedPersons = getAffectedPersons()
    buildings = getBuildings() + getSafeHouses() 

    return Model.Model( tasks, resources, affectedPersons, buildings )
