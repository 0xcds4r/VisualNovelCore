SceneUtils = {}

function SceneUtils:new(o)
	Log.print("Initializing SceneUtils..", "SceneUtils")
	o = o or {}
	setmetatable(o, self)
	self.__index = self
	self.arial_font = 0
	self.sceneCounter = 0
	self.dialogCounter = 0
	self.textSurface = 0
	self.sceneNames = {}
	self.dataPaths = {
	  [0] = "data/script.json",
	  [1] = "data/main_menu.json",
	  [2] = "data/pause_menu.json",
	}

	-- Be sure to initialize the render
	RenderUtils.initialize()
	
	return o
end

function SceneUtils:loadScripts()
	Log.print(self.dataPaths[0], "loadScripts")
	local scriptData = scriptLoader.loadScript("scenes", self.dataPaths[0])
	scenes.addSceneFromScriptData(scriptData)

	local mmData = scriptLoader.loadScript("main_menu", self.dataPaths[1])
	local pmData = scriptLoader.loadScript("pause_menu", self.dataPaths[2])

	self.sceneCounter = 0
	self.dialogCounter = 0

	self.scenes_data = scenes.getScenes()
	self.scenes_count = scenes.getScenesCount()

	for i = 0, self.scenes_count-1 do
	  self.sceneNames[i] = self.scenes_data[i].getName()
	end

	self:resetScene()
	self:updateScene()
end

function SceneUtils:setCurrentScene(sceneIndex)
	scenes.getSceneView().setCurrentScene(scenes.getScene(self.sceneNames[sceneIndex]))
end

function SceneUtils:resetScene()
	self.sceneCounter = 0
	self.dialogCounter = 0
	self:setCurrentScene(self.sceneCounter)
end

function SceneUtils:updateScene()
	scenes.getSceneView().showScene(false)
	self.dialogCounter = 0
	self:setCurrentScene(self.sceneCounter)
	scenes.getSceneView().showScene(true)
end

function SceneUtils:drawScene()
	local sceneView = scenes.getSceneView()
	if not sceneView.isSceneShowing() then return end

	local current_scene = sceneView.getCurrentScene() 

	local background = current_scene.getDataValue('background')

	local characters = current_scene.getDataValue('characters')
	local charsKeys = VN.getDataKeys(characters)
	local charLen = VN.getDataLength(characters)

	local dialogue = current_scene.getDataValue('dialogue')
	local dialogueLen = VN.getDataLength(dialogue)

	-- render background
	local background_img = render.getImageManager().load_image(background)
	background_img = render.getImageManager().setImageSize(background_img, 1920, 1080)
	render.addSurfaceToRenderQueue('bg', background_img) 

	-- render characters
	for i = 0, charLen-1 do
		local name = charsKeys[i]
		-- Log.print("name char:" ..name)
		local character = characters[name]
		local image = character['image']
		local position = character['position']
		local img = render.getImageManager().load_image(image)

		if name == "judge" then
			img = render.getImageManager().setImageSize(img, 370, 800)
		else
			img = render.getImageManager().setImageSize(img, 600, 800)
		end
		
		render.addSurfaceToRenderQueuePos(name, img, position[0], position[1]) 
	end

	-- render dialogues
	local speaker = dialogue[self.dialogCounter]['speaker']
	local text = dialogue[self.dialogCounter]['text']

	RenderUtils.renderSubtitle(speaker, text)
end

function SceneUtils:nextDialogue()
	local res = self.dialogCounter
	self.dialogCounter = res + 1
end 

function SceneUtils:nextScene()
    self.sceneCounter = self.sceneCounter + 1
    core.getAudioManager().play_sfx("sweep")
    if self.sceneCounter > #self.sceneNames then
        self:resetScene()
    else
        self:updateScene()
    end
end

function SceneUtils:nextClickEvent()
	local sceneView = scenes.getSceneView()
	local current_scene = sceneView.getCurrentScene() 

	local dialogue = current_scene.getDataValue('dialogue')
    local dialogueLen = VN.getDataLength(dialogue)

    if self.dialogCounter < dialogueLen-1 then
        self:nextDialogue()
    else
        self:nextScene()
    end
end