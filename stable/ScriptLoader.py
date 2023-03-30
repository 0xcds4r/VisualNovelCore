from Log import Log
import json
import os

class ScriptLoader():
	def __init__(self, core):
		Log.print("Initializing ScriptLoader..")
		self.core = core
		self.scripts = []

	def getCore(self):
		return self.core

	def getScripts(self):
		return self.scripts

	def getScriptData(self, tag):
		if len(tag) <= 0:
			Log.print("Script tag is empty")
			return None

		for script_tag, script_data in self.getScripts():
			if script_tag == tag:
				return script_data

		return None

	def getScriptTagByData(self, data):
		for script_tag, script_data in self.getScripts():
			if script_data == data:
				return script_tag

	def loadScript(self, script_tag, file_path):
		if len(script_tag) <= 0:
			Log.print("Script tag is empty")
			return None

		if self.getScriptData(script_tag) is not None:
			return self.getScriptData(script_tag)

		if not os.path.exists(file_path):
			Log.print("Error while loading script: {script_tag} (path: {file_path}): file not found!")

		scriptData = None
		with open(file_path, 'r') as f:
			scriptData = json.load(f)

		if scriptData is not None:
			Log.print(f"New script loaded: {script_tag} (path: {file_path})")
			self.scripts.append((script_tag, scriptData))
			return scriptData

		Log.print("Error while loading script: {script_tag} (path: {file_path}): no script data!")
		return None
		