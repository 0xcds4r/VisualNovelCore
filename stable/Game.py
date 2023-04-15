from VNCore import *

class Game(VNCore):
	def __init__(self):
		super().__init__()
		self.printNotifies()

	def printNotifies(self):
		self.getRender().notify("Welcome to Visual Novel Core DEMO!", (1920 / 2 - 5) - (self.getRender().getTextManager().getTextWidth("Welcome to Visual Novel Core DEMO!", "assets/arial.ttf", 44) / 2 - 5), 1080 / 2, 255, 255, 255, 255, 25,0,0,255, "assets/arial.ttf", 44, 2500)
		self.getRender().notify("VNCore developed by 0xcds4r", (1920 / 2 - 5) - (self.getRender().getTextManager().getTextWidth("Welcome to Visual Novel Core DEMO!", "assets/arial.ttf", 44) / 2 - 5), 1080 / 1.8, 255, 255, 255, 255, 25,0,0,0, "assets/arial.ttf", 44, 2550)

	def process(self):
		super().process()