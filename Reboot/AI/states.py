class State:
	#Used for checking if a worker is in a certain state, equality check
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
	def __ne__(self, other):
		return not self.__eq__(other)

class Idle(State):
	def Enter(self, unit):
		pass
	def Execute(self, unit):
		pass
	def Exit(self, unit):
		pass
##======================================================
#Craftsman states
class CStart(State):
	def Enter(self, unit):
		pass
	def Execute(self, unit):
		unit.changeState(Idle())
	def Exit(self, unit):
		pass

class CMoveToKiln(State):
	def Enter(self, unit):
		unit.target = unit.findTarget("kiln")
		unit.path = unit.findBuilding()
		if unit.path:
			unit.path.pop(0)
		else:
			unit.changeState(Idle())

	def Execute(self, unit):
		if len(unit.path) < 1:
			unit.changeState(CWorking())
		elif unit.moveTo():
			unit.tileId = unit.path[0]
			unit.path.pop(0)
			MapHandle.exploreCloseTiles(unit.tileId)

	def Exit(self, unit):
		pass

class CMoveToSmith(State):
	def Enter(self, unit):
		pass
	def Execute(self, unit):
		pass
	def Exit(self, unit):
		pass
		pass

class CWorking(State):
	def Enter(self, unit):
		unit.startTime = perf_counter()
		unit.doneWhen = Config.config["workTime"]["coaling"]

	def Execute(self, unit):
		if perf_counter() - unit.startTime > unit.doneWhen:
			unit.target.addResources()
			unit.changeState(BMoveBackToTownHall())
	
	def Exit(self, unit):
		unit.target.worker = None

#Builder states
class BMoveToBuilding(State):
	def Enter(self, unit):
		unit.target = BuildingManager.unfinishedBuilding
		unit.path = unit.findBuilding()
		if unit.path:
			unit.path.pop(0)
		else:
			unit.changeState(Idle())

	def Execute(self, unit):
		if len(unit.path) < 1:
			unit.changeState(BBuildBuilding())
		elif unit.moveTo():
			unit.tileId = unit.path[0]
			unit.path.pop(0)
			MapHandle.exploreCloseTiles(unit.tileId)

	def Exit(self, unit):
		pass

class BBuildBuilding(State):
	def Enter(self, unit):
		unit.startTime = perf_counter()
		unit.doneWhen = Config.config["buildings"]["kiln"]["time"]

	def Execute(self, unit):
		if perf_counter() - unit.startTime > unit.doneWhen:
			BuildingManager.completeBuilding()
			ResourceManager.wood -= Config.config["buildings"]["kiln"]["cost"]
			unit.changeState(BMoveBackToTownHall())

	def Exit(self, unit):
		pass

class BMoveBackToTownHall(State):
	def Enter(self, unit):
		unit.path = unit.findHome()
		if unit.path:
			unit.path.pop(0)
			unit.tryagain = False
		else:
			unit.tryagain = True

	def Execute(self, unit):
		if not unit.tryagain:
			if len(unit.path) < 1:
				unit.changeState(Idle())
			elif unit.moveTo():
				unit.tileId = unit.path[0]
				unit.path.pop(0)
				MapHandle.exploreCloseTiles(unit.tileId)
		else:
			unit.changeState(BMoveBackToTownHall())

	def Exit(self, unit):
		return


##======================================================
#Worker states
class WStart(State):
	def Enter(self, worker):
		pass
	def Execute(self, worker):
		worker.changeState(Idle())
	def Exit(self, worker):
		pass

class WUpgradeToExplorer(State):

	def Enter(self, unit):
		unit.startTime = perf_counter()
		unit.doneWhen = Config.config["upgradeTimes"]["explorer"]
	
	def Execute(self, unit):
		if perf_counter() - unit.startTime > unit.doneWhen:
			unit.colorChange = True
			unit.color = Config.config["unitData"]["Ecolor"]
			unit.changeState(EStart())

	def Exit(self, unit):
		pass

class WUpgradeToCraftsman(State):
	def Enter(self, unit):
		print(str(unit.ID) + " upgrading to craftsman.")
		unit.startTime = perf_counter()
		unit.doneWhen = Config.config["upgradeTimes"]["explorer"]
	def Execute(self, unit):
		if perf_counter() - unit.startTime > unit.doneWhen:
			unit.colorChange = True
			unit.color = Config.config["unitData"]["Ccolor"]
			unit.changeState(CStart())
	def Exit(self, unit):
		 pass

class WCuttingTree(State):
	def Enter(self, unit):
		unit.startTime = perf_counter()
		unit.doneWhen = Config.config["workTime"]["woodChop"]

	def Execute(self, unit):
		if perf_counter() - unit.startTime > unit.doneWhen:
			tree = unit.endNode.trees.pop()
			WindowHandle.removeShapes.append(tree.shape)
			unit.changeState(WMoveBackToTownHall())
			
	def Exit(self, unit):
		pass

class WMoveBackToTownHall(State):
	def Enter(self, unit):
		unit.path = unit.findHome()
		if unit.path:
			unit.path.pop(0)
			unit.tryagain = False
		else:
			unit.tryagain = True

	def Execute(self, unit):
		if not unit.tryagain:
			if len(unit.path) < 1:
				ResourceManager.wood += 1
				unit.changeState(Idle())
			elif unit.moveTo():
				unit.tileId = unit.path[0]
				unit.path.pop(0)
				MapHandle.exploreCloseTiles(unit.tileId)
		else:
			unit.changeState(WMoveBackToTownHall())

	def Exit(self, unit):
		pass

class WGoToTree(State):
	def Enter(self, unit):
		unit.path = unit.findTree()
		if unit.path:
			unit.path.pop(0)
		else:
			unit.changeState(Idle())

	def Execute(self, unit):
		if len(unit.path) < 1:
			unit.changeState(WCuttingTree())
		elif unit.moveTo():
			unit.tileId = unit.path[0]
			unit.path.pop(0)
			MapHandle.exploreCloseTiles(unit.tileId)

	def Exit(self, unit):
		pass

##======================================================
#Explorer states
class EStart(State):
	def Enter(self, unit):
		pass

	def Execute(self, unit):
		unit.changeState(EExploring())

	def Exit(self, unit):
		pass

class EExploring(State):
	def Enter(self, unit):
		unit.path = unit.explore()
		if unit.path:
			unit.path.pop(0)
		else:
			unit.changeState(EWaiting())

	def Execute(self, unit):
		if len(unit.path) < 1:
			unit.changeState(EWaiting())
		elif unit.moveTo():
			unit.tileId = unit.path.pop(0)
			MapHandle.exploreCloseTiles(unit.tileId)
			
	def Exit(self, unit):
		pass

class EWaiting(State):
	def Enter(self, unit):
		pass

	def Execute(self, unit):
		unit.changeState(EExploring())

	def Exit(self, unit):
		pass

from time import perf_counter
from config import *
from managers import *