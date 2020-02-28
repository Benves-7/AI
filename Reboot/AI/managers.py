class Manager:
	def update():
		print("Base update.. ERROR")

class UnitManager(Manager):
	unitList = []

	workers = 0
	explorers = 0
	craftsman = 0

	needExplorers = False
	needCraftsman = False

	idleCounter = 0


	def getIdle(type= "", profession= ""):
		for unit in UnitManager.unitList:
			if unit.currentState == Idle():
				if type == "":
					return unit
				elif type == unit.type and profession == unit.profession:
					return unit
		if perf_counter() - UnitManager.idleCounter > 5:
			UnitManager.idleCounter = perf_counter()
			print("no idle unit of type " + str(type) + " found...")
		return False

	def addUnit(unit):
		UnitManager.unitList.append(unit)

	def upgrade():
		if (ResourceManager.needWood or ResourceManager.needIron) and UnitManager.explorers < Config.config["aiData"]["explorers"]:
			unit = UnitManager.getIdle("worker")
			if unit:
				unit.changeType("explorer")
				UnitManager.explorers += 1

		if BuildingManager.needBuilder and UnitManager.craftsman < Config.config["aiData"]["craftsman"]:
				unit = UnitManager.getIdle("worker")
				if unit:
					unit.changeType("craftsman", "builder")
					UnitManager.craftsman += 1

	def assignWork():
		for unit in UnitManager.unitList:
			if unit.currentState == Idle():
				if BuildingManager.needBuilder and unit.type == "craftsman":
					unit.profession = "builder"
					unit.changeState(BMoveToBuilding())

				elif ResourceManager.needCharcoal and BuildingManager.numKilns > 0 and unit.type == "craftsman" and ResourceManager.wood >= 1:
					unit.profession = "crafter"
					unit.changeState(CMoveToKiln())

				elif ResourceManager.needWood and ResourceManager.numOfTrees > 0 and unit.type == "worker":
					unit.changeState(WGoToTree())

	def update():
		UnitManager.upgrade()
		UnitManager.assignWork()
		for unit in UnitManager.unitList:
			unit.update()

class ResourceManager(Manager):
	# resources
	wood = 100
	charcoal = 0
	ironore = 0
	swords = 0

	# needs
	needWood = False
	needCharcoal = False
	needIron = False
	needSword = False

	# information
	treeLocations = []
	numOfTrees = 0
	ironLocations = []
	numOfIron = 0

	def getClosestTree(unit):
		if ResourceManager.treeLocations == []:
			return False
		currentTile = MapHandle.grid[unit.tileId]
		distance = len(MapHandle.grid)
		closestTile = None
		for tile in ResourceManager.treeLocations:
			if tile.reservedTrees < len(tile.trees):
				distanceToTree = abs(tile.xy[0] - currentTile.xy[0]) + abs(tile.xy[1] - currentTile.xy[1])
				if(distanceToTree < distance):
					distance = distanceToTree
					closestTile = tile
			else:
				ResourceManager.treeLocations.remove(tile)

		if(distance == len(MapHandle.grid)):
			return False
		else:
			closestTile.reservedTrees += 1
			ResourceManager.numOfTrees -= 1
			return closestTile

	def update():
		## check if resources exist and change needs.
		if ResourceManager.wood <= 400:
			ResourceManager.needWood = True
		else:
			ResourceManager.needWood = False

		if ResourceManager.charcoal <= 200:
			ResourceManager.needCharcoal = True
		else:
			ResourceManager.needCharcoal = False

		if ResourceManager.ironore <= 100:
			ResourceManager.needIron = True
		else:
			ResourceManager.needIron = False

		if ResourceManager.swords <= 10:
			ResourceManager.needSword = True
		else:
			ResourceManager.needSword = False

class BuildingManager(Manager):
	config = None

	numKilns = 0
	numSmithy = 0
	numTownhall = 0

	needBuilder = False
	needKiln = False
	needSmithy = False

	buildings = []
	unfinishedBuilding = []
	townhall = None

	def addBuilding(building):
		if BuildingManager.config == None:
			BuildingManager.config = Config.config["buildings"]

		BuildingManager.unfinishedBuilding = building
		if building.type == "kiln":
			BuildingManager.numKilns += 1
		elif building.type == "smithy":
			BuildingManager.numSmithy += 1
		elif building.type == "townhall":
			BuildingManager.buildings.append(building)
			BuildingManager.unfinishedBuilding = None
			BuildingManager.townhall = building
			BuildingManager.numTownhall += 1

	def completeBuilding():
		BuildingManager.unfinishedBuilding.done = True
		BuildingManager.buildings.append(BuildingManager.unfinishedBuilding)
		BuildingManager.needBuilder = False

	def update():
		config = BuildingManager.config
		if ResourceManager.wood >= config["kiln"]["cost"] and BuildingManager.numKilns < config["kiln"]["num"]:
			BuildingManager.needBuilder = True
			if BuildingManager.unfinishedBuilding == None:
				BuildingManager.addBuilding(Kiln(Config.nextID))

class WindowManager(Manager):
	def update(fps_limit):
		WindowHandle.update(fps_limit)


from config import *
from states import *
from basegameentity import *