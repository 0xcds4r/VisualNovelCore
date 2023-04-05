from VNCore import *
from Log import *
from Render import *
from RectWrapper import *

class Game:
	def __init__(self, engine):
		self.engine = engine
		self.engine.getRender().setFlags([RenderFlags.USE_DEFAULT_DISPLAY_FLAGS, RenderFlags.USE_DEFAULT_SURFACE_FLAGS, RenderFlags.DONT_LOAD_DEFAULT_FONT, RenderFlags.DONT_AUTO_RENDER_IMAGES])
		self.engine.getRender().setScreenSize((1920, 1080))
		self.engine.getRender().Initialize()
		self.engine.startGame()

STOP_GAME = False
def stopGame():
	print("Stopping the game..")
	global STOP_GAME
	STOP_GAME = True

def runEngine():
    engine = VNCore()
    game = Game(engine)

    engine.getEvents().register_key_up_handler(pygame.K_ESCAPE, stopGame) # You released the button

    while not STOP_GAME:
        engine.process()

    engine.quitGame()

if __name__ == '__main__':
    runEngine()