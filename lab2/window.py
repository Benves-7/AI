from tkinter import *
from config import *

class Window:
	mapHandle = None

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

		for y in range(0,mapHandle.heigth):
			for x in range(0,mapHandle.width):
				shape = window.create_rectangle(x*xIndent, y*yIndent, x*xIndent + xIndent, y*yIndent + yIndent, fill = 'gray')
				node = nodes[x+(y*mapHandle.width)]
				node.x = x
				node.y = y

				if(node.fogOfWar):
					window.itemconfig(shape, fill = 'gray50')
				else:
					window.itemconfig(shape, fill = node.color)
				

	def updateWindow(self):
		self.window.update()

