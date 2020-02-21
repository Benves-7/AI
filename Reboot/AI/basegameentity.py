from config import *
from random import uniform
from states import WStart

##===================================================
# Base GameEntity class
class BaseGameEntity:
	nextValidID = 0
	ID = 0

	mapHandle = None
	winHandle = None

	def __init__(self, ID):
		self.setID(ID)

	def setID(self, ID):
		if(ID >= BaseGameEntity.nextValidID):
			self.ID = ID
			BaseGameEntity.nextValidID = ID+1
			Config.nextID += 1
		else:
			assert 0, "invalid ID"

	def exploreCloseTiles(self, tile):
		neighbours = []

		width = MapHandle.width
		localMap = MapHandle.grid
		id = tile.ID
		checklist = [id - 1 - width, id - width, id + 1 - width, id - 1, id, id + 1, id - 1 + width, id + width, id + 1 + width]

		# Check if node is already explored to avoid redrawing trees
		for tileId in checklist:
			tile = localMap[tileId]
			if tile.fogOfWar:
				tile.fogOfWar = False
				WindowHandle.exploredTiles.append(tile)

	def update(self):
		print("Base update.. ERROR")

##===================================================
# Unit class
class Unit(BaseGameEntity):
	def __init__(self, ID, townhall, type, profession = ""):
		BaseGameEntity.__init__(self, ID)
		self.position = Unit.getPositionOf(townhall)
		self.lastPosition = Unit.getPositionOf(townhall)
		self.type = type
		self.profession = profession
		self.startTime = None
		self.doneWhen = None
		sizeConfig = Config.config["unitData"]["size"]
		size = [WindowHandle.indent[0]/10*sizeConfig/2, WindowHandle.indent[1]/10*sizeConfig/2]
		self.shape = WindowHandle.window.create_oval(self.position[0]-size[0], self.position[1]-size[1], self.position[0]+size[0], self.position[1]+size[1], fill= Config.config["unitData"]["color"])
		self.tileId = townhall.tileId
		self.path = []
		self.currentState = WStart()

	def getPositionOf(item):
		return [item.position[0], item.position[1]]

	def update(self):
		self.currentState.Execute(self)

	def changeType(self, type, profession = ""):
		if(type == "explorer"):
			self.type = "explorer"
			self.changeState(state.WUpgradeToExplorer())
		elif(type == "craftsman"):
			self.type = "craftsman"
			self.profession = profession
			self.changeState(state.WUpgradeToCraftsman())
		else:
			assert 0, "invalid type change..."

	def changeState(self, newState):
		self.currentState.Exit(self)
		self.currentState = newState
		self.currentState.Enter(self)

	def getDeltaMove(self):
		dx = -(self.lastPosition[0] - self.position[0])
		dy = -(self.lastPosition[1] - self.position[1])

		self.lastPosition[0] = self.position[0]
		self.lastPosition[1] = self.position[1]

		return [dx, dy]

	def moveTo(self):
		try:
			node = self.map[self.path[0]]
			distX = (self.position[0] - node.pos[0])
			distY = (self.position[1] - node.pos[1])
		except:
			return False

		angle = atan2(distY, distX)

		dxangle = -cos(angle)
		dyangle = -sin(angle)

		dx = -cos(angle) * node.moveSpeed
		dy = -sin(angle) * node.moveSpeed

		if abs(dx) > abs(distX):
			dx = -distX
		if abs(dy) > abs(distY):
			dy = -distY

		self.position[0] += dx
		self.position[1] += dy

		return self.position[0] == node.pos[0] and self.position[1] == node.pos[1]

##===================================================
# Tile class (used to keep info about map).
class Tile(BaseGameEntity):
	config = None

	def __init__(self, ID, char):
		BaseGameEntity.__init__(self, ID)
		if Tile.config == None:
			Tile.config = Config.config["tileTypes"]
		if char == "B":
			self.type = "border"
		elif char == "M":
			self.type = "mountain"
		elif char == "G":
			self.type = "ground"
		elif char == "T":
			self.type = "wood"
		elif char == "S":
			self.type = "swamp"
		elif char == "W":
			self.type = "water"
			
		self.isTree = bool(Tile.config[self.type]["trees"])
		self.isWalkable = bool(Tile.config[self.type]["walkable"])
		self.color = Tile.config[self.type]["color"]
		self.moveSpeed = Tile.config[self.type]["mSpeed"]
		self.fogOfWar = Tile.config[self.type]["fogOfWar"]

		self.xy = []
		self.position = []
		self.trees = []
		self.building = None
		self.reservedTrees = 0

	def addTrees(self):
		for x in range(5):
			self.trees.append(TreeNode(self))

# TreeNode class (used to keep info about the trees in Tiles)
class TreeNode:
	size = 4
	shape = None

	def __init__(self, tile):
		self.parent = tile
		self.nodeSize = WindowHandle.indent
		self.position = self.randomTreePosition()

	def randomTreePosition(self):
		self.x = x = uniform(self.parent.xy[0]*self.nodeSize[0], (self.parent.xy[0]+1)*self.nodeSize[0])
		self.y = y = uniform(self.parent.xy[1]*self.nodeSize[1], (self.parent.xy[1]+1)*self.nodeSize[1])

		return [x-self.size/2, y-self.size/2, x+self.size/2, y+self.size/2]

##===================================================
# Building class
class Building(BaseGameEntity):
	def __init__(self, ID):
		BaseGameEntity.__init__(self, ID)

class TownHall(Building):
	tileId = None
	position = None
	shape = None
	type = None

	def __init__(self, ID):
		BaseGameEntity.__init__(self, ID)
		config = Config.config["buildings"]["townHall"]
		self.type = "townhall"
		self.tileId = config["nodeId"]
		self.parentTile = MapHandle.grid[self.tileId]
		self.position = self.parentTile.position
		self.size = size = [WindowHandle.indent[0]/10*config["size"]/2, WindowHandle.indent[1]/10*config["size"]/2]
		self.shape = WindowHandle.window.create_rectangle(self.position[0]-size[0], self.position[1]-size[1], self.position[0]+size[0], self.position[1]+size[1], fill= config["color"])
		
		self.exploreCloseTiles(self.parentTile)
