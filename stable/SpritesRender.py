from Log import Log
import pygame

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