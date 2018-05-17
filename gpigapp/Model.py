from abc import ABC

# mje518 I added a class to hold the entire model for the decision making
class Model:
	def __init__(self, tasks, resources, affectedPersons, buildings):
		self.tasks = tasks
		self.resources = resources
		self.affectedPersons = affectedPersons
		self.buildings = buildings
		self.buildingPriorityList = None
		

class Task:
	def __init__(self, resources, locatedAt):
		self.resources = resources
		self.locatedAt = locatedAt
		self.percentComplete = 0

	def calculatePriority()
		pass

class Resource:
	def __init__(self, location):
		self.location = location
		
class Boat(Resource):		
	def __init__(self, locatedAt, capacity):
		self.capacity = capacity
		super().__init__(locatedAt)
		
		

class Responder(Resource):
	def __init__(self, locatedAt):
		super().__init__(locatedAt)
		

		
class Paramedic(Resource):
	def __init__(self, locatedAt):
		super().__init__(locatedAt)
		


class AffectedPerson:
	def __init__(self, name, dateOfBirth, priority):
		self.name = name
		self.__dateOfBirth = dateOfBirth
		self.priority = priority


class VulnerablePerson(AffectedPerson):
	def __init__(self, name, dateOfBirth, priority):
		super().__init__(name, dateOfBirth, priority)


class InjuredPerson(AffectedPerson):
	def __init__(self, name, dateOfBirth, priority):
		super().__init__(name, dateOfBirth, priority)


class Name:
	def __init__(self, firstname, lastname):
		self.__firstname = firstname
		self.__lastname = lastname


class Building(ABC):
	def __init__(self, location, isImpacted, estimatedOccupants, affectedOccupants):
		self.location = location
		self.isImpacted = isImpacted
		self.estimatedOccupants = estimatedOccupants
		self.affectedOccupants = affectedOccupants

#We have created another subclass for affected buildings
class affectedBuilding(Building):
	def __init__(self, location, isImpacted, estimatedOccupants, affectedOccupants):
		super.__init__(location, isImpacted, estimatedOccupants, affectedOccupants)

class Safehouse(Building):
	def __init__(self, location, isImpacted, capacity):
		super().__init__(location, isImpacted, 0, None)
		self.capacity = capacity

	def getRemainingCapacity(self):
		return self.capacity - self.estimatedOccupants		


class Location:
	def __init__(self, longitude, latitude):
		self.__longitude = longitude
		self.__latitude = latitude
