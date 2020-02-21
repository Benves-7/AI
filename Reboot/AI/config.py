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

# Class for handling and storing data for the window and shapes.
class WindowHandle:
	tk = None					# the window
	window = None				# the canvas
	background = None			# background image (used to save graphic time) *(hopefully)
	windowSize = []				# [x, y]
	indent = []					# [x, y]

	exploredTiles = []

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
				tile = MapHandle.grid[x+(y*MapHandle.width)]
				tile.xy = [x, y]
				ix=x*indent[0]
				iy=y*indent[1]
				tile.position = [(ix)+(indent[0]/2), (iy)+(indent[1]/2)]
				if tile.fogOfWar:
					tile.shape = WindowHandle.window.create_rectangle(ix, iy, ix+indent[0], iy+indent[1], fill= 'gray', outline= "")
				if tile.isTree:
					tile.addTrees()

	def createMapImage():
		img = Image.open(Config.config["mapimage"])
		img = img.resize((WindowHandle.windowSize[0], WindowHandle.windowSize[1]))
		img.save("newimg.ppm", "ppm")


		WindowHandle.background = itk.PhotoImage(file= 'newimg.ppm')
		WindowHandle.window.create_image(0,0, anchor=NW, image= WindowHandle.background)
		
	def update():

		for tile in WindowHandle.exploredTiles:
			WindowHandle.window.delete(tile.shape)

		WindowHandle.window.update()

from basegameentity import *
from managers import *