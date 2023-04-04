from Events import Events
from ScriptLoader import ScriptLoader
from Render import Render
from Scenes import *
from MenuSystem import MenuSystem
from Log import Log
from LuaWrapper import *
import pygame
import os

class VNCore():
	def __init__(self):
		Log.print("Initializing Visual Novel Core..")
		self.events = Events(self)
		self.render = Render(self)
		self.menuSystem = MenuSystem(self) 
		self.scriptLoader = ScriptLoader(self)
		self.scenes = Scenes(self)
		self.running = False
		self.luapath = 'scripts/'
		self.luadirectories = os.listdir(self.luapath)
		for file in self.luadirectories:
			self.luaWrapper = LuaWrapper(self, self.luapath + file)

	def getLuaWrapper(self):
		return self.luaWrapper

	def getEvents(self):
		return self.events

	def getRender(self):
		return self.render

	def getScriptLoader(self):
		return self.scriptLoader

	def getScenes(self):
		return self.scenes

	def stopGame(self):
		self.running = False

	def isGameRunning(self):
		return self.running

	def startGame(self):
		self.running = True

	def quitGame(self):
		pygame.quit()

	def process(self):
		if self.getEvents() is not None:
			self.running = self.getEvents().handle()
		if self.getRender() is not None:
			self.running = self.getRender().renderAll()

def print_about():
	Log.printL("\n-------------------------------------------------------------------------")
	Log.printL("\t[bold white]Visual Novel Core v0.3-stable[/]", True)
	Log.printL("\t[bold white]Author -> 0xcds4r[/]", True)

	Log.printL("\t[bold white]itch.io ->[/] [link=https://0xcds4r.itch.io/visual-novel-core]https://0xcds4r.itch.io/visual-novel-core[/link]", True)
	Log.printL("-------------------------------------------------------------------------\n", True)

print_about()