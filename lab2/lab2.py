from maploader import *
from window import *
from fileimporter import *
from config import *
from basegameentity import *
from time import perf_counter
Configuration.open()
mapHandle = MapHandle()
windowHandle = Window()
grid = mapHandle.createGrid(FileImporter.loadFile("map.txt"))
windowHandle.drawWindow(mapHandle, grid)
mapHandle.addTrees(windowHandle, mapHandle)

BaseGameEntity.setDependencies(grid, windowHandle, mapHandle)
BaseGameEntity.placeStaticBuildings()

unitList = []


for x in range(0,25):
	worker = Entity(x, "worker")
	EntityManager.addEntity(worker)
	unitList.append(worker)

while(1):

	for unit in unitList:
		unit.Update()

	ResourceManager.Update()
	BuildingManager.Update()
	EntityManager.Update()

	windowHandle.updateWindow()