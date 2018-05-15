class Task:
	def __init__(self, resources, locatedAt):
		self.resources = resources
		self.locatedAt = locatedAt


class Resource:
	def __init__(self):
		pass

		
class Boat(Resource):
	def __init__(self):
		pass
		

class Responder(Resource):
	def __init__(self):
		pass

		
class Paramedic(Resource):
	def __init__(self):
		pass


class AffectedPerson:
	def __init__(self, name, dateOfBirth, priority):
		self.name = name
		self.__dateOfBirth = dateOfBirth
		self.priority = priority


class VulnerablePerson(AffectedPerson):
	def __init__(self, name, dateOfBirth, priority):
		super(name, dateOfBirth, priority).__init__() 


class InjuredPerson(AffectedPerson):
	def __init__(self):
		super(name, dateOfBirth, priority).__init__() 


class Name:
	def __init__(self, firstname, lastname):
		self.__firstname = firstname
		self.__lastname = lastname


class Building:
    def __init__(self, location, impacted, estimatedOccupants, vulnerableOccupants):
        self.location = location
        self.impacted = impacted
        self.estimatedOccupants = estimatedOccupants
		self.vulnerableOccupants = vulnerableOccupants


class Safehouse(Building):
	def __init__(self, location, capacity):
		self.location = location
		self.estimatedOccupants = 0
		self.capacity = capacity

	def getRemainingCapacity(self):
		return self.capacity - self.estimatedOccupants		


class Location:
	def __init__(self, longitude, latitude):
		self.__longitude = longitude
		self.__latitude = latitude
