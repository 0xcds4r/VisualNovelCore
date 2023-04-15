import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import *
import time
from pygame import mixer
import threading

SPRITE_TEX = "assets/items/sprite.png"

# todo in future
class GLRender():
	def __init__(self, engine, width, height):
		threading.Thread.__init__(self)
		self.width = width
		self.height = height
		self.display = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
		self.textures = {}
		self.init_pygame()
		self.init_opengl()
		self.load_textures()
		self.running = True

	def load_textures(self):
		self.sprite_texture = self.load_texture(SPRITE_TEX)

	def init_pygame(self):
		pygame.init()
		mixer.init()
		
	def init_opengl(self):
		glViewport(0, 0, self.width, self.height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, self.width, 0, self.height, -1, 1)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glEnable(GL_TEXTURE_2D)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
	def start_render(self):
		glClearColor(0.0, 0.0, 0.0, 0.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
	def end_render(self):
		pygame.display.flip()
		pygame.time.wait(10)
		
	def get_texture_size(self, texture_id):
		return self.textures[texture_id][1], self.textures[texture_id][2]

	def draw_texture(self, name, texture, x, y, width=None, height=None):
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, texture)
		glBegin(GL_QUADS)
		if width is None or height is None:
			width, height = self.get_texture_size(name)
		glTexCoord2f(0, 0)
		glVertex2f(x, y)
		glTexCoord2f(1, 0)
		glVertex2f(x + width, y)
		glTexCoord2f(1, 1)
		glVertex2f(x + width, y + height)
		glTexCoord2f(0, 1)
		glVertex2f(x, y + height)
		glEnd()
		glDisable(GL_TEXTURE_2D)

	def find_texture_in_cache(self, filename):
		for texture in self.textures:
			if texture[0] == filename:
				return texture
		return None

	def load_texture(self, filename):
		if filename in self.textures:
			return self.textures[filename][0]

		surface = pygame.image.load(filename).convert_alpha()
		texture_data = pygame.image.tostring(surface, 'RGBA', 1)
		texture_width, texture_height = surface.get_size()
		texture_id = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture_id)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_width, texture_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		self.textures[filename] = (texture_id, texture_width, texture_height)
		return texture_id

	def render(self):
		self.start_render()
		self.draw_texture(SPRITE_TEX, self.sprite_texture, 15, 15, 100, 100)
		self.end_render()

	def event_handle(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			
	def run(self):
		while self.running:
			self.event_handle()
			self.render()
			time.sleep(0.01)
		pygame.quit()

	def stop(self):
		self.running = False