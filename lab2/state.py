


class State:
	def messageRecvd(message):#Check what the message contains and act accordingly
		#Type 1: request, Type 2: ack, Type 3: go now, Type 4: leave

		if(message['type'] == 1):
			pass
		elif(message['type'] == 2): 
			pass
		elif(message['type'] == 3):
			pass
		elif(message['type'] == 4):
			pass
	def Enter(self):
		assert 0, "Something went very wrong"
	def Execute(self):
		assert 0, "Something went very wrong"
	def Exit(self):
		assert 0, "Something went very wrong"

	#Used for checking if a worker is in a certain state, equality check
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
	def __ne__(self, other):
		return not self.__eq__(other)


class EStart(State):
	def Enter(self, explorer):
		pass
	def Execute(self, explorer):
		pass
	def Exit(self, explorer):
		pass

#Craftsman states
class CStart(State):
	def Enter(self, craftsman):
		pass
	def Execute(self, craftsman):
		pass
	def Exit(self, craftsman):
		pass

class CMoveToKiln(State):
	def Enter(self, craftsman):
		pass
	def Execute(self, craftsman):
		pass
	def Exit(self, craftsman):
		pass

class CWorking(State):
	def Enter(self, worker):
		pass
	def Execute(self, worker):
		pass
	def Exit(self, worker):
		pass
#Worker states
class WStart(State):
	def Enter(self, worker):
		pass
	def Execute(self, worker):
		pass
	def Exit(self, worker):
		pass

class WUpgradeToExplorer(State):

	def Enter(self, worker):
		pass
	def Execute(self, worker):
		pass
	def Exit(self, worker):
		pass

class WUpgradeToCraftsman(State):
	def Enter(self, worker):
		pass
	def Execute(self, worker):
		pass
	def Exit(self, craftsman):
		 pass

class WCuttingTree(State):
	def Enter(self, worker):
		pass
	def Execute(self, worker):
		pass
	def Exit(self, worker):
		pass

class WMoveBackToTownHall(State):
	def Enter(self, Entity):
		pass
	def Execute(self, Entity):
		pass
	def Exit(self, Entity):
		pass

class WGoToTree(State):
	def Enter(self, Entity):
		pass
	def Execute(self, Entity):
		pass
	def Exit(self, worker):
		pass
#Builder states
class BBuildBuilding(State):
	def Enter(self, builder):
		pass
	def Execute(self, builder):
		pass
	def Exit(self, builder):
		pass
class BMoveBackToTownHall(State):
	def Enter(self, builder):
		pass
	def Execute(self, builder):
		pass
	def Exit(self, Entity):
		return

#Explorer states
class Exploring(State):
	def Enter(self, Entity):
		pass
	def Execute(self, Entity):
		pass
	def Exit(self, Entity):
		pass

class Waiting(State):
	def Enter(self, worker):
		worker.path = None
	def Execute(self, worker):
		return
	def Exit(self, worker):
		return




from basegameentity import *
from messaging import *
from pathfinding import *
from managers import *
from config import Configuration
from graphics import *
from time import perf_counter