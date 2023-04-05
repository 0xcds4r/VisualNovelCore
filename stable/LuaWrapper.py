import lupa
from lupa import LuaRuntime
from datetime import datetime, date
import pygame.locals

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
            # print(self.final)
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
	def getCore():
		return core
		