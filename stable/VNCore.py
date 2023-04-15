from Events import Events
from ScriptLoader import ScriptLoader
from Render import Render
from Scenes import Scenes, Scene, SceneView
from MenuSystem import MenuSystem
from Log import Log
from LuaWrapper import LuaWrapper
from Audio import AudioManager
from FileManager import FileManager
import pygame
import os
import sys
import threading
import multiprocessing
import time

VNC_VERSION = "0.6.1"
VNC_VERSION_CODE = 61
VNC_VERSION_TAG = "patch"

class VNCore():
	def __init__(self):
		Log.print("Initializing Visual Novel Core..")
		self.script_dir = 'scripts/'
		self.lua_scripts = []
		self.fps = 60
		self.render_thread = threading.Thread(target=self.graphicProcess, daemon=True)
		self.running = False
		self.init_classes()

	def getVersion(self):
		return VNC_VERSION

	def getVersionTag(self):
		return VNC_VERSION_TAG

	def getVersionCode(self):
		return VNC_VERSION_CODE

	def checkVersionCode(self, code):
		if code <= 0:
			return -2

		if code > self.getVersionCode():
			return -1

		if code == self.getVersionCode():
			return 1

		if code < self.getVersionCode():
			return 0

	def setFPS(self, fps):
		self.fps = fps

	def getFPS(self):
		return self.fps

	def getFPSDeltaTime(self):
		return 1/self.fps

	def init_classes(self):
		self.events = Events(self)
		self.render = Render(self)
		self.menuSystem = MenuSystem(self) 
		self.scriptLoader = ScriptLoader(self)
		self.scenes = Scenes(self)
		self.audioManager = AudioManager(self)
		self.fileManager = FileManager()
		self.loadLuaScripts()

	def getFileManager(self):
		return self.fileManager

	def getAudioManager(self):
		return self.audioManager

	def loadLuaScripts(self):
		for file in os.listdir(self.script_dir):
			if file.endswith('.lua') or file.endswith('.luac'):
				script_path = os.path.join(self.script_dir, file)
				script = LuaWrapper(self, file, script_path)
				self.lua_scripts.append((file, script))

	def loadLuaScript(self, path, file):
		script_path = os.path.join(self.script_dir, path + "/" + file)
		script = LuaWrapper(self, file, script_path)
		self.lua_scripts.append((file, script))

	def callLuaEvent(self, name, eventName, *args):
		for data in self.lua_scripts:
			script_name = data[0]
			script = data[1]
			if script_name == name:
				func = script.lua.globals()[eventName]
				if func is not None:
					func(*args)

	def callLuaEventInAll(self, eventName, *args):
		for data in self.lua_scripts:
			script_name = data[0]
			script = data[1]
			func = script.lua.globals()[eventName]
			if func is not None:
				func(*args)

	def getLuaWrapper(self):
		return self.luaWrapper

	def GetTickCount(self):
		return int(round(time.time() * 1000))

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

	def graphicProcess(self):
		while self.running:
			self.getRender().renderAll()

	def startGame(self):
		self.callLuaEventInAll("onGameStart")
		self.running = True
		self.process()

	def quitGame(self):
		pygame.quit()
		sys.exit()

	def onMouseClickEvent(self, event):
		self.callLuaEventInAll("onTouchEvent", event.button, event.pos[0], event.pos[1])

	def onMouseKeyUp(self, event):
		self.callLuaEventInAll("onTouchEndEvent", event.button, event.pos[0], event.pos[1])

	def onMouseMoveEvent(self, mouse_pos):
		self.callLuaEventInAll("onTouchMoveEvent", mouse_pos[0], mouse_pos[1])

	def eventProcess(self):
		while self.running:
			# Обработка событий Pygame здесь
			event_failed = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					event_failed = True
					break
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.onMouseClickEvent(event)

				if event.type == pygame.MOUSEBUTTONUP:
					self.onMouseKeyUp(event)

				if event.type == pygame.MOUSEMOTION:
					mouse_pos = pygame.mouse.get_pos()
					self.onMouseMoveEvent(mouse_pos)

				if not self.getEvents().handle(event):
					self.running = False
					event_failed = True
					break

			if event_failed:
				break

			pygame.time.Clock().tick(self.fps)

		self.quitGame()

	def process(self):
		if not self.render_thread or not self.render_thread.is_alive():
			self.render_thread = threading.Thread(target=self.graphicProcess, daemon=True)
			self.render_thread.start()
		self.eventProcess()

	def setTitle(self, title='VNCore Game'):
		pygame.display.set_caption(title)

	def setIcon(self, icon_img):
		pygame.display.set_icon(icon_img)

def print_about():
	Log.printL("\n-------------------------------------------------------------------------")
	Log.printL(f"\t[bold white]Visual Novel Core v{VNC_VERSION}-{VNC_VERSION_TAG}[/]", True)
	Log.printL("\t[bold white]Author -> 0xcds4r[/]", True)

	Log.printL("\t[bold white]itch.io ->[/] [link=https://0xcds4r.itch.io/visual-novel-core]https://0xcds4r.itch.io/visual-novel-core[/link]", True)
	Log.printL("-------------------------------------------------------------------------\n", True)

print_about()