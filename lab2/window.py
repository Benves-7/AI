from tkinter import *
from config import *
class Window:
	window = None
	heigthP = None
	widthP = None
	xIndent = 0
	yIndent = 0
	indentX = 0
	indentY = 0
	#Load the window size from the config
	def __init__(self):
		self.heigthP = Configuration.config["windowParams"]["height"]
		self.widthP = Configuration.config["windowParams"]["width"]
	#Draw a rectangle for each node in the map
	def drawWindow(self, width, heigth, nodes):
		self.tk = tk = Tk()
		self.window = window = Canvas(tk, width= self.widthP, height= self.heigthP)
		tk.title("AI TEST")
		window.pack()
		#self.window.master.geometry(Configuration.config["windowParams"]["moveWindow"])
		xIndent = self.indentX = self.widthP/width
		yIndent = self.indentY = self.heigthP/heigth

		for y in range(0,heigth):
			for x in range(0,width):
				shape = window.create_rectangle(x*xIndent, y*yIndent, x*xIndent + xIndent, y*yIndent + yIndent, fill = 'gray')
				node = nodes[x+(y*width)]
				node.x = x
				node.y = y

				if(node.fogOfWar):
					window.itemconfig(shape, fill = 'gray50')
				else:
					window.itemconfig(shape, fill = node.color)
				

	def updateWindow(self):
		self.window.update()

