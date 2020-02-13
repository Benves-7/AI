
class Manager:
	map = []

class ExplorerManager(Manager):
	pass

class ResourceManager(Manager):
	charcoal = 0
	trees = 0

	#When an explorer finds a tree its location is saved inside this list
	treeLocations = []
	#this function finds the closest tree to the provided worker and returns its index inside the map
	def getClosestTree(worker, currentNode):
		distance = len(BaseGameEntity.map)
		closestNode = None
		for node in ResourceManager.treeLocations:
			if(BaseGameEntity.map[node].reservedTrees < 5):
				distanceToTree = abs(BaseGameEntity.map[node].x - BaseGameEntity.map[currentNode].x) + abs(BaseGameEntity.map[node].y - BaseGameEntity.map[currentNode].y)
				if(distanceToTree < distance):
					distance = distanceToTree
					closestNode = node
		if(distance == len(BaseGameEntity.map)):
			return False
		else:
			#BaseGameEntity.map[closestNode].reservedTrees += 1
			return closestNode
	#If a worker isn't doing anything make it search for a tree to cut down
	def Update():
		return
		for id, ent in EntityManager.entities.items():
			if(ent.type == "worker" and ent.path ==  None and len(ResourceManager.treeLocations) != 0):
				ent.changeState(state.WGoToTree())

class BuildingManager(Manager):
	kilns = 0

	buildings = {}

	def addBuilding(building, type):
		BuildingManager.buildings.append(building)
		if(type == "kiln"):
			kilns += 1
	#Checks if conditions are right for building a kiln and if they are it builds one
	def Update():
		return
		#Build kilns
		if(ResourceManager.trees > 10 and EntityManager.builders > 0 and BuildingManager.kilns < Configuration.config["aiData"]["kilns"]):
			buildingPos = 0
			while(1):
				#position of the kiln
				xRand = random.randint(-10, 10)
				yRand = random.randint(-10,10)
				buildingPos = Configuration.config["buildings"]["townHall"]["position"] + (xRand + BaseGameEntity.width * yRand)
				if(not BaseGameEntity.map[buildingPos].fogOfWar and BaseGameEntity.map[buildingPos].building == None and BaseGameEntity.map[buildingPos].moveSpeed == 1 and BaseGameEntity.map[buildingPos].isWalkable):
					builder =  EntityManager.getBuilder()
					if(builder != False):
						BaseGameEntity.map[buildingPos].building = Kiln(buildingPos)
						BuildingManager.buildings[buildingPos] = BaseGameEntity.map[buildingPos].building
						builder.working = True
						builder.path = BreadthFirst(BaseGameEntity.map, BaseGameEntity.width, BaseGameEntity.height, builder.pointIndex, buildingPos)
						circle = Circle(BaseGameEntity.map[buildingPos].center, 5)
						circle.setFill("White")
						circle.draw(BaseGameEntity.windowClass.window)
						BuildingManager.kilns +=1
						builder.changeState(state.BBuildBuilding())
						break
					break
		
		


class EntityManager:

	entities = {}
	craftsmen = 0
	builders = 0

	workers = 0
	explorers = 0
	trainingCraftsman = False
	#numExplorers = Configuration.config["aiData"]["numExplorers"]
		

	def addEntity(entity):
		#numExplorers = Configuration.config["aiData"]["numExplorers"]
		EntityManager.entities[entity.ID] = entity
		if(entity.type == "worker"):
			EntityManager.workers += 1
		if(entity.type == "explorer"):
			EntityManager.explorers += 1
		if(entity.type == "craftsman"):
			EntityManager.craftsmen += 1


	def getEntity(id):
		return EntityManager.entities[id]
	#returns a worker that isnt doing anythin
	def getBuilder():
		for id, ent in EntityManager.entities.items():
			if(ent.type == "craftsman" and ent.profession == "builder" and not ent.working):
				print("working")
				return ent
			else:
				print("not working")
				return False
	


	def Update():
		return
		#Trains craftsman and explorers
		if(EntityManager.builders < int(Configuration.config["aiData"]["builders"])):
			for id, ent in EntityManager.entities.items():
				if(ent.type == "worker" and ent.m_currentState == state.Waiting() and EntityManager.builders < int(Configuration.config["aiData"]["builders"])):
					EntityManager.builders += 1
					EntityManager.workers -= 1
					#ent.playerCircle.setFill("black")
					ent.changeType("craftsman", "builder")

				elif(ent.type == "worker" and ent.m_currentState == state.Waiting() and EntityManager.explorers < int(Configuration.config["aiData"]["explorers"])):
					EntityManager.explorers += 1
					EntityManager.workers -= 1
					#ent.playerCircle.setFill("yellow")
					ent.changeType("explorer")
		#trains a kiln operator if one is needed
		for id, building in BuildingManager.buildings.items():
			if(building.type == "kiln" and building.complete and not building.populated):
				for id, ent in EntityManager.entities.items():
					if(ent.type == "worker" and (ent.m_currentState == state.Waiting() or ent.m_currentState == state.WMoveBackToTownHall())):
						building.populated = True
						ent.playerCircle.setFill("black")
						ent.path = BreadthFirst(BaseGameEntity.map, BaseGameEntity.width, BaseGameEntity.height, ent.pointIndex, building.position)
						ent.changeType("craftsman", "kilnOperator")
						break

from basegameentity import *
from config import Configuration
from pathfinding import BreadthFirst
import state
import random
from buildings import *