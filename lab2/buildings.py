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
	def __init__(self, position):
		#Load the position of the town hall from the config file
		TownHall.position = position
		self.sizeX = sizeX = Window.indentX/10*6
		self.sizeY = sizeY = Window.indentY/10*6
		self.charCoal = 0
		self.trees = 0
		self.position = 0
		self.ironOre = 0
		self.ironBars = 0
		pos = self.getPos()
		x1 = pos[0]-sizeX/2
		x2 = pos[1]-sizeY/2
		x3 = pos[0]+sizeX/2
		x4 = pos[1]+sizeY/2

		self.shape = Window.window.create_rectangle(pos[0]-sizeX/2, pos[1]-sizeY/2, pos[0]+sizeX/2, pos[1]+sizeY/2, fill = "orange")

		print("hejk")

	def getPos(self):
		self.x = x = BaseGameEntity.map[TownHall.position].x * Window.indentX + Window.indentX/2
		self.y = y = BaseGameEntity.map[TownHall.position].y * Window.indentY + Window.indentY/2
		return [x,y]

from config import *
from window import *
from basegameentity import *