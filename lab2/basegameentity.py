from window import *

class BaseGameEntity:
	Im_nextValidID = 0
	width = None
	height = None
	windowClass = 0
	townHall = None
	mapHandle = None
	#path = None

	def __init__(self, ID, mapHandle, windowHandle):
		self.setID(ID)
		self.mapHandle = mapHandle
		self.windowClass = windowHandle
		self.size = [Window.indentX/2, Window.indentY/2]
	
	#Place buildings that should be placed before the simulation starts
	def placeStaticBuildings():
		townhallPos = Configuration.config["buildings"]["townHall"]["position"]
		for node in BaseGameEntity.map:
			if node.id == townhallPos:
				node.building = TownHall(townhallPos)
				BaseGameEntity.townHall = node.id

	def setID(self, ID):
		if(ID >= BaseGameEntity.Im_nextValidID):
			self.ID = ID
			BaseGameEntity.Im_nextValidID = ID + 1
		else:
			assert 0, "invalid ID"

	#Set static variables that are use by all the entities
	def setDependencies(map, windowHandle, mapHandle):
		BaseGameEntity.map = map
		BaseGameEntity.windowClass = windowHandle
		BaseGameEntity.width = mapHandle.width
		BaseGameEntity.height = mapHandle.heigth

	def goTo(self):
		try:
			distX = (self.point.getX() - self.map[self.path[0]].center.getX())
			distY = (self.point.getY() - self.map[self.path[0]].center.getY())
		except:
			return False
		angle = atan2(distY, distX)

		dX = -cos(angle) * self.map[self.path[0]].moveSpeed
		dY = -sin(angle) * self.map[self.path[0]].moveSpeed

		if(abs(dX) > abs(distX)):
			dX = -distX
		if(abs(dY) > abs(distY)):
			dY = -distY

		self.point.move(dX, dY)
		self.playerCircle.move(dX, dY)

		return self.point.getX() == self.map[self.path[0]].center.getX() and self.point.getY() == self.map[self.path[0]].center.getY() 




class Entity(BaseGameEntity):
	def __init__(self, id, type, mapHandle, windowHandle, profession = ""):
		BaseGameEntity.__init__(self, id, mapHandle, windowHandle)
		self.type = type
		self.profession = profession
		self.startTime = None
		
		self.position = self.spawnPos()
		self.lastPosition = self.spawnPos()
		
		self.shape = Window.window.create_oval(self.position[0]-self.size[0]/2,
			self.position[1]-self.size[1]/2,
			self.position[0]+self.size[0]/2, 
			self.position[1]+self.size[1]/2, 
			fill= "yellow")
		self.nodeId = TownHall.nodeId
		self.path = []
		if(type == "explorer"):
			self.m_currentState = state.EStart()
		elif(type == "worker"):
			self.m_currentState = state.WStart()
			self.trees = 0
		elif(type == "craftsman"):
			self.m_currentState = state.CStart()

	def spawnPos(self):
		x = TownHall.position[0]
		y = TownHall.position[1]
		return [x,y]

	#Used for upgrading an entity
	def changeType(self, type, profession = ""):
		if(type == "explorer"):
			self.type = "explorer"
			self.changeState(state.WUpgradeToExplorer())
		elif(type == "craftsman"):
			self.type = "craftsman"
			self.profession = profession
			self.working = False
			self.changeState(state.WUpgradeToCraftsman())

	def Update(self):
		self.m_currentState.Execute(self) #execute current state execute method

	def changeLocation(self, location):
		self.m_currentLocation = location

	def changeState(self, state):
		self.m_currentState.Exit(self)
		self.m_currentState = state
		self.m_currentState.Enter(self)

	def recvMessage(self, message):
		self.m_currentState.messageRecvd(message)

	def getMove(self):
		
		dx = -(self.lastPosition[0] - self.position[0])
		dy = -(self.lastPosition[1] - self.position[1])

		self.lastPosition[0] = self.position[0]
		self.lastPosition[1] = self.position[1]

		return [dx,dy]
		pass

		#Follows a path and returns true when it has reached the next point
	def MoveTo(self):
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

	#This is called when an explorer goes to a new now and it removes the fog of war
	def exploreCloseNodes(self):
		neighbours = []
		
		width = self.mapHandle.width
		localMap = self.mapHandle.grid
		id = self.nodeId
		checklist = [id - 1 - width, id - width, id + 1 - width, id - 1, id, id + 1, id - 1 + width, id + width, id + 1 + width]

		#Checks if the node is aleady explored to avoid redrawing trees
		for nodeID in checklist:
			tile = localMap[nodeID]
			if(tile.fogOfWar):
				tile.fogOfWar = False
				Window.exploredID.append(nodeID)

		#If any of the nodes are tree nodes add the trees to the map
		#for x in neighbours:
		#	self.windowClass.window.items[x].setFill(color_rgb(self.map[x].color[0], self.map[x].color[1], self.map[x].color[2]))
		#	BaseGameEntity.map[x].fogOfWar = False
		#	#If the node is a tree node draw the trees
		#	if(BaseGameEntity.map[x].isTree):
		#		#Add the tree locations to the resource managers list of trees
		#		ResourceManager.treeLocations.append(x)
		#		for tree in BaseGameEntity.map[x].trees:
		#			tree.point.draw(BaseGameEntity.windowClass.window)
		#			#tree.point.undraw()

			




import state
import messaging
from math import *
from graphics import *
from managers import *
from config import *
from buildings import *

