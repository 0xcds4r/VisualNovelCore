import lupa
from lupa import LuaRuntime
from datetime import datetime, date
import pygame.locals
from RenderData import *
from RectWrapper import RectWrapper
import random

class LuaWrapper:
    def __init__(self, core, script_name, script_path):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.script_path = script_path
        SDKLua.setCore(core)

        key_constants = {}
        for name in dir(pygame.locals):
            if name.startswith('K_'):
                value = getattr(pygame.locals, name)
                key_constants[name] = value

        key_code = ''
        for name, value in key_constants.items():
            key_code += f'\t\t{name} = {value}\n'

        # Render flags
        key_code += f'\t\tFLAG_USE_VSYNC = {FLAG_USE_VSYNC}\n'
        key_code += f'\t\tFLAG_DONT_LOAD_DEFAULT_FONT = {FLAG_DONT_LOAD_DEFAULT_FONT}\n'
        key_code += f'\t\tFLAG_USE_DEFAULT_DISPLAY_FLAGS = {FLAG_USE_DEFAULT_DISPLAY_FLAGS}\n'
        key_code += f'\t\tFLAG_USE_DEFAULT_SURFACE_FLAGS = {FLAG_USE_DEFAULT_SURFACE_FLAGS}\n'
        key_code += f'\t\tFLAG_DONT_AUTO_RENDER_IMAGES = {FLAG_DONT_AUTO_RENDER_IMAGES}\n'

        scr_name = script_name.replace(".lua", "")
        scr_path = script_path.replace(script_name, "")
        self.begin = f'''
            function(obj)
                if obj.__name__ == 'SDKLua' then
                    rawset(_G, 'SDKLua', obj)
                end
                VN = _G['SDKLua']
                if not VN then
                    return
                end
                local SCRIPT_NAME = '{scr_name}'
                local SCRIPT_PATH = '{scr_path}'
                {key_code}
        '''
        with open(script_path, 'r') as f:
            self.final = self.begin + f.read() + '\nend\n'
            self.interface = self.lua.eval(self.final)
        self.interface(SDKLua)

    def register_event(self, event_name, callback):
        self.lua.globals()[event_name] = callback

    def unregister_event(self, event_name):
        self.lua.globals()[event_name] = None

    def hasLuaEvent(self, event):
        with open(self.script_path, 'r') as f:
            return any(event in line for line in f.readlines())

class SDKLua:
	core = None

	@staticmethod
	def setCore(_core):
		global core
		core = _core

	@staticmethod
	def log(message):
		now = datetime.now()
		current_time = str(now.strftime("%H:%M:%S"))
		today = str(date.today())
		msg = f"[{current_time}] {message}"
		print(msg)

	@staticmethod
	def containsZone(tx, ty, tw, th, x, y, w, h):
		trw = RectWrapper(tx, ty, tw, th)
		rw = RectWrapper(x, y, w, h)
		state = rw.contains(trw)
		del trw
		del rw
		return state

	@staticmethod
	def randomizeBetween(begin_value, end_value, chance = 0):
		if chance <= 0:
			return random.uniform(begin_value, end_value)

		if random.random() < chance:
			return random.uniform(begin_value, end_value)
		else:
			return begin_value

	@staticmethod
	def overlapsZone(tx, ty, tw, th, x, y, w, h):
		trw = RectWrapper(tx, ty, tw, th)
		rw = RectWrapper(x, y, w, h)
		state = rw.overlaps(trw)
		del trw
		del rw
		return state

	@staticmethod
	def getCore():
		return core
		