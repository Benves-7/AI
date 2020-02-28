import json
from tkinter import *
from PIL import ImageTk as itk, Image

# Function for running once and setting up window, map and all nodes.
def runSetup():
	Config.open()
	MapHandle.createGrid(FileImporter.loadFile(Config.config["map"]))
	WindowHandle.createWindow()
	BuildingManager.addBuilding(TownHall(Config.nextID))
	for x in range(Config.config["aiData"]["startUnit"]):
		UnitManager.addUnit(Unit(Config.nextID, BuildingManager.buildings[0], "worker"))

# Class for loading and storing json config file
class Config:
	config = {}
	nextID = 0

	def open():
		with open("config.json") as fobj:
			Config.config = json.load(fobj)

# Loads a file and separated into a list of line
class FileImporter:
	def loadFile(path):
		with open(path, 'r') as x:
			list = x.read().splitlines()
		return list

# Class for handling and storing data for the map 
class MapHandle:
	width = 0
	heigth = 0
	grid = []

	def createGrid(lineString):
		MapHandle.width = len(list(lineString[0]))
		nodeConfigs = Config.config["tileTypes"]

		for line in lineString:
			line = list(line) # convert from a string to a list of each character.
			MapHandle.heigth += 1
			for character in line:
				MapHandle.grid.append(Tile(Config.nextID, character))

	def getNeighbours(current):
		map = MapHandle.grid
		width = MapHandle.width
		neighbours = []
		if map[current-1].isWalkable:
			neighbours.append(current-1)
		if map[current-width].isWalkable:
			neighbours.append(current-width)
		if map[current+1].isWalkable:
			neighbours.append(current+1)
		if map[current+width].isWalkable:
			neighbours.append(current+width)
		return neighbours

	def getNeighboursW(current):
		map = MapHandle.grid
		width = MapHandle.width
		neighbours = []
		if not map[current-1].fogOfWar and map[current-1].isWalkable:
			neighbours.append(current-1)
		if not map[current-width].fogOfWar and map[current-width].isWalkable:
			neighbours.append(current-width)
		if not map[current+1].fogOfWar and map[current+1].isWalkable:
			neighbours.append(current+1)
		if not map[current+width].fogOfWar and map[current+width].isWalkable:
			neighbours.append(current+width)
		return neighbours

	def exploreCloseTiles(tileId):
		width = MapHandle.width
		for id in [tileId - width, tileId + 1, tileId - 1, tileId + width, tileId - width + 1, tileId - width - 1, tileId + width + 1, tileId + width - 1]:
			tile = MapHandle.grid[id]
			if tile.fogOfWar:
				tile.fogOfWar = False
				WindowHandle.removeShapes.append(tile.shape)
				if tile.isTree:
					ResourceManager.treeLocations.append(tile)
					ResourceManager.numOfTrees += 5


	def placeBuilding(building):
		id = BuildingManager.townhall.tileId
		neighbours = MapHandle.getNeighbours(id)
		checked = [id]
		chosenTile = None
		while chosenTile == None:
			id = neighbours.pop(0)
			tile = MapHandle.grid[id]
			if tile.isWalkable and tile.building == None:
				chosenTile = tile
			else:
				checked.append(id)
				neighbours += MapHandle.getNeighbours(tile.tileId)

		chosenTile.building = building
		building.parentTile = chosenTile

# Class for handling and storing data for the window and shapes.
class WindowHandle:
	tk = None					# the window
	window = None				# the canvas
	background = None			# background image (used to save graphic time) *(hopefully)
	windowSize = []				# [x, y]
	indent = []					# [x, y]

	removeShapes = []
	addShapes = []

	unitCounter = 0
	loops = 0

	def createWindow():
		WindowHandle.windowSize = [Config.config["windowParams"]["width"], Config.config["windowParams"]["height"]]
		WindowHandle.tk = Tk()
		WindowHandle.tk.title("AI")
		WindowHandle.window = Canvas(WindowHandle.tk, width= WindowHandle.windowSize[0], height= WindowHandle.windowSize[1])
		WindowHandle.window.pack()
		WindowHandle.indent = indent = [WindowHandle.windowSize[0]/MapHandle.width, WindowHandle.windowSize[1]/MapHandle.heigth]

		WindowHandle.createMapImage()

		for y in range(0, MapHandle.heigth):
			for x in range(0, MapHandle.width):
				tileId = x+(y*MapHandle.width)
				tile = MapHandle.grid[tileId]
				tile.tileId = tileId
				tile.xy = [x, y]
				ix=x*indent[0]
				iy=y*indent[1]
				tile.position = [(ix)+(indent[0]/2), (iy)+(indent[1]/2)]
				if tile.isTree:
					tile.addTrees()
					color = Config.config["tileTypes"]["wood"]["treecolor"]
					for tree in tile.trees:
						tree.shape = WindowHandle.window.create_oval(tree.position[0],tree.position[1],tree.position[2],tree.position[3], fill= color)
				if tile.fogOfWar:
					tile.shape = WindowHandle.window.create_rectangle(ix, iy, ix+indent[0], iy+indent[1], fill= 'gray', outline= "")

		WindowHandle.addResourceCounter()

	def addResourceCounter():
		WindowHandle.window.create_text(10,10, anchor= NW, text= "Wood")
		WindowHandle.woodDisplay = WindowHandle.window.create_text(10,25, anchor= NW, text= "Wood")
		WindowHandle.window.create_text(10,40, anchor= NW, text= "Charcoal")
		WindowHandle.coalDisplay = WindowHandle.window.create_text(10,55, anchor= NW, text= "Wood")

	def createMapImage():
		img = Image.open(Config.config["mapimage"])
		img = img.resize((WindowHandle.windowSize[0], WindowHandle.windowSize[1]))
		img.save("newimg.ppm", "ppm")


		WindowHandle.background = itk.PhotoImage(file= 'newimg.ppm')
		WindowHandle.window.create_image(0,0, anchor=NW, image= WindowHandle.background)
		
	def update(fps_limit):
		start = perf_counter()
		WindowHandle.updateUnits(start, fps_limit)
		WindowHandle.removeShape(start, fps_limit)
		WindowHandle.AddShape(start, fps_limit)

		b = BuildingManager.unfinishedBuilding
		if b:
			if b.done:
				WindowHandle.window.itemconfig(b.shape, fill= b.color)
				BuildingManager.unfinishedBuilding = None

		WindowHandle.window.itemconfig(WindowHandle.woodDisplay, text= ResourceManager.wood)
		WindowHandle.window.itemconfig(WindowHandle.coalDisplay, text= ResourceManager.charcoal)

		WindowHandle.window.update()
		WindowHandle.loops += 1

	def updateUnits(start, fps_limit):
		
		while WindowHandle.unitCounter < len(UnitManager.unitList):
			unit = UnitManager.unitList[WindowHandle.unitCounter]
			if unit.colorChange:
				WindowHandle.window.itemconfig(unit.shape, fill= unit.color)
				unit.colorChange = False
			delta = unit.getDeltaMove()
			WindowHandle.window.move(unit.shape, delta[0], delta[1])

			WindowHandle.unitCounter += 1
			if WindowHandle.unitCounter == 25:
				WindowHandle.unitCounter = 0
				break
			if perf_counter() - start > (fps_limit/2):
				break
			
	def removeShape(start, fps_limit):
		while len(WindowHandle.removeShapes) > 0:
			id = WindowHandle.removeShapes.pop(0)
			WindowHandle.window.delete(id)
			if perf_counter() - start > (fps_limit/2):
				break

	def AddShape(start, fps_limit):
		while len(WindowHandle.addShapes) > 0:
			item = WindowHandle.addShapes.pop()
			if item[0] == "oval":
				item[2].shape = WindowHandle.window.create_oval(item[1][0],item[1][1],item[1][2],item[1][3], fill= item[3])
			elif item[0] == "rectangle":
				item[2].shape = WindowHandle.window.create_rectangle(item[1][0],item[1][1],item[1][2],item[1][3], fill= item[3])
			if perf_counter() - start > (fps_limit/2):
				break

from managers import *
from basegameentity import *
from time import perf_counter