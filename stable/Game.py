from VNCore import *
from Log import *
from Render import *
from RectWrapper import *

class Game:
	def __init__(self, engine):
		self.engine = engine
		self.scriptLoader = self.engine.getScriptLoader()
		self.scenes = self.engine.getScenes()
		self.sceneView = self.scenes.getSceneView()
		self.render = self.engine.getRender()
		self.sprites = self.render.getSprites()
		self.events = self.engine.getEvents()
		self.sceneCounter = 0

	def loadScripts(self):
		self.mmData = self.scriptLoader.loadScript("main_menu", "data/main_menu.json")
		self.pmData = self.scriptLoader.loadScript("pause_menu", "data/pause_menu.json")
		self.scrData = self.scriptLoader.loadScript("scenes", "data/script.json")

	def nextScene(self, skip=1):
		Log.print("scene next")
		self.sceneView.showScene(False)
		self.sceneCounter += skip
		self.updateScene()
		Log.print("sceneCounter -> " + str(self.sceneCounter))

	def loadScenes(self):
		self.scenes.addSceneFromScriptData(self.scrData)
		self.sceneCounter = 0
		self.updateScene()

	def updateScene(self):
		if self.sceneCounter == 0:
			self.sceneView.setCurrentScene(self.scenes.getScene("intro"))
		elif self.sceneCounter == 1:
			self.sceneView.setCurrentScene(self.scenes.getScene("goal"))
		else:
			stopGame()
		self.sceneView.showScene(True)

	def drawScenes(self):
		if not self.sceneView.isSceneShowing():
			return

		background = self.sceneView.getCurrentScene().getDataValue(key='background')
		if background is not None:
			sfImg = self.render.load_image(filename=background);
			sfImg = self.render.setSizeImage(image=sfImg, w=1920, h=1080)
			self.render.addSurfaceToRenderQueue(tag='bg', _surface=sfImg, pos=(0,0))

		# todo

	def sceneEvent(self):
		Log.print("sceneEvent")
		self.nextScene()

	def process(self):
		self.drawScenes()

STOP_GAME = False
def stopGame():
	print("Stopping the game..")
	global STOP_GAME
	STOP_GAME = True

def testFunc():
	print("test work")

def runEngine():
	# Init VNCore
    engine = VNCore()
    engine.getRender().setFlags([RenderFlags.USE_DEFAULT_DISPLAY_FLAGS, RenderFlags.USE_DEFAULT_SURFACE_FLAGS, RenderFlags.DONT_LOAD_DEFAULT_FONT, RenderFlags.DONT_AUTO_RENDER_IMAGES])
    engine.getRender().setScreenSize((1920, 1080))
    engine.getRender().Initialize()
    engine.startGame()

    # Init game class
    game = Game(engine)

    # Register keys
    engine.getEvents().register_key_down_handler(pygame.K_SPACE, game.sceneEvent) # You pressed the button
    engine.getEvents().register_key_up_handler(pygame.K_ESCAPE, stopGame) # You released the button
    engine.getEvents().register_long_key_down_handler(pygame.K_LEFT, testFunc) # You held the button
    
    # Loading scripts and scenes
    game.loadScripts()
    game.loadScenes()

    while not STOP_GAME:
        engine.process()
        game.process()

    engine.quitGame()

if __name__ == '__main__':
    runEngine()