from Log import Log
import pygame

class FontHelper:
	def __init__(self, core):
		Log.print("Initializing FontHelper..")
		self.core = core
		self.fonts = []
		self.fontsDefaultFolder = "assets"
		self.fontsDefaultFontName = "arial.ttf"

	def getCore(self):
		return self.core

	def setDefaultFolder(self, dir):
		self.fontsDefaultFolder = dir

	def setDefaultFontName(self, name):
		self.fontsDefaultFontName = name

	def loadDefaultFont(self):
		Log.print("Loading default font..")
		self.loadFont(self.fontsDefaultFolder, self.fontsDefaultFontName, 20, False)

	def getDefaultFontPath(self):
		return self.fontsDefaultFolder + "/" + self.fontsDefaultFontName

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
		