from abc import ABC
from gpigapp import Data
import base64
from functools import reduce
import operator

# mje518 I added a class to hold the entire model for the decision making
class Model:
	def __init__(self, tasks, resources, affectedPersons, buildings):
		self.tasks = tasks
		self.resources = resources
		self.assignedResources = []
		self.affectedPersons = affectedPersons
		self.buildings = buildings
		self.buildingPriorityList = []
		
	@staticmethod
	def loadFakeModel():
		return Data.getPopulatedModel()

	def getFrontendModel(self):
		"""Splits things up to make it easier to display the model on the frontend
		This is horrible and you probably shouldn't read it... but it made my life easier"""
		class FrontModel(Model):
			def __init__(self, m):
				super().__init__(m.tasks, m.resources, m.affectedPersons, m.buildings)
				self.safehouses = []
				self.affectedBuildings = []

				for b in m.buildings:
					if isinstance(b, Safehouse):
						self.safehouses.append(b)
					elif isinstance(b, AffectedBuilding):
						self.affectedBuildings.append(b)
					else:
						raise Exception("Don't know how to display type {} on frontend".format(type(b)))

				self.boats = []
				self.assignedBoats = 0
				self.responders = []
				self.assignedResponders = 0
				self.paramedics = []
				self.assignedParamedics = 0

				for r in (m.resources):
					if isinstance(r, Boat):
						self.boats.append(r)
					elif isinstance(r, Responder):
						self.responders.append(r)
					elif isinstance(r, Paramedic):
						self.paramedics.append(r)
					else:
						raise Exception("Don't know how to display type {} on frontend".format(type(b)))

				for r in (m.assignedResources):
					if isinstance(r, Boat):
						self.boats.append(r)
						self.assignedBoats += 1
					elif isinstance(r, Responder):
						self.responders.append(r)
						self.assignedResponders += 1
					elif isinstance(r, Paramedic):
						self.paramedics.append(r)
						self.assignedParamedics += 1
					else:
						raise Exception("Don't know how to display type {} on frontend".format(type(b)))

				self.assignedBoats = self.assignedBoats/len(self.boats)*100
				self.assignedResponders = self.assignedResponders/len(self.responders)*100
				self.assignedParamedics = self.assignedParamedics/len(self.paramedics)*100
				self.remainingRestCentreSpace = 100.0 - sum([x.getRemainingCapacity() for x in self.safehouses])/sum([x.capacity for x in self.safehouses])*100

				with open("data/overlay.png", "rb") as imageFile:
					b64img = base64.b64encode(imageFile.read())
					self.flood = b64img.decode()

		return FrontModel(self)

class Task:
	def __init__(self, uuid, name, resources, destinations, expectedPeople):
		self.ID = uuid
		self.name = name
		self.resources = resources
		self.destinations = destinations # List of destinations for the task
		self.expectedPeople = expectedPeople
		self.percentComplete = 0
		self.active = False


class Resource:
	def __init__(self, location):
		self.location = location
		# vars for movement--
		self.startLocation = Location(self.location.x(), self.location.y())
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
		self.taskAssigned = False

class Safehouse(Building):
	def __init__(self, location, isImpacted, capacity):
		super().__init__(location, isImpacted, 0, None)
		self.capacity = capacity
		self.maxCapacity = capacity

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