from Log import Log

class Scene():
	def __init__(self, name, data):
		Log.print(f"Loading scene: {name}..")
		self.name = name
		self.data = data

	def destroy(self):
		self.name = None
		self.data = None

	def getData(self):
		return self.data

	def getName(self):
		return self.name
		
class SceneView():
	def __init__(self):
		Log.print("Initializing SceneView..")
		self.currentScene = None
		self.show_scene = False

	def showScene(self, state = True):
		self.show_scene = state

	def isSceneShowing(self):
		return self.show_scene == True

	def getCurrentScene(self):
		return self.currentScene

	def setCurrentScene(self, scene):
		self.currentScene = scene

class Scenes():
	def __init__(self, core):
		Log.print("Initializing Scenes..")
		self.core = core
		self.sceneView = SceneView()
		self.scenes = []
		
	def getSceneView(self):
		return self.sceneView

	def getCore(self):
		return self.core

	def getScenes(self):
		return self.scenes

	def getScene(self, name):
		for scene in self.getScenes():
			if scene.getName() == name:
				return scene
		return None

	def getSceneByData(self, data):
		for scene in self.getScenes():
			if scene.getData() == data:
				return scene
		return None

	def isSceneExists(self, name):
		for scene in self.getScenes():
			if scene.getName() == name:
				return True
		return False

	def addSceneFromScriptData(self, data):
		for scene_name, scene_data in data['scenes'].items():
			self.createScene(scene_name, scene_data)

	def createScene(self, name, data, rewrite=False, existsAlert=False, existsRewriteAlert=False):
		if self.isSceneExists(name) and rewrite == True:
			if existsRewriteAlert == True:
				Log.print(f"Scene with name: {name} already exists, rewriting..")
			self.destroyScene(name)
		elif self.isSceneExists(name) and rewrite == False:
			if existsAlert == True:
				Log.print(f"Scene with name: {name} already exists!")
			return False

		self.scenes.append(Scene(name, data))
		Log.print(f"Scene with name: {name} successfully loaded!")
		return True

	def destroyScene(self, name):
		if not self.isSceneExists(name):
			Log.print(f"Scene with name: {name} not exists")
			return False

		for scene in self.getScenes():
			if scene.getName() == name:
				scene.destroy()
				self.scenes.remove(scene)
				return True
		return False
