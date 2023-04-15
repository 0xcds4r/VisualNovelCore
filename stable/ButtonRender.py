import pygame
from Log import Log

class Button:
    def __init__(self, core):
        self.core = core
        self.text = None
        self.font = None
        self.font_color = None
        self.rect = None
        self.bg_color = None
        self.bg_image = None
        self.hovered = False
        self.tag = ""
        self.hover_color = None
        self.size = (0, 0)
        self.pos = (0, 0)
        self.disabled = False

    def reset(self):
        self.text = None
        self.font = None
        self.font_color = None
        self.rect = None
        self.bg_color = None
        self.bg_image = None
        self.hovered = False
        self.tag = ""
        self.hover_color = None
        self.size = (0, 0)
        self.pos = (0, 0)
        self.disabled = False

    def getCore(self):
        return self.core

    def setText(self, text):
        self.text = text

    def setDisabled(self, value):
        self.disabled = value

    def isDisabled(self):
        return self.disabled

    def createButton(self, tag):
        self.tag = tag

    def getId(self):
        return self.tag

    def setFont(self, font_file, font_size):
        self.font = pygame.font.Font(font_file, font_size) if font_file is not None else pygame.font.Font(None, font_size)

    def setColor(self, color):
        self.font_color = color

    def setColorRGBA(self, r,g,b,a):
        self.font_color = (r,g,b,a)

    def setRect(self, rect):
        self.rect = pygame.Rect(rect) if rect is not None else None

    def setPosition(self, x, y):
        self.pos = (x, y)
        self.setRect([self.pos[0],self.pos[1],self.size[0],self.size[1]])

    def setSize(self, w, h):
        self.size = (w, h)
        self.setRect([self.pos[0],self.pos[1],self.size[0],self.size[1]])

    def set_hover_color(self, color):
        self.hover_color = color

    def set_hover_color_rgba(self, r, g, b, a):
        self.hover_color = (r,g,b,a)

    def get_hover_color(self):
        return self.hover_color

    def set_bg_color(self, color):
        self.bg_color = color

    def set_bg_color_rgba(self, r, g, b, a):
        self.bg_color = (r,g,b,a)

    def get_bg_color(self):
        return self.bg_color

    def set_hovered(self, val):
        self.hovered = val

    def setBgImage(self, image):
        self.bg_image = image

    def isButtonPressed(self, tag_id=None):
        if self.rect == None:
            return False

        if self.tag == None:
            return False

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if tag_id == self.tag:
                if not self.isDisabled():
                    return pygame.mouse.get_pressed()[0]

        return False

    def draw(self):
        if self.tag == None:
            return

        if self.bg_color is not None:
            # if self.isButtonPressed(self.tag):
                # self.set_hovered(True)
            # else:
                # self.set_hovered(False)

            button_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            
            if self.hovered == True:
                button_surface.set_alpha(self.hover_color[3])
                button_surface.fill(self.hover_color)
            else:
                button_surface.set_alpha(self.bg_color[3])
                button_surface.fill(self.bg_color)

            self.getCore().getRender().getDisplay().blit(button_surface, self.rect.topleft)

            text_surface = self.font.render(self.text, True, self.font_color)
            text_rect = text_surface.get_rect(center=self.rect.center) if self.rect is not None else text_surface.get_rect()
            self.getCore().getRender().getDisplay().blit(text_surface, text_rect)
        elif self.bg_image is not None:
            button_image = self.bg_image.copy()
            button_image.set_alpha(self.bg_image.get_at((0, 0))[3])
            self.getCore().getRender().getDisplay().blit(button_image, self.rect.topleft)
            text_surface = self.font.render(self.text, True, self.font_color)
            text_rect = text_surface.get_rect(center=self.rect.center) if self.rect is not None else text_surface.get_rect()
            self.getCore().getRender().getDisplay().blit(text_surface, text_rect)

        self.reset()

class ButtonRender(Button):
    def __init__(self, core):
        Log.print("Initializing ButtonRender..")
        super().__init__(core)

    def draw(self):
        super().draw()