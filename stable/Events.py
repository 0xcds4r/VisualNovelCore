from Log import Log
import pygame

class Events():
	def __init__(self, core):
		Log.print("Initializing Events..")
		self.core = core
		self.keyPressed = ''
		self.keyUp = ''
	
	def getCore(self):
		return self.core

	def getKeyPressed(self):
		return self.keyPressed

	def getKeyUp(self):
		return self.keyUp

	def handle(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			elif event.type == pygame.KEYDOWN:
				if self.keyUp == pygame.key.name(event.key):
					self.keyUp = ''
				self.keyPressed = pygame.key.name(event.key)
			elif event.type == pygame.KEYUP:
				if self.keyPressed == pygame.key.name(event.key):
					self.keyUp = self.keyPressed
				self.keyPressed = ''
		return True