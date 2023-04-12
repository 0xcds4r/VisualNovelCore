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
    
    def registerKeyDownEvent(self, key, code):
        handler = lambda: self.core.callLuaEventInAll(code)
        if handler:
            self.key_down_handlers[key] = handler

    def registerKeyUpEvent(self, key, code):
        handler = lambda: self.core.callLuaEventInAll(code)
        if handler:
            self.key_up_handlers[key] = handler

    def registerLongKeyDownEvent(self, key, code, delay=0.5, interval=1):
        handler = lambda: self.core.callLuaEventInAll(code)
        if handler:
            self.long_key_down_handlers[key] = handler
            self.key_down_times[key] = 0
            self.long_key_down_delay = delay
            self.long_key_down_interval = interval

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

    def handle(self, event):
        keyDownActive = None
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_down_handlers:
                self.key_down_handlers[event.key]()
                keyDownActive = event.key
            if event.key in self.long_key_down_handlers:
                self.long_key_down_handlers[event.key]()
                self.key_down_times[event.key] = 0
            return True
        if event.type == pygame.KEYUP:
            if event.key in self.key_up_handlers:
                self.key_up_handlers[event.key]()
                keyDownActive = None
            if event.key in self.long_key_down_handlers:
                self.key_down_times[event.key] = 0
            return True
        return True