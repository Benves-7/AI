import json
#Class for loading json config file
class Configuration:
	config = {}
	
	def open():
		with open("config.json") as fobj:
			Configuration.config = json.load(fobj)