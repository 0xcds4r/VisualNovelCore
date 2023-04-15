import lupa
from lupa import LuaRuntime
from datetime import datetime, date
import pygame.locals
from RenderData import *
from RectWrapper import RectWrapper
import random
import re
import importlib
import inspect
import os

class LuaWrapper:
	def __init__(self, core, script_name, script_path):
		# from Log import Log
		# Log.print("Initializing LuaWrapper..")
		self.lua = LuaRuntime(unpack_returned_tuples=True)
		self.script_path = script_path
		self.core = core
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
		file_content = self.open_script(script_path)
		file_content = file_content.replace("@method", "--")
		file_content = file_content.replace("@include", "--")
		file_content = file_content.replace("@pyimport", "--")

		self.final = self.begin + file_content + '\nend\n'

		self.checkAPI(self.final)
		self.interface = self.lua.eval(self.final)
		self.interface(SDKLua)

	def existsInCode(self, tag, str_code):
		code_lines = str_code.split('\n')
		for code_line in code_lines:
			if tag in code_line:
				if not code_line.strip().startswith("--"):
					return True
		return False

	def checkAPI(self, str_code):
		from Log import Log
		if not self.existsInCode("API_VERSION", str_code):
			Log.print(f"API_VERSION not found! (add in script: API_VERSION = {str(core.getVersionCode())})")
			self.core.quitGame()
			return

		code_lines = str_code.split('\n')
		for code_line in code_lines:
			if "API_VERSION" in code_line:
				api_version_line = code_line.replace(" ", "").split('=')
				number = ''
				for char in api_version_line[1]:
					if char.isdigit():
						number += char
					else:
						break
				api_version = int(number)
				if core.checkVersionCode(api_version) == 1:
					# Log.print(f"API_VERSION is {str(api_version)}")
					pass
				else:
					if core.checkVersionCode(api_version) < 0:
						Log.print(f"Invalid API_VERSION: {str(api_version)} (API version of the core now is -> {str(core.getVersionCode())})")
					elif core.checkVersionCode(api_version) == 0:
						Log.print(f"Deprecated API_VERSION {str(api_version)} (API version of the core now is -> {str(core.getVersionCode())})")
					self.core.quitGame()


	def open_script(self, script_path):
		with open(script_path, 'r') as f:
			file_content = f.read()
			lines = file_content.splitlines()
			included_content = ""
			for line in lines:
				if '@include' in line:
					if line.strip().startswith("--"):
						# print(f"commented include: {line}")
						continue
					match = re.search(r"'(.+?)'", line)
					if match:
						# Extract the text inside single quotes
						text = match.group(1)
						included_path = "./scripts/" + text + ".lua"
						included_content += self.open_script(included_path) + "\n"
				elif '@method' in line:
					if line.strip().startswith("--"):
						# print(f"commented method: {line}")
						continue

					match = re.search(r"'(.+?)'", line)
					if match:
						text = match.group(1)
						res = text.replace(' ', '').split(',')
						included_path = "./scripts/" + res[0] + ".lua"
						if len(res) == 2:
							method_code = self.get_lua_function_code(included_content, self.open_script(included_path), res[1])
							included_content += method_code + "\n"
							# print(method_code)
						elif len(res) > 2:
							for i in range(1, len(res)):
								method_code = self.get_lua_function_code(included_content, self.open_script(included_path), res[i])
								included_content += method_code + "\n"
								# print(method_code)
						else:
							pass
				elif '@pyimport' in line:
					if line.strip().startswith("--"):
						# print(f"commented pyimport: {line}")
						continue

					match = re.search(r"'(.+?)'", line)
					if match:
						text = match.group(1)
						res = text.replace(' ', '').split(':')
						# print(res)
						if len(res) == 1:
							# module = importlib.import_module(text)
							included_content += res[0] + " = " + "VN.__pyimport__('"+res[0]+"')" + "\n"
						elif len(res) == 2:
							# module = importlib.import_module(res[1])
							included_content += res[1] + " = " + "VN.__pyimport__('"+res[0]+"')" + "\n"
						else:
							pass
				else:
					included_content += line + "\n"

		return included_content

	def get_lua_function_code(self, included_content, lua_script_code, function_name):
		result = ""
		pattern = rf"function\s+({function_name})\s*([^\)]*)\)\s*(.*?\n)\s*end"
		match = re.search(pattern, lua_script_code, re.DOTALL)
		if match:
			name = match.group(1)
			if '.' in name:
				full_name = name.replace(' ', '').split('.')
				className = full_name[0]
				add_class = f"{className} = {{}}\n"
				if not add_class in included_content:
					result += add_class

			args = match.group(2).replace(' ', '').split(',')
			code_str = match.group(3)
			result += "function" + " " + name + "" + ", ".join(args) + ")" + "\n" + "\t" + code_str.strip() + "\nend"
			# return {'name': name, 'args': args, 'code': code_str.strip()}
			return result
		return ""

	def register_event(self, event_name, callback):
		self.lua.globals()[event_name] = callback

	def unregister_event(self, event_name):
		self.lua.globals()[event_name] = None

	def hasLuaEvent(self, event):
		with open(self.script_path, 'r') as f:
			return any(event in line for line in f.readlines())

lua_vars = {}
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
	def RWRect(x, y, w, h):
		return RectWrapper(x, y, w, h)

	@staticmethod
	def safe_delete(data):
		if data:
			del data

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
	def getDataValue(data, key):
		return data[key]

	@staticmethod
	def getDataKeys(data):
		keys = {}
		for i, key in enumerate(data.keys()):
			keys[i] = key
		return keys

	@staticmethod
	def getDataItems(data):
		items = {}
		for i, item in enumerate(data.items()):
			items[i] = item
		return items

	@staticmethod
	def getDataValues(data):
		values = {}
		for i, value in enumerate(data.values()):
			values[i] = value
		return values

	@staticmethod
	def getDataLength(data):
		return len(data)

	@staticmethod
	def __load__(namespace, name):
		if name.endswith('.luac'):
			core.loadLuaScript("utils", name)
		elif name.endswith('.lua'):
			core.loadLuaScript("utils", name)
		else:
			core.loadLuaScript("utils", name + ".lua")
			return name + ".lua"

		return name

	@staticmethod
	def __call__(script, event, *args):
		core.callLuaEvent(script, event, *args)

	@staticmethod
	def putVar(varName, varValue):
		# print("Creating var: " + varName)
		lua_vars[varName] = varValue
	   
	@staticmethod
	def getVar(varName):
		return lua_vars.get(varName)

	@staticmethod
	def delVar(varName):
		if varName in lua_vars:
			# print("Deleting var: " + varName)
			del lua_vars[varName]
			lua_vars[varName] = None

	@staticmethod
	def getMousePos():
		return pygame.mouse.get_pos()

	@staticmethod
	def getCore():
		return core
		
	@staticmethod
	def __pyimport__(module):
		module_obj = importlib.import_module(module)
		return module_obj