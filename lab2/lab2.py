from maploader import *
from window import *
from fileimporter import *
from config import *
from managers import *
from basegameentity import *
from time import perf_counter, sleep
import threading


Configuration.open()
mapHandle = MapHandle()
windowHandle = Window()
grid = mapHandle.createGrid(FileImporter.loadFile("map.txt"))
windowHandle.drawWindow(mapHandle, grid)
mapHandle.addTrees(windowHandle, mapHandle)

BaseGameEntity.setDependencies(grid, windowHandle, mapHandle)
BaseGameEntity.placeStaticBuildings()
unitList = []

for x in range(25):
	worker = Entity(x, "worker", mapHandle, windowHandle)
	EntityManager.addEntity(worker)
	UnitManager.addUnit(worker)

def managers():
	while True:
		start = perf_counter()
		ResourceManager.Update()
		BuildingManager.Update()
		EntityManager.Update()
		time = perf_counter() - start
		if time < 0.016:
			sleep(0.016-time)

def units():
	while True:
		start = perf_counter()
		UnitManager.Update()
		time = perf_counter() - start
		if time < 0.016:
			sleep(0.016-time)

def main():
	while True:
		windowHandle.updateWindow()

if __name__ == '__main__':

	threading.Thread(target= managers).start()
	threading.Thread(target= units).start()
	main()