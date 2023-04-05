import pygame
from Log import Log
import time
import threading

VIDEO_MODES = [(1920, 1080), (1680, 1050), (1600, 1024), (1600, 900), (1440, 900), (1366, 768), (1360, 768), (1280, 1024), (1280, 960), (1280, 800), (1280, 768), (1280, 720), (1176, 664), (1152, 864), (1024, 768), (800, 600), (720, 576), (720, 480), (640, 480)]

class RenderFlags:
	USE_VSYNC = 555
	DONT_LOAD_DEFAULT_FONT = 111
	USE_DEFAULT_DISPLAY_FLAGS = 444
	USE_DEFAULT_SURFACE_FLAGS = 222
	DONT_AUTO_RENDER_IMAGES = 999

class Sprites():
	def __init__(self, core):
		Log.print("Initializing Sprites..")
		self.core = core
		self.sprites = pygame.sprite.Group()

	def getCore(self):
		return self.core

	def draw(self):
		self.sprites.draw(self.getCore().getRender().getDisplay())

	def setSpritePosition(self, sprite, pos):
		if sprite in self.sprites:
			sprite.rect.x, sprite.rect.y = pos
		else:
			Log.print(f"Sprite ({sprite}) not loaded!")

	def setSpriteSize(self, sprite, size):
		if sprite in self.sprites:
			sprite.rect.width, sprite.rect.height = size
			sprite.image = pygame.transform.scale(sprite.image, (sprite.rect.width, sprite.rect.height))
		else:
			Log.print(f"Sprite ({sprite}) not loaded!")

	def setSpriteRect(self, sprite, rect):
		if sprite in self.sprites:
			sprite.rect = rect
			sprite.image = pygame.transform.scale(sprite.image, (sprite.rect.width, sprite.rect.height))
		else:
			Log.print(f"Sprite ({sprite}) not loaded!")

	def unload_sprite(self, sprite):
		if sprite in self.sprites:
			self.sprites.remove(sprite)
			self.sprites.update()
		else:
			Log.print(f"Sprite ({sprite}) not loaded!")

	def load_sprite(self, filename):
		image = self.getCore().getRender().load_image(filename)
		sprite = pygame.sprite.Sprite()
		sprite.image = image
		img_rect = image.get_rect()
		image = pygame.transform.scale(image, (img_rect.width, img_rect.height))
		sprite.rect = img_rect
		self.sprites.add(sprite)
		return sprite

	def load_sprite_r(self, filename, rect):
		image = self.getCore().getRender().load_image(filename)
		image = pygame.transform.scale(image, (rect.width, rect.height))
		sprite = pygame.sprite.Sprite()
		sprite.image = image
		sprite.rect = rect
		self.sprites.add(sprite)
		return sprite

	def load_sprites(self, directory):
		for filename in os.listdir(directory):
			if filename.endswith('.png') or filename.endswith('.jpg'):
				self.load_sprite(os.path.join(directory, filename))

class Render():
	def __init__(self, core):
		Log.print("Initializing Render..")
		self.core = core
		self.width = 1920
		self.height = 1080
		self.fonts = []
		self.surface = None
		self.screen = None
		self.clock = None
		self.sprites = None
		self.render_flags = []
		self.images = {}
		self.displayFlags = 0
		self.surfaceFlags = 0
		self.renderQueue = {}

	def hasDisplayFlags(self):
		if not int(self.displayFlags) == 0:
			return True
		return False

	def hasSurfaceFlags(self):
		if not int(self.surfaceFlags) == 0:
			return True
		return False

	def setDisplayFlags(self, flags):
		self.displayFlags = flags

	def setSurfaceFlags(self, flags):
		self.surfaceFlags = flags

	def setScreenSize(self, size):
		self.width, self.height = size

	def setFlags(self, flags):
		self.render_flags = flags

	def addFlag(self, flag):
		self.render_flags.append(flag)

	def clearFlags(self):
		self.render_flags = []

	def getFlagState(self, flag):
		if flag in self.render_flags:
			return True
		return False

	def Initialize(self):
		pygame.init()

		if self.getFlagState(RenderFlags.USE_DEFAULT_DISPLAY_FLAGS):
			Log.print("Using default display flags")
			self.setDisplayFlags(pygame.RESIZABLE | pygame.DOUBLEBUF)
		else:
			if not self.hasDisplayFlags():
				Log.print("[bold red]Warning: no display flags[/]")

		if self.getFlagState(RenderFlags.USE_DEFAULT_SURFACE_FLAGS):
			Log.print("Using default surface flags")
			self.setSurfaceFlags(pygame.SRCALPHA)
		else:
			if not self.hasSurfaceFlags():
				Log.print("[bold red]Warning: no surface flags[/]")

		self.screen = pygame.display.set_mode(self.getScreenSize(), self.getDisplayFlags(), vsync=self.isVSyncEnabled())
		self.surface = pygame.Surface(self.getScreenSize(), self.getSurfaceFlags())
		self.clock = pygame.time.Clock()
		self.sprites = Sprites(self.core)

		self.surface.fill((0,0,0))
		self.surface.set_alpha(0)

		self.alpha_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
		self.alpha_surface.fill((255, 255, 255))  # Fill with a transparent white color
		self.alpha_surface.set_alpha(0)

		if not self.getFlagState(RenderFlags.DONT_LOAD_DEFAULT_FONT):
			self.loadDefaultFont()

	def getSprites(self):
		return self.sprites

	def fade(self):
		# todo
		return

	def renderFade(self):
		# todo
		return
		
	def renderAll(self):
		self.clock.tick(60)
		
		self.getDisplay().fill((255, 255, 255))

		if not self.getFlagState(RenderFlags.DONT_AUTO_RENDER_IMAGES):
			self.getSprites().draw()
			self.renderImages()

		self.renderRQ()
		self.getCore().callLuaEventInAll("onGameRender")

		pygame.display.flip()

		pygame.display.update()
		return True

	def renderRQ(self):
		for data_name in list(self.renderQueue):
			surface = self.renderQueue[data_name][0]
			pos = self.renderQueue[data_name][1]
			self.renderSurface(surface, pos)
			del self.renderQueue[data_name]

	def resizeImage(self, image):
		img_rect = image.get_rect()
		image = pygame.transform.scale(image, (img_rect.width, img_rect.height))
		return image

	def setSizeImage(self, image, w, h):
		image = pygame.transform.scale(image, (w, h))
		return image

	def addSurfaceToRenderQueue(self, tag, _surface, pos=(0,0)):
		self.renderQueue[tag] = (_surface, pos)

	def renderSurface(self, _surface, pos=(0,0)):
		self.getDisplay().blit(_surface, pos)

	def renderImages(self):
		for data in self.images:
			self.renderSurface(self.images[data], (0,0))

	def loadDefaultFont(self):
		Log.print("Loading default font..")
		self.loadFont("assets", "arial.ttf", 20, False)

	def load_image(self, filename):
		if filename not in self.images:
		    self.images[filename] = pygame.image.load(filename).convert_alpha()
		return self.images[filename]

	def getScreenSize(self):
		return (self.width, self.height)

	def getClock(self):
		return self.clock

	def getDisplay(self):
		return self.screen

	def getSurface(self):
		return self.surface

	def getDisplayFlags(self):
		return self.displayFlags

	def getSurfaceFlags(self):
		return self.surfaceFlags

	def isVSyncEnabled(self):
		if not self.getFlagState(RenderFlags.USE_VSYNC):
			return 0

		Log.print("[bold red]Warning: VSync enabled![/]")
		return 1

	def getFonts(self):
		return self.fonts

	def getFontByName(self, name):
		if len(self.fonts) == 0:
			return None

		for font_name, font_size, font in self.fonts:
			if font_name == name:
				return font
		return None

	def getFontSize(self, fontPtr):
		if len(self.fonts) == 0:
			return -1

		for font_name, font_size, font in self.fonts:
			if font == fontPtr:
				return font_size
		return -1

	def getFontSizeByName(self, name):
		if len(self.fonts) == 0:
			return -1

		for font_name, font_size, font in self.fonts:
			if font_name == name:
				return font_size
		return -1

	def getFontName(self, fontPtr):
		if len(self.fonts) == 0:
			return None

		for font_name, font_size, font in self.fonts:
			if fontPtr == font:
				return font_name
		return None

	def loadFont(self, font_path, font_name, font_size, logging=True):
		if logging == True:
			Log.print(f"Loading font from {font_path}: {font_name} (size: {font_size})")
		font = pygame.font.Font(font_path + "/" + font_name, font_size)
		if font is not None:
			self.fonts.append((font_name, font_size, font))
		else:
			Log.print(f"Error while loading font: {font_name}")

		return font

	def getCore(self):
		return self.core