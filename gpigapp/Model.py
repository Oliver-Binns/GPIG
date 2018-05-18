from abc import ABC
from gpigapp import Data

# mje518 I added a class to hold the entire model for the decision making
class Model:
	def __init__(self, tasks, resources, affectedPersons, buildings):
		self.tasks = tasks
		self.resources = resources
		self.affectedPersons = affectedPersons
		self.buildings = buildings
		self.buildingPriorityList = []
		
	@staticmethod
	def loadFakeModel():
		buildings = Data.getBuildings()
		affectedPeople = [b.affectedOccupants for b in buildings if len(b.affectedOccupants)]
		return Model([], [item for sublist in Data.getResources() for item in sublist], affectedPeople, buildings + Data.getSafeHouses())

	def getFrontendModel(self):
		"""splits things up to make it easier to display the model on the frontend"""
		class FrontModel(Model):
			def __init__(self):
				super().__init__(None, None, None, None)
				self.safehouses = None
				self.affectedBuildings = None
		ret = FrontModel()
		ret.tasks = self.tasks
		ret.resources = self.resources
		ret.affectedPersons = self.affectedPersons
		ret.safehouses = [sh for sh in self.buildings if isinstance(sh, Safehouse)]
		ret.affectedBuildings = [ab for ab in self.buildings if isinstance(ab, AffectedBuilding)]
		return ret

class Task:
	def __init__(self, resources, destinations):
		self.resources = resources
		self.destinations = destinations # List of destinations for the task
		self.percentComplete = 0

	def calculatePriority():
		pass

class Resource:
	def __init__(self, location):
		self.location = location
		# vars for movement--
		self.startLocation = location
		self.distanceToTravel = None
		self.directionToTravel = None
		self.moving = False
		#--
		
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
class AffectedBuilding(Building):
	def __init__(self, location, isImpacted, estimatedOccupants, affectedOccupants):
		super().__init__(location, isImpacted, estimatedOccupants, affectedOccupants)
		self.isServiced = False

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
	def y(self):
		return self.__longitude
	def x(self):
		return self.__latitude
	def set(self, x, y):
		self.__longitude = y
		self.__latitude = x
	def get(self):
		return (self.__latitude, self.__longitude)