from config import *
from managers import *
from random import randint, uniform
from pathfinding import BreadthFirst

#Created the map object and fills it with Nodes
class MapHandle:
	width = 0
	heigth = 0
	grid = []
	nextID = 0
	removedID = []

	def createGrid(self, lineString):
		MapHandle.width = self.width = len(list(lineString[0]))
		parameters = Configuration.config["nodeTypes"]

		for line in lineString:
			lineList = list(line)
			MapHandle.heigth = self.heigth = self.heigth + 1
			for character in lineList:
				#Each nodes parameters are from the config file
				if character == "B":
					border = parameters["border"]
					self.grid.append(Node("border", border["trees"], bool(border["walkable"]), border["color"], self.nextID, border["mSpeed"], border["fogOfWar"]))
				elif character == "M":#Mountain
					mountain = parameters["mountain"]
					self.grid.append(Node("mountain", mountain["trees"], bool(mountain["walkable"]), mountain["color"], self.nextID, mountain["mSpeed"], mountain["fogOfWar"]))
				elif(character == "G"):#Ground
					ground = parameters["ground"]
					self.grid.append(Node("ground", ground["trees"], bool(ground["walkable"]), ground["color"], self.nextID, ground["mSpeed"], ground["fogOfWar"]))
				elif(character == "T"):#Tree
					tree = parameters["tree"]
					self.grid.append(Node("tree", tree["trees"], bool(tree["walkable"]), tree["color"], self.nextID, tree["mSpeed"], tree["fogOfWar"]))
				elif(character == "S"):#Swamp
					swamp = parameters["swamp"]
					self.grid.append(Node("swamp", swamp["trees"], bool(swamp["walkable"]), swamp["color"], self.nextID, swamp["mSpeed"], swamp["fogOfWar"]))
				elif(character == "W"):#Water
					water = parameters["water"]
					self.grid.append(Node("water", water["trees"], bool(water["walkable"]), water["color"], self.nextID, water["mSpeed"], water["fogOfWar"]))
				self.nextID += 1
		return self.grid

	def addTrees(self, windowHandle, mapHandle): #windowWidth, windowHeight, mapWidth, mapHeight):
		for node in self.grid:
			if(node.isTree):
				for x in range(0,5):
					node.trees.append(TreeNode(node, windowHandle, mapHandle))  #windowWidth, windowHeight, mapWidth, mapHeight))

	def getNeighbours(self, id):
		map = self.grid
		width = self.width
		neighbours = []
		if(map[id - 1].isWalkable): #Left of
			neighbours.append(id-1)
		if(map[id - width].isWalkable): #Above
			neighbours.append(id - width)
		if(map[id + 1].isWalkable): #Right of
			neighbours.append(id+1)
		if(map[id + width].isWalkable): #Below
			neighbours.append(id + width)

		return neighbours
	def getAllNeighbours(self, id): #returns a list of all neighbours vertical, horizontal and diagonal
		map = MapHandle.grid
		width = MapHandle.width
		neighbours = []
		top = False
		bottom = False
		right = False
		left = False
		if(map[id - width].isWalkable == True): #Above
			neighbours.append(id - width)
			top = True
		if(map[id + 1].isWalkable == True): #Right of
			neighbours.append(id+1)
			right = True
		if(map[id - 1].isWalkable == True): #Left of
			neighbours.append(id-1)
			left = True
		if(map[id + width].isWalkable == True): #Below
			neighbours.append(id + width)
			bottom = True
		if(map[id - width + 1].isWalkable and top and right): #Above right
			neighbours.append(id - width + 1)
		if(map[id - width - 1].isWalkable and top and left): #Above left
			neighbours.append(id - width - 1)
		if(map[id + width + 1].isWalkable and bottom and right): #Below right
			neighbours.append(id + width + 1)
		if(map[id + width - 1].isWalkable and bottom and left): #Below left
			neighbours.append(id + width - 1)

		return neighbours 

	def findExploration(self, unit):
		unit.startNode = self.grid[unit.nodeId]
		unit.endNode = self.getRandomNode(unit.nodeId)
		if unit.endNode:
			return self.searchForPath(unit.startNode, unit.endNode)
		else:
			return False

	def getRandomNode(self, id): #return random node ID within range..
		break_counter = 0
		while True:
			ychange = randint(-5, 5)
			xchange = randint(-5, 5)
			newID = id + xchange + (ychange*MapHandle.width)
			size = len(self.grid)

			if newID in MapHandle.removedID or newID < 0 or newID > size or not self.grid[newID].isWalkable:
				MapHandle.removedID.append(newID)
				break_counter += 1
			else:
				return MapHandle.grid[newID]

			if break_counter >= 10:
				return False

	def searchForPath(self, startNode, endNode):
		return BreadthFirst(self, startNode, endNode)

	def findTree(self, unit):
		unit.startNode = self.grid[unit.nodeId]
		unit.endNode = ResourceManager.getClosestTree(unit)
		if unit.endNode:
			return self.searchForPath(unit.startNode, unit.endNode)
		else:
			return False

	def findHome(self, unit):
		unit.startNode = self.grid[unit.nodeId]
		unit.endNode = self.grid[TownHall.nodeId]
		return self.searchForPath(unit.startNode, unit.endNode)


	#returns the manhattan distance between two nodes
	def getDistance(nodeA, nodeB):
		return abs(nodeA.x - nodeB.x) + abs(nodeA.y - nodeB.y)
	#returns the node with he lowest f cost. used for A*
	def getLowestFCost(openNodes, map):
		lowest = len(map)*2
		id = 0
		for node in openNodes:
			f_cost = map[node].g_cost + map[node].h_cost
			if f_cost < lowest:
				lowest = f_cost
				id = node

		return id


#Map is filled with instances of this class
class Node:
	isTree = False
	isWalkable = False
	moveSpeed = 0
	color = ""
	id = 0
	g_cost = 0
	h_cost = 0
	x = 0
	y = 0

	pos = []
	shape = None

	def __init__(self, type, tree, walkable, color, id, speed, fogOfWar):
		self.type = type
		self.isTree = tree
		self.isWalkable = walkable
		self.color = color
		self.id = id
		self.moveSpeed = speed
		self.fogOfWar = fogOfWar
		self.x = None
		self.y = None
		self.trees = []
		self.building = None
		self.reservedTrees = 0

# Randomizes a position inside a node when created
class TreeNode:
	size = 4
	shape = None

	def __init__(self, node, windowHandle, mapHandle):
		self.parent = node
		self.widthOfNode = windowHandle.indentX
		self.heigthOfNode = windowHandle.indentY
		self.pos = self.randomTreePos()
		
	def randomTreePos(self):
		self.x = x = uniform(self.parent.x*self.widthOfNode, (self.parent.x+1)*self.widthOfNode)
		self.y = y = uniform(self.parent.y*self.heigthOfNode, (self.parent.y+1)*self.heigthOfNode)

		return [x-self.size/2, y-self.size/2, x+self.size/2, y+self.size/2]

import messaging
from math import *
from graphics import *