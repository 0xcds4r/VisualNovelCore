-- SCRIPT INFO
SCRIPT_NAME = "SceneHelper"
SCRIPT_AUTHOR = "0xcds4r"
SCRIPT_VERSION = "v0.1"

-- Imports?
EVENT_SCRIPT = "events.lua"

-- Log SCRIPT_NAME and SCRIPT_PATH
-- default SCRIPT_NAME is your lua script file name
VN.log("Loaded new script: " .. SCRIPT_NAME .. " from: " .. SCRIPT_PATH)

-- UTILS
local core = VN.getCore()
local scenes = core.getScenes()
local render = core.getRender()
local events = core.getEvents()
local scriptLoader = core.getScriptLoader()

local function printLog(log)
    VN.log("["..SCRIPT_NAME.."] "..log)
end

-- SCENE HELPER
local sceneCounter = 0

local sceneNames = {
    [0] = "intro",
    [1] = "goal",
}

local dataPaths = {
	[0] = "data/script.json",
	[1] = "data/main_menu.json",
	[2] = "data/pause_menu.json",
}

function loadScripts()
    local scriptData = scriptLoader.loadScript("scenes", dataPaths[0])
    scenes.addSceneFromScriptData(scriptData)

    local mmData = scriptLoader.loadScript("main_menu", dataPaths[1])
    local pmData = scriptLoader.loadScript("pause_menu", dataPaths[2])

    core.callLuaEvent(EVENT_SCRIPT, "onScriptsLoadedEvent")
end

function setCurrentScene(sceneIndex)
    scenes.getSceneView().setCurrentScene(scenes.getScene(sceneNames[sceneIndex]))
end

function resetScene()
    sceneCounter = 0
    setCurrentScene(sceneCounter)
end

function updateScene()
    scenes.getSceneView().showScene(false)
    setCurrentScene(sceneCounter)
    scenes.getSceneView().showScene(true)
end

function drawScene()
    if scenes.getSceneView().isSceneShowing() then
        local background = scenes.getSceneView().getCurrentScene().getDataValue('background')
        local img = render.load_image(background)
        img = render.setSizeImage(img, 1920, 1080)
        render.addSurfaceToRenderQueue('bg', img) 
    end
end

function nextScene()
	nextSceneCounter = sceneCounter + 1
	core.callLuaEvent(EVENT_SCRIPT, "onNextSceneEvent", sceneCounter, nextSceneCounter)
    sceneCounter = nextSceneCounter

    if sceneCounter > #sceneNames then
        resetScene()
    else
        updateScene()
    end
end

function registerKeyStuff()
	events.registerKeyDownEvent(K_SPACE, "onSpaceClickEvent") -- if space clicked then call onSpaceClickEvent in events.lua
	-- Made for convenience, so as not to do everything in one script
end

-- GLOBAL EVENTS --

-- Calling when game starting
function onGameStart()
    printLog("onGameStart")
    loadScripts() -- Loading json data
    registerKeyStuff() -- loading key binds
end

-- Render (Calling every frame)
function onGameRender()
    drawScene()
end
