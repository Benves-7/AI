from tkinter import *
from config import *
from managers import *
from time import perf_counter

class Window:
	mapHandle = None
	unitlist = []
	exploredID = []

	window = None
	heigthP = None
	widthP = None
	indentX = 0
	indentY = 0
	#Load the window size from the config
	def __init__(self):
		self.heigthP = Configuration.config["windowParams"]["height"]
		self.widthP = Configuration.config["windowParams"]["width"]
	#Draw a rectangle for each node in the map
	def drawWindow(self, mapHandle, nodes):
		Window.mapHandle = self.mapHandle = mapHandle
		self.tk = tk = Tk()
		Window.window = window = Canvas(tk, width= self.widthP, height= self.heigthP)
		tk.title("AI TEST")
		window.pack()
		#self.window.master.geometry(Configuration.config["windowParams"]["moveWindow"])
		Window.indentX = xIndent = self.indentX = self.widthP/mapHandle.width
		Window.indentY = yIndent = self.indentY = self.heigthP/mapHandle.heigth

		window.create_rectangle(0,0, self.widthP, self.heigthP, fill="lawn green")

		for y in range(0,mapHandle.heigth):
			for x in range(0,mapHandle.width):
				node = nodes[x+(y*mapHandle.width)]
				node.pos = [(x*xIndent)+(xIndent/2), (y*yIndent)+(yIndent/2)]
				node.shape = window.create_rectangle(x*xIndent, y*yIndent, x*xIndent + xIndent, y*yIndent + yIndent, fill = 'gray')
				node.x = x
				node.y = y

				if(node.fogOfWar):
					window.itemconfig(node.shape, fill= 'gray50')
				else:
					window.itemconfig(node.shape, fill= node.color)

	def updateWindow(self):
		for unit in self.unitlist:
			delta = unit.getMove()
			self.window.move(unit.shape, delta[0], delta[1])
		start = perf_counter()
		for id in self.exploredID:
			tile = self.mapHandle.grid[id]
			if tile.type == "ground":
				self.window.delete(tile.shape)
			else:
				self.window.itemconfig(tile.shape, fill= tile.color)
				if tile.type == "tree":
					for tree in tile.trees:
						pos = tree.pos
						self.window.create_oval(pos[0], pos[1], pos[2], pos[3], fill= "green3")
			self.exploredID.remove(id)
			if perf_counter()-start > 0.016:
				break
			
		self.window.update()

