from Log import Log

class MenuSystem:
	def __init__(self, core):
		Log.print("Initializing MenuSystem..")
		self.core = core

	def getCore(self):
		return self.core
		