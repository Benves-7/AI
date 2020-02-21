from config import *
from states import *

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
	
	def addUnit(unit):
		UnitManager.unitList.append(unit)

	def update():
		if ResourceManager.needWood and ResourceManager.numOfTrees <= 5 and UnitManager.explorers < Config.config["aiData"]["explorers"]:
			unit = UnitManager.getIdle()
			unit.changeState(WUpgradeToExplorer())
			UnitManager.explorers += 1

		if ResourceManager.needIron and ResourceManager.numOfIron <= 5 and UnitManager.explorers < Config.config["aiData"]["explorers"]:
			unit = UnitManager.getIdle()
			unit.changeState(WUpgradeToExplorer())
			UnitManager.explorers += 1

		if ResourceManager.needCharcoal and BuildingManager.kilns >= 1 and UnitManager.craftsman < Config.config["aiData"]["craftsman"]:
			unit = UnitManager.getIdle()
			unit.changeState(WUpgradeToCraftsman())
			UnitManager.craftsman += 1

		if ResourceManager.needSword and BuildingManager.smithy >= 1 and UnitManager.craftsman < Config.config["aiData"]["craftsman"]:
			unit = UnitManager.getIdle()
			unit.changeState(WUpgradeToCraftsman())
			UnitManager.craftsman += 1


		for unit in UnitManager.unitList:
			unit.update()


class ResourceManager(Manager):
	# resources
	wood = 0
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
		if treeLocations == []:
			return False
		currentTile = MapHandle.grid[unit.nodeId]
		distance = len(MapHandle.grid)
		closestTile = None
		for tile in ResourceManager.treelocations:
			if tile.reservedTrees < len(tile.trees):
				distanceToTree = abs(tile.xy[0] - currentTile.xy[0]) + abs(tile.xy[1] - currentTile.xy[1])
				if(distanceToTree < distance):
					distance = distanceToTree
					cclosestTile = tile

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

	kilns = 0
	smithy = 0
	townhall = 0

	buildings = []

	def addBuilding(building):
		if BuildingManager.config == None:
			BuildingManager.config = Config.config["buildings"]

		BuildingManager.buildings.append(building)
		if building.type == "kiln":
			BuildingManager.kilns += 1
		elif building.type == "smithy":
			BuildingManager.smithy += 1
		elif building.type == "townhall":
			BuildingManager.townhall += 1

	def update():
		config = BuildingManager.config
		if ResourceManager.wood >= config["kiln"]["cost"]:
			pass