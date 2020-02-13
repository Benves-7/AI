#Loads a file and separated into a list of line
class FileImporter:
	def loadFile(path):
		with open(path, 'r') as x:
			list = x.read().splitlines()
		return list