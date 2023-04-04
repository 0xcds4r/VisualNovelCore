
from Log import Log
import pygame
import time

class Events:
    def __init__(self, core):
        self.key_down_handlers = {}
        self.key_up_handlers = {}
        self.long_key_down_handlers = {}
        self.key_down_times = {}
        self.core = core
    
    def register_key_down_handler(self, key, handler):
        self.key_down_handlers[key] = handler
    
    def register_key_up_handler(self, key, handler):
        self.key_up_handlers[key] = handler
    
    def register_long_key_down_handler(self, key, handler, delay=0.5, interval=0.5):
        self.long_key_down_handlers[key] = handler
        self.key_down_times[key] = 0
        self.long_key_down_delay = delay
        self.long_key_down_interval = interval
    
    def test(self):
    	print("test work events")

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_down_handlers:
                    self.key_down_handlers[event.key]()
                if event.key in self.long_key_down_handlers:
                    self.key_down_times[event.key] = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP:
                if event.key in self.key_up_handlers:
                    self.key_up_handlers[event.key]()
                if event.key in self.long_key_down_handlers:
                    self.key_down_times[event.key] = 0

        for key, time in self.key_down_times.items():
            if time != 0 and pygame.time.get_ticks() - time > self.long_key_down_delay:
                if key in self.long_key_down_handlers:
                    if (pygame.time.get_ticks() - time - self.long_key_down_delay) % self.long_key_down_interval == 0:
                        self.long_key_down_handlers[key]()

        return True