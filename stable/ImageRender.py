from Log import Log
import pygame

class ImageRender:
	def __init__(self, core):
		Log.print("Initializing ImageRender..")
		self.core = core
		self.images = {}

	def getCore(self):
		return self.core

	def resizeImage(self, image):
		img_rect = image.get_rect()
		image = pygame.transform.scale(image, (img_rect.width, img_rect.height))
		return image

	def setImagePos(self, image, x, y):
		rect = image.get_rect()
		rect.x = x
		rect.y = y
		return image
	
	def setImageSize(self, image, w, h):
		image = pygame.transform.scale(image, (w, h))
		return image

	def renderImages(self):
		for data in self.images:
			self.renderSurface(self.images[data], (0,0))
	
	def load_image(self, filename):
		if filename not in self.images:
		    self.images[filename] = pygame.image.load(filename).convert_alpha()
		return self.images[filename]