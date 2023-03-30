import pygame

class RectWrapper:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def get(self):
        return self.rect

    def __getattr__(self, attr):
        return getattr(self.rect, attr)
    
    def __setattr__(self, attr, value):
        if attr == 'rect':
            super().__setattr__(attr, value)
        else:
            setattr(self.rect, attr, value)
    
    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
    
    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
    def resize(self, width, height):
        self.rect.width = width
        self.rect.height = height
        
    def set_pos(self, x, y):
        self.rect.topleft = (x, y)
    
    def set_center(self, x, y):
        self.rect.center = (x, y)
    
    def set_bottomleft(self, x, y):
        self.rect.bottomleft = (x, y)
    
    def set_bottomright(self, x, y):
        self.rect.bottomright = (x, y)
    
    def set_topleft(self, x, y):
        self.rect.topleft = (x, y)
    
    def set_topright(self, x, y):
        self.rect.topright = (x, y)
        
    def set_centerx(self, x):
        self.rect.centerx = x
        
    def set_centery(self, y):
        self.rect.centery = y
    
    def contains(self, other_rect):
        return self.rect.contains(other_rect)
    
    def overlaps(self, other_rect):
        return self.rect.colliderect(other_rect)