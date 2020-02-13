from maploader import *
from window import *
from fileimporter import *
from config import *
from basegameentity import *
from time import perf_counter
Configuration.open()
mapHandle = MapLoader()
windowHandle = Window()
grid = mapHandle.createGrid(FileImporter.loadFile("map.txt"))
windowHandle.drawWindow(mapHandle, grid)
mapHandle.addTrees(windowHandle, mapHandle)

BaseGameEntity.setDependencies(grid, windowHandle, mapHandle)
BaseGameEntity.placeStaticBuildings()
explorerlist = []


for x in range(0,25):
	worker = Entity(x, "worker")
	EntityManager.addEntity(worker)
	explorerlist.append(worker)
time = perf_counter()
while(1):

	for entity in explorerlist:
		entity.Update()

	ResourceManager.Update()
	EntityManager.Update()
	BuildingManager.Update()

	if(perf_counter() - time > 1):
		time = perf_counter()
		windowHandle.updateWindow()