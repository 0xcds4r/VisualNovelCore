-- SCRIPT INFO
-- SCRIPT INFO
SCRIPT_NAME = "SceneEvents"
SCRIPT_AUTHOR = "0xcds4r"
SCRIPT_VERSION = "v0.1"

-- Imports?
MAIN_SCRIPT = "main.lua"

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

-- EVENTS
function onNextSceneEvent(oldSceneId, newSceneId)
	printLog("onNextSceneEvent called with args -> oldSceneId: "..oldSceneId..", newSceneId: "..newSceneId)
end

function onSpaceClickEvent()
    printLog("onSpaceClickEvent called without args")
    core.callLuaEvent(MAIN_SCRIPT, "nextScene") -- call nextScene in main.lua
    -- Made for convenience, so as not to do everything in one script
end

function onScriptsLoadedEvent()
	printLog("onScriptsLoadedEvent called without args")
	core.callLuaEvent(MAIN_SCRIPT, "resetScene")
	core.callLuaEvent(MAIN_SCRIPT, "updateScene")
end