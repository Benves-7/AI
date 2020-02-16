from window import *

class BaseGameEntity:
	Im_nextValidID = 0
	mapHandle = Window.mapHandle
	width = None
	height = None
	windowClass = 0
	townHall = None
	#path = None
	def __init__(self, ID):
		self.setID(ID)
		self.position = TownHall.position
		self.size = [Window.indentX/2, Window.indentY/2]
		self.shape = Window.window.create_oval(self.position[0]-self.size[0]/2, self.position[1]-self.size[1]/2, self.position[0]+self.size[0]/2, self.position[1]+self.size[1]/2, fill= "yellow")
		self.nodeId = TownHall.nodeId
		self.path = []
	
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

	#Follows a path and returns true when it has reached the next point
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
	def __init__(self, id, type, profession = ""):
		BaseGameEntity.__init__(self, id)
		self.type = type
		self.profession = profession
		self.startTime = None
		if(type == "explorer"):
			self.m_currentState = state.EStart()
		elif(type == "worker"):
			self.m_currentState = state.WStart()
			self.trees = 0
		elif(type == "craftsman"):
			self.m_currentState = state.CStart()

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

	#This is called when an explorer goes to a new now and it removes the fog of war
	def exploreCloseNodes(self):
		neighbours = []
		localMap = BaseGameEntity.map
		#Checks if the node is aleady explored to avoid redrawing trees
		if(localMap[self.pointIndex-self.width].fogOfWar):
			neighbours.append(self.pointIndex-self.width)
		if(localMap[self.pointIndex + 1].fogOfWar):
			neighbours.append(self.pointIndex + 1)
		if(localMap[self.pointIndex - 1].fogOfWar):
			neighbours.append(self.pointIndex - 1)
		if(localMap[self.pointIndex + self.width].fogOfWar):
			neighbours.append(self.pointIndex + self.width)
		if(localMap[self.pointIndex - self.width + 1].fogOfWar):
			neighbours.append(self.pointIndex - self.width + 1)
		if(localMap[self.pointIndex - self.width - 1].fogOfWar):
			neighbours.append(self.pointIndex - self.width - 1)
		if(localMap[self.pointIndex + self.width + 1].fogOfWar):
			neighbours.append(self.pointIndex + self.width + 1)
		if(localMap[self.pointIndex + self.width - 1].fogOfWar):
			neighbours.append(self.pointIndex + self.width - 1)
		#If any of the nodes are tree nodes add the trees to the map
		for x in neighbours:
			self.windowClass.window.items[x].setFill(color_rgb(self.map[x].color[0], self.map[x].color[1], self.map[x].color[2]))
			BaseGameEntity.map[x].fogOfWar = False
			#If the node is a tree node draw the trees
			if(BaseGameEntity.map[x].isTree):
				#Add the tree locations to the resource managers list of trees
				ResourceManager.treeLocations.append(x)
				for tree in BaseGameEntity.map[x].trees:
					tree.point.draw(BaseGameEntity.windowClass.window)
					#tree.point.undraw()

			




import state
import messaging
from math import *
from graphics import *
from managers import *
from config import *
from buildings import *

