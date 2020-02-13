from maploader import *
from window import *
from fileimporter import *
from config import *
from basegameentity import *
from time import perf_counter
Configuration.open()
a = MapLoader()
grid = a.createGrid(FileImporter.loadFile("map.txt"))
b = Window()
b.drawWindow(a.width, a.heigth, grid)
a.addTrees(grid, b, a)

BaseGameEntity.setDependencies(grid, b, a.width, a.heigth)
#BaseGameEntity.placeStaticBuildings()
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
		b.updateWindow()