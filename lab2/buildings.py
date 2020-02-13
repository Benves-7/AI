#Building base class
class Building:	
	def __init__(self, position):
		self.position = position


class Kiln(Building):

	def __init__(self, position):
		Building.__init__(self, position)
		self.treeCoal = 0
		self.trees = 0
		self.populated = False
		self.complete = False
		self.type = "kiln"

class Smith(Building):
	pass

class Smelter(Building):
	def __init(self, position):
		super.__init__(position)
		self.ironBar = 0
		self.ironOre = 0

class TrainingCamp(Building):
	pass

class TownHall(Building):
	def __init__(self):
		#Load the position of the town hall from the config file
		TownHall.position = Configuration.config["buildings"]["townHall"]["position"]
		self.charCoal = 0
		self.trees = 0
		self.position = 0
		self.ironOre = 0
		self.ironBars = 0
		self.circle = Circle(BaseGameEntity.map[TownHall.position].center, 6)
		self.circle.setFill("blue")


from config import *
from graphics import Circle
from graphics import Point
from basegameentity import *