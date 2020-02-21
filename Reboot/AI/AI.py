from config import *
from managers import *

if __name__ == '__main__':

	runSetup()

	while True:
		UnitManager.update()
		ResourceManager.update()
		BuildingManager.update()
		WindowHandle.update()

