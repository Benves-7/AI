from config import Configuration
from window import *
from state import *
from buildings import *
from time import perf_counter


class Manager:
	mapHandle = Window.mapHandle
	mapGrid = []

class UnitManager(Manager):
	unitList = []
	
	def Update():
		for unit in UnitManager.unitList:
			unit.Update()

	def addUnit(unit):
		if Window.unitlist == []:
			Window.unitlist = UnitManager.unitList
		UnitManager.unitList.append(unit)

class ResourceManager(Manager):
	needCharcoal = False
	needTrees = False
	lookForTrees = False

	#When an explorer finds a tree its location is saved inside this list
	treeLocations = []
	numKnownTrees = 0

	#this function finds the closest tree to the provided worker and returns its index inside the map
	def getClosestTree(unit):
		currentTile =  BaseGameEntity.map[unit.nodeId]
		distance = len(BaseGameEntity.map)
		closestTile = None
		for tile in ResourceManager.treeLocations:
			if(tile.reservedTrees < len(tile.trees)):
				distanceToTree = abs(tile.x - currentTile.x) + abs(tile.y - currentTile.y)
				if(distanceToTree < distance):
					distance = distanceToTree
					closestTile = tile

		if(distance == len(BaseGameEntity.map)):
			return False
		else:
			closestTile.reservedTrees += 1
			ResourceManager.numKnownTrees -= 1
			return closestTile

	#If a worker isn't doing anything make it search for a tree to cut down
	def Update():
		if TownHall.charcoal <= 200:
		    ResourceManager.needCharcoal = True
		else:
			ResourceManager.needCharcoal = False

		if TownHall.trees <= 400:
			ResourceManager.needTrees = True
		else:
			ResourceManager.needTrees = False

		if len(ResourceManager.treeLocations) <= 0:
			ResourceManager.lookForTrees = True
		else:
			ResourceManager.lookForTrees = False

		if ResourceManager.lookForTrees and EntityManager.explorers < Configuration.config["aiData"]["explorers"]:
			EntityManager.needExplorers = True
		else:
			EntityManager.needExplorers = False

		if ResourceManager.needCharcoal and EntityManager.craftsmen < Configuration.config["aiData"]["craftsman"]:
			EntityManager.needCraftsman = True
		else:
			EntityManager.needCraftsman = False
	
class BuildingManager(Manager):
	kilns = 0
	buildings = {}

	needKiln = False
	canBuildKiln = False

	def addBuilding(building, type):
		BuildingManager.buildings.append(building)
		if(type == "kiln"):
			kilns += 1
	#Checks if conditions are right for building a kiln and if they are it builds one
	def Update():
		if BuildingManager.kilns < Configuration.config["aiData"]["kilns"]:
			BuildingManager.needKiln = True
		else:
			BuildingManager.needKiln = False

		if  TownHall.trees >= Configuration.config["buildings"]["kiln"]["cost"]:
			BuildingManager.canBuildKiln = True
		else:
			BuildingManager.canBuildKiln = False

		if BuildingManager.canBuildKiln and BuildingManager.needKiln and EntityManager.builders < Configuration.config["aiData"]["builders"]:
			EntityManager.needBuilders = True
		else:
			EntityManager.needBuilders = False

class EntityManager(Manager):
	entities = {}
	craftsmen = 0
	builders = 0
	workers = 0
	explorers = 0

	needBuilders = False
	needExplorers = False

	trainingCraftsman = False
	idleCounter = 0

	def addEntity(entity):
		EntityManager.entities[entity.ID] = entity
		if(entity.type == "worker"):
			EntityManager.workers += 1
		if(entity.type == "explorer"):
			EntityManager.explorers += 1
		if(entity.type == "craftsman"):
			EntityManager.craftsmen += 1

	def getEntity(id):
		return EntityManager.entities[id]

	#returns a worker that isnt doing anything
	def getIdle(type= "", profession= ""):
		for id, unit in EntityManager.entities.items():
			if unit.m_currentState == Idle():
				if type == "":
					return unit
				elif type == unit.type and profession == unit.profession:
					return unit
		if perf_counter() - EntityManager.idleCounter > 5:
			EntityManager.idleCounter = perf_counter()
			print("no idle unit found.. " + str(type))
	
	def Update():
		if EntityManager.needExplorers:
			unit = EntityManager.getIdle("worker")
			if unit:
				unit.changeType("explorer")
				EntityManager.explorers += 1

		if EntityManager.needBuilders:
			unit = EntityManager.getIdle("worker")
			if unit:
				unit.changeType("builder")
				EntityManager.builders += 1

		if ResourceManager.needTrees and ResourceManager.numKnownTrees > 0:
			unit = EntityManager.getIdle("worker")
			if unit:
				unit.changeState(WGoToTree())

		return


		#Trains craftsman and explorers
	#	if(EntityManager.builders < int(Configuration.config["aiData"]["builders"])):
	#		for id, ent in EntityManager.entities.items():
	#			if(ent.type == "worker" and ent.m_currentState == state.Waiting() and EntityManager.builders < int(Configuration.config["aiData"]["builders"])):
	#				EntityManager.builders += 1
	#				EntityManager.workers -= 1
	#				#ent.playerCircle.setFill("black")
	#				ent.changeType("craftsman", "builder")
	#
	#			elif(ent.type == "worker" and ent.m_currentState == state.Waiting() and EntityManager.explorers < int(Configuration.config["aiData"]["explorers"])):
	#				EntityManager.explorers += 1
	#				EntityManager.workers -= 1
	#				#ent.playerCircle.setFill("yellow")
	#				ent.changeType("explorer")
	#	#trains a kiln operator if one is needed
	#	for id, building in BuildingManager.buildings.items():
	#		if(building.type == "kiln" and building.complete and not building.populated):
	#			for id, ent in EntityManager.entities.items():
	#				if(ent.type == "worker" and (ent.m_currentState == state.Waiting() or ent.m_currentState == state.WMoveBackToTownHall())):
	#					building.populated = True
	#					ent.playerCircle.setFill("black")
	#					ent.path = BreadthFirst(BaseGameEntity.map, BaseGameEntity.width, BaseGameEntity.height, ent.pointIndex, building.position)
	#					ent.changeType("craftsman", "kilnOperator")
	#					break
	
from basegameentity import *
from pathfinding import BreadthFirst

import random
