import pygame
from pygame import mixer
import time
import threading

from Log import Log
from SpritesRender import Sprites
from TextRender import TextRender
from FontHelper import FontHelper
from ImageRender import ImageRender
from Animation import AnimationRenderer, Animation, FadeAnimation

# render flags
from RenderData import *

# video modes
VIDEO_MODES = [(1920, 1080), (1680, 1050), (1600, 1024), (1600, 900), (1440, 900), (1366, 768), (1360, 768), (1280, 1024), (1280, 960), (1280, 800), (1280, 768), (1280, 720), (1176, 664), (1152, 864), (1024, 768), (800, 600), (720, 576), (720, 480), (640, 480)]

class RenderFlags:
	def __init__(self):
		self.render_flags = 0

	def reset_flags(self):
		self.render_flags = 0

	def add_flag(self, flag):
		self.render_flags |= flag

	def set_flags_by_args(self, *flag_consts):
		for flag_const in flag_consts:
			self.render_flags |= flag_const

	def set_flag_state(self, flag, value):
		if value:
			self.render_flags |= flag
		else:
			self.render_flags &= ~flag

	def set_flags(self, *flag_expr):
		flag_consts = []
		for flag in flag_expr:
			if isinstance(flag, int):
				flag_consts.append(flag)
			elif isinstance(flag, str):
				for const_name in flag.split('|'):
					const_name = const_name.strip()
					if const_name.startswith('FLAG_'):
						const_value = globals().get(const_name)
						if const_value is not None:
							flag_consts.append(const_value)

		for flag_const in flag_consts:
			self.render_flags |= flag_const

	def is_flag_set(self, flag_const):
		if self.render_flags == 0:
			return False

		return bool(self.render_flags & flag_const)

class Render():
	def __init__(self, core):
		Log.print("Initializing Render..")
		self.core = core
		self.textRender = TextRender(self.core)
		self.fontHelper = FontHelper(self.core)
		self.renderFlags = RenderFlags()
		self.width = 1920
		self.height = 1080
		self.surface = None
		self.screen = None
		self.clock = None
		self.sprites = None
		self.imageRender = ImageRender(self.core)
		self.animationRenderer = AnimationRenderer(self.core)
		self.displayFlags = 0
		self.surfaceFlags = 0
		self.renderQueue = {}

	def getAnimationManager(self):
		return self.animationRenderer

	def getImageManager(self):
		return self.imageRender

	def getRenderFlags(self):
		return self.renderFlags

	def getSpritesManager(self):
		return self.sprites

	def getFontManager(self):
		return self.fontHelper

	def getTextManager(self):
		return self.textRender

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

	def setScreenSize(self, x, y):
		self.width, self.height = x, y

	def Initialize(self):
		pygame.init()
		mixer.init()

		if self.getRenderFlags().is_flag_set(FLAG_USE_DEFAULT_DISPLAY_FLAGS):
			Log.print("Using default display flags")
			self.setDisplayFlags(pygame.RESIZABLE | pygame.DOUBLEBUF)
		else:
			if not self.hasDisplayFlags():
				Log.print("[bold red]Warning: no display flags[/]")

		if self.getRenderFlags().is_flag_set(FLAG_USE_DEFAULT_SURFACE_FLAGS):
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

		if not self.getRenderFlags().is_flag_set(FLAG_DONT_LOAD_DEFAULT_FONT):
			self.getFontManager().loadDefaultFont()
		
	def renderNonRQ(self):
		if not self.getRenderFlags().is_flag_set(FLAG_DONT_AUTO_RENDER_IMAGES):
			self.getSpritesManager().draw()
			self.getImageManager().renderImages()

	def renderAll(self):
		dt = self.clock.tick(60) / 1000.0
		self.getAnimationManager().update(dt)
		self.getDisplay().fill((255, 255, 255))

		self.renderNonRQ()
		self.renderRQ()
		self.getAnimationManager().draw_all()

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

	def addSurfaceToRenderQueue(self, tag, _surface, pos=(0,0)):
		self.renderQueue[tag] = (_surface, pos)

	def addSurfaceToRenderQueuePos(self, tag, _surface, x=0, y=0):
		self.renderQueue[tag] = (_surface, (x,y))

	def renderSurface(self, _surface, pos=(0,0)):
		self.getDisplay().blit(_surface, pos)

	def getScreenSize(self):
		return (self.width, self.height)

	def getScreenWidth(self):
		return self.width

	def getScreenHeight(self):
		return self.height

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
		if not self.getRenderFlags().is_flag_set(FLAG_USE_VSYNC):
			return 0

		Log.print("[bold red]Warning: VSync enabled![/]")
		return 1

	def addRect(self, name = "rect", r = 255, g = 255, b = 255, a = 255, x = 0, y = 0, width = 100, height = 100):
		temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)
		temp_surface.fill((r, g, b, a))
		self.addSurfaceToRenderQueue(name, temp_surface, (x, y))

	def addCircle(self, name = "circle", x = 0, y = 0, r = 255, g = 255, b = 255, a = 255, radius = 2.0, bx = 0, by = 0, bw = 0, bh = 0, border_width=0, br = 0, bg = 0, bb = 0, ba = 0):
		circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(circle_surface, (r,g,b,a), (radius, radius), radius)

		if border_width > 0:
			pygame.draw.circle(circle_surface, (br, bg, bb, ba), (radius, radius), radius, border_width)

		if bx != 0 and bw != 0:
			bounds_surface = pygame.Surface((bw, bh), pygame.SRCALPHA)
			self.addSurfaceToRenderQueue(name + "_bounds", bounds_surface, (bx, by))
			self.addSurfaceToRenderQueue(name, circle_surface, (bx + x - radius, by + y - radius))

		self.addSurfaceToRenderQueue(name, circle_surface, (x - radius, y - radius))
			

	def getCore(self):
		return self.core