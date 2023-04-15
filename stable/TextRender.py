from Log import Log
import pygame

class TextElement:
	def __init__(self, textMgr):
		self.textMgr = textMgr
		self.text = "Example Text"
		self.x = 0
		self.y = 0
		self.font = "assets/arial.ttf"
		self.size = 24
		self.align = 'left'
		self.bold = False
		self.italic = False
		self.text_color_r = 255
		self.text_color_g = 255
		self.text_color_b = 255
		self.text_color_a = 255
		self.bg_color_r = 0
		self.bg_color_g = 0
		self.bg_color_b = 0
		self.bg_color_a = 0
		self.stroke_color_r = 0
		self.stroke_color_g = 0
		self.stroke_color_b = 0
		self.stroke_color_a = 0
		self.stroke_width = 1
		self.alpha = 255

	def reset(self):
		self.alpha = 255

	def setAlign(self, align):
		self.align = align

	def setAlpha(self, alpha):
		self.alpha = alpha

	def getAlpha(self):
		return self.alpha

	def getAlign(self):
		return self.align

	def setPositionX(self, x):
		self.x = x

	def getPositionX(self):
		return self.x

	def setPositionY(self, y):
		self.y = y

	def getPositionY(self):
		return self.y

	def setPosition(self, x, y):
		self.x = x
		self.y = y

	def getPosition(self):
		return self.x, self.y

	def setText(self, text):
		self.text = text

	def getText(self):
		return self.text

	def setFont(self, path):
		self.font = path

	def getFont(self):
		return self.font

	def setFontSize(self, size):
		self.size = size

	def getFontSize(self):
		return self.size

	def setBold(self, bold):
		self.bold = bold

	def isBold(self):
		return self.bold

	def setItalic(self, italic):
		self.italic = italic

	def isItalic(self):
		return self.italic

	def setTextColor(self, r, g, b, a):
		self.text_color_r = r
		self.text_color_g = g
		self.text_color_b = b
		self.text_color_a = a

	def getTextColor(self, el):
		if el == 'r':
			return self.text_color_r

		if el == 'g':
			return self.text_color_g

		if el == 'b':
			return self.text_color_b

		if el == 'a':
			return self.text_color_a

		return 0

	def setBgColor(self, r, g, b, a):
		self.bg_color_r = r
		self.bg_color_g = g
		self.bg_color_b = b
		self.bg_color_a = a

	def getBgColor(self, el):
		if el == 'r':
			return self.bg_color_r

		if el == 'g':
			return self.bg_color_g

		if el == 'b':
			return self.bg_color_b

		if el == 'a':
			return self.bg_color_a

		return 0

	def setStrokeColor(self, r, g, b, a):
		self.stroke_color_r = r
		self.stroke_color_g = g
		self.stroke_color_b = b
		self.stroke_color_a = a

	def getStrokeColor(self, el):
		if el == 'r':
			return self.stroke_color_r

		if el == 'g':
			return self.stroke_color_g

		if el == 'b':
			return self.stroke_color_b

		if el == 'a':
			return self.stroke_color_a

		return 0

	def setStrokeWidth(self, width):
		self.stroke_width = width

	def getStrokeWidth(self):
		return self.stroke_width

	def draw(self):
		self.textMgr.addText(self.text, self.x, self.y, self.font, self.size, self.align, self.bold, self.italic, self.text_color_r, self.text_color_g, self.text_color_b, self.text_color_a, self.bg_color_r, self.bg_color_g, self.bg_color_b, self.bg_color_a, self.stroke_color_r, self.stroke_color_g, self.stroke_color_b, self.stroke_color_a, self.stroke_width)
		self.reset()

class TextRender:
	def __init__(self, core):
		Log.print("Initializing TextRender..")
		self.core = core
		self.textElement = TextElement(self)
		
	def getCore(self):
		return self.core

	def getTextElement(self):
		return self.textElement

	def getTextWidth(self, text, font_path, font_size):
		font = pygame.font.Font(font_path, font_size)
		text_surface = font.render(text, True, (255, 255, 255))
		return text_surface.get_width()

	def addText(self, text, x, y, font=None, size=24, align='left', bold=False, italic=False, r=255, g=255, b=255, a=255, bgr=0, bgg=0, bgb=0, bga=0, sr=0, sg=0, sb=0, sa=0, stroke_width=1):
		color = (r, g, b, a)

		background = None
		if bga != 0:
			background = (bgr, bgg, bgb, bga)

		stroke_color = None
		if sa != 0:
			stroke_color = (sr, sg, sb, sa)

		if font is None:
			return

		font_style = ""
		if bold:
			font_style += "bold "
		if italic:
			font_style += "italic "
		font_style = font_style.strip()

		font_obj = pygame.font.SysFont(font, size, bold=bold, italic=italic)
		if stroke_color is not None:
			stroke_font = pygame.font.SysFont(font, size, bold=bold, italic=italic)
			stroke_surface_t = stroke_font.render(text, True, stroke_color, background)
			stroke_surface_b = stroke_font.render(text, True, stroke_color)
			stroke_surface_l = stroke_font.render(text, True, stroke_color)
			stroke_surface_r = stroke_font.render(text, True, stroke_color)

			stroke_surface_tr = stroke_font.render(text, True, stroke_color)
			stroke_surface_tl = stroke_font.render(text, True, stroke_color)

			stroke_surface_br = stroke_font.render(text, True, stroke_color)
			stroke_surface_bl = stroke_font.render(text, True, stroke_color)

			text_surface = font_obj.render(text, True, color)
			text_surface.set_alpha(self.getTextElement().getAlpha())

			stroke_surface_t.set_alpha(self.getTextElement().getAlpha())
			stroke_surface_b.set_alpha(self.getTextElement().getAlpha())
			stroke_surface_l.set_alpha(self.getTextElement().getAlpha())
			stroke_surface_r.set_alpha(self.getTextElement().getAlpha())
			stroke_surface_tr.set_alpha(self.getTextElement().getAlpha())
			stroke_surface_tl.set_alpha(self.getTextElement().getAlpha())
			stroke_surface_br.set_alpha(self.getTextElement().getAlpha())
			stroke_surface_bl.set_alpha(self.getTextElement().getAlpha())
		else:
			text_surface = font_obj.render(text, True, color, background)
			text_surface.set_alpha(self.getTextElement().getAlpha())

		text_rect = text_surface.get_rect()
		if align == 'left':
			text_rect.left = x
		elif align == 'center':
			text_rect.centerx = x
		elif align == 'right':
			text_rect.right = x
		text_rect.top = y

		if stroke_surface_r is not None and stroke_surface_l is not None and stroke_surface_t is not None and stroke_surface_b is not None:
			# Log.print("has surface stroke")
			
			# RIGHT
			stroke_rect_r = stroke_surface_r.get_rect()
			stroke_rect_r.top = text_rect.top 
			stroke_rect_r.left = text_rect.left + stroke_width
			self.getCore().getRender().addSurfaceToRenderQueue(text + "_stroke_right", stroke_surface_r, stroke_rect_r)

			# LEFT
			stroke_rect_l = stroke_surface_l.get_rect()
			stroke_rect_l.top = text_rect.top 
			stroke_rect_l.left = text_rect.left - stroke_width
			self.getCore().getRender().addSurfaceToRenderQueue(text + "_stroke_left", stroke_surface_l, stroke_rect_l)

			# TOP
			stroke_rect_t = stroke_surface_t.get_rect()
			stroke_rect_t.top = text_rect.top - stroke_width
			stroke_rect_t.left = text_rect.left
			self.getCore().getRender().addSurfaceToRenderQueue(text + "_stroke_top", stroke_surface_t, stroke_rect_t)

			# BOTTOM
			stroke_rect_b = stroke_surface_t.get_rect()
			stroke_rect_b.top = text_rect.top + stroke_width
			stroke_rect_b.left = text_rect.left
			self.getCore().getRender().addSurfaceToRenderQueue(text + "_stroke_bottom", stroke_surface_b, stroke_rect_b)

			# TOP RIGHT
			stroke_rect_tr = stroke_surface_tr.get_rect()
			stroke_rect_tr.top = text_rect.top - stroke_width
			stroke_rect_tr.left = text_rect.left + stroke_width
			self.getCore().getRender().addSurfaceToRenderQueue(text + "_stroke_topright", stroke_surface_tr, stroke_rect_tr)

			# TOP LEFT
			stroke_rect_tl = stroke_surface_tl.get_rect()
			stroke_rect_tl.top = text_rect.top - stroke_width
			stroke_rect_tl.left = text_rect.left - stroke_width
			self.getCore().getRender().addSurfaceToRenderQueue(text + "_stroke_topleft", stroke_surface_tl, stroke_rect_tl)

			# BOTTOM RIGHT
			stroke_rect_br = stroke_surface_br.get_rect()
			stroke_rect_br.top = text_rect.top + stroke_width
			stroke_rect_br.left = text_rect.left + stroke_width
			self.getCore().getRender().addSurfaceToRenderQueue(text + "_stroke_bottomright", stroke_surface_br, stroke_rect_br)

			# BOTTOM LEFT
			stroke_rect_bl = stroke_surface_bl.get_rect()
			stroke_rect_bl.top = text_rect.top + stroke_width
			stroke_rect_bl.left = text_rect.left - stroke_width
			self.getCore().getRender().addSurfaceToRenderQueue(text + "_stroke_bottomleft", stroke_surface_bl, stroke_rect_bl)

		self.getCore().getRender().addSurfaceToRenderQueue(text, text_surface, text_rect)
		return text_rect
