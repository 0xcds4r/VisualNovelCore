from VNCore import *
from Log import *
from Render import *
from RectWrapper import *
import time
import cProfile

class Game():
	def __init__(self, engine):
		self.engine = engine
		self.mmData = None
		self.pmData = None
		self.scrData = None
		self.scriptLoader = self.getEngine().getScriptLoader()
		self.scenes = self.getEngine().getScenes()
		self.sceneView = self.scenes.getSceneView()
		self.render = self.getEngine().getRender()
		self.sprites = self.render.getSprites()
		self.events = self.getEngine().getEvents()

	def getEngine(self):
		return self.engine

	def loadScripts(self):
		self.mmData = self.scriptLoader.loadScript("main_menu", "data/main_menu.json")
		self.pmData = self.scriptLoader.loadScript("pause_menu", "data/pause_menu.json")
		self.scrData = self.scriptLoader.loadScript("scenes", "data/script.json")

	def loadScenes(self):
		self.scenes.addSceneFromScriptData(self.scrData)
		if self.sceneView.getCurrentScene() == None:
			self.render.fade()
			self.sceneView.setCurrentScene(self.scenes.getScene("intro"))
			self.sceneView.showScene(True)

	def drawScenes(self):
		if not self.sceneView.isSceneShowing():
			return

		if self.sceneView.getCurrentScene():
			scene_data =  self.sceneView.getCurrentScene().getData()
			sprite_rect = RectWrapper(0, 0, 1920, 1080)
			sprite = self.sprites.load_sprite_r(scene_data['background'], sprite_rect)

	def process(self):
		if self.events.getKeyUp() == 'escape':
			self.getEngine().stopGame()

		self.loadScripts()
		self.loadScenes()
		self.drawScenes()

def runEngine():
	engine = VNCore()
	
	engine.getRender().setFlags([
		RenderFlags.USE_DEFAULT_DISPLAY_FLAGS, 
		RenderFlags.USE_DEFAULT_SURFACE_FLAGS, 
		RenderFlags.DONT_LOAD_DEFAULT_FONT
	])
	
	# engine.getRender().addFlag(RenderFlags.USE_VSYNC)
	# engine.getRender().setDisplayFlags(pygame.FULLSCREEN | pygame.OPENGL | pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE);
	# engine.getRender().setSurfaceFlags(pygame.SRCALPHA);
	
	engine.getRender().setScreenSize((1920, 1080))
	engine.getRender().Initialize()
	engine.startGame()
	
	game = Game(engine)

	while engine.isGameRunning():
		engine.process()
		game.process()
		time.sleep(0.01)

	engine.quitGame()

if __name__ == '__main__':
	profiler = cProfile.Profile()
	profiler.enable()

	runEngine()

	profiler.disable()
	profiler.print_stats(sort='cumtime')