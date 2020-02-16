#Building base class
class Building:	
	def __init__(self, position):
		self.position = position


class Kiln(Building):

	def __init__(self, position):
		self.position = position
		self.treeCoal = 0
		self.trees = 0
		self.populated = False
		self.complete = False
		self.type = "kiln"

class Smith(Building):
	pass

class Smelter(Building):
	def __init(self, position):
		self.position = position
		self.ironBar = 0
		self.ironOre = 0

class TrainingCamp(Building):
	pass

class TownHall(Building):
	nodeId = 0
	position = 0
	charcoal = 0
	trees = 0
	ironOre = 0
	ironBars = 0
	def __init__(self, nodeId):
		#Load the position of the town hall from the config file
		TownHall.nodeId = self.nodeId = nodeId
		TownHall.position = self.position = pos = self.getPos()
		self.size = size = [Window.indentX/10*9, Window.indentY/10*9]

		TownHall.charCoal = self.charCoal = 0
		TownHall.trees = self.trees = 0
		TownHall.ironOre = self.ironOre = 0
		TownHall.ironBars = self.ironBars = 0
		self.shape = Window.window.create_rectangle(pos[0]-size[0]/2, pos[1]-size[1]/2, pos[0]+size[0]/2, pos[1]+size[1]/2, fill = "orange")

	def getPos(self):
		self.x = x = BaseGameEntity.map[TownHall.nodeId].x * Window.indentX + Window.indentX/2
		self.y = y = BaseGameEntity.map[TownHall.nodeId].y * Window.indentY + Window.indentY/2
		return [x,y]

from config import *
from window import *
from basegameentity import *