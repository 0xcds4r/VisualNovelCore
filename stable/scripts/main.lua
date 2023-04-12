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

-- Initialize render
render.getRenderFlags().set_flags(FLAG_USE_DEFAULT_DISPLAY_FLAGS | FLAG_USE_DEFAULT_SURFACE_FLAGS | FLAG_DONT_AUTO_RENDER_IMAGES | FLAG_DONT_LOAD_DEFAULT_FONT)
render.setScreenSize(1920, 1080)
render.Initialize()

local function renderSubtitle(speaker, text)
    local screen_width = render.getScreenWidth()
    local screen_height = render.getScreenHeight()
    local font_size = 30
    local font_size_t = 40

    local r = 0
    local g = 0
    local b = 0
    local a = 150
    local name = "box"
    local x = screen_width * 0
    local y = screen_height * 0.85
    local width = screen_width
    local height = screen_height
    render.addRect(name, r, g, b, a, x, y, width, height)

    -- old method
    -- render.getTextManager().addText(speaker, screen_width * 0.05, y + (height * 0.02), "assets/arial.ttf", font_size, "left", false, false, 0, 0, 0, 255, 0,0,0,0, 255,0,0,255, 0.95)
    
    -- new method
    render.getTextManager().getTextElement().setText(speaker)
    render.getTextManager().getTextElement().setPosition(screen_width * 0.05, y + (height * 0.02))
    render.getTextManager().getTextElement().setFont("assets/arial.ttf")
    render.getTextManager().getTextElement().setFontSize(font_size)
    render.getTextManager().getTextElement().setAlign("left")
    render.getTextManager().getTextElement().setBold(false)
    render.getTextManager().getTextElement().setItalic(true)
    render.getTextManager().getTextElement().setTextColor(0, 0, 0, 255)
    render.getTextManager().getTextElement().setBgColor(0, 0, 0, 10)
    render.getTextManager().getTextElement().setStrokeColor(255, 0, 0, 255)
    render.getTextManager().getTextElement().setStrokeWidth(0.95)
    render.getTextManager().getTextElement().draw()

    local words = {}
    for word in text:gmatch("%S+") do
        table.insert(words, word)
    end
    local lines = {}
    local line = ""
    for i, word in ipairs(words) do
        if render.getTextManager().getTextWidth(line .. " " .. word, "assets/arial.ttf", font_size) > 0.9 * screen_width then
            table.insert(lines, line)
            line = word
        else
            line = line .. " " .. word
        end
    end
    table.insert(lines, line)
    for i, line in ipairs(lines) do
        -- old method
        -- render.getTextManager().addText(line, screen_width * 0.055, y + (height * 0.05) + (i-1)*0.04*screen_height, "assets/arial.ttf", font_size_t, "left", false, false, 255, 255, 255, 255, 0,0,0,0, 0,0,0,255, 0.95)

        -- new method
        render.getTextManager().getTextElement().setText(line)
        render.getTextManager().getTextElement().setPosition(screen_width * 0.055, y + (height * 0.05) + (i-1)*0.04*screen_height)
        render.getTextManager().getTextElement().setFont("assets/arial.ttf")
        render.getTextManager().getTextElement().setFontSize(font_size)
        render.getTextManager().getTextElement().setAlign("left")
        render.getTextManager().getTextElement().setBold(false)
        render.getTextManager().getTextElement().setItalic(false)
        render.getTextManager().getTextElement().setTextColor(255, 255, 255, 255)
        render.getTextManager().getTextElement().setBgColor(0, 0, 0, 0)
        render.getTextManager().getTextElement().setStrokeColor(0, 0, 0, 255)
        render.getTextManager().getTextElement().setStrokeWidth(0.95)
        render.getTextManager().getTextElement().draw()
    end
end

-- SCENE HELPER
local arial_font = 0
local sceneCounter = 0
local dialogCounter = 0
local textSurface = 0

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
    dialogCounter = 0
    setCurrentScene(sceneCounter)
end

function updateScene()
    scenes.getSceneView().showScene(false)
    setCurrentScene(sceneCounter)
    dialogCounter = 0
    scenes.getSceneView().showScene(true)
end

function drawScene()
    if scenes.getSceneView().isSceneShowing() then
        local background = scenes.getSceneView().getCurrentScene().getDataValue('background')
        local characters = scenes.getSceneView().getCurrentScene().getDataValue('characters')

        local choro = characters['choro']
        local choroImage = choro['image']
        local choroPos = choro['position']

        dialogue = scenes.getSceneView().getCurrentScene().getDataValue('dialogue')
        dialogueLen = scenes.getSceneView().getCurrentScene().getDataLength(dialogue)

        -- render background
        local img = render.getImageManager().load_image(background)
        img = render.getImageManager().setImageSize(img, 1920, 1080)
        render.addSurfaceToRenderQueue('bg', img) 

        -- render characters
        local choroImg = render.getImageManager().load_image(choroImage)
        choroImg = render.getImageManager().setImageSize(choroImg, 600, 800)
        render.addSurfaceToRenderQueuePos('choro', choroImg, choroPos[0], choroPos[1]) 

        -- render dialogue
        local speaker = dialogue[dialogCounter]['speaker']
        local text = dialogue[dialogCounter]['text']
        renderSubtitle(speaker, text)

        -- render.addCircle("tcirc", 500, 500, VN.randomizeBetween(0, 255), VN.randomizeBetween(0, 255), VN.randomizeBetween(0, 255), VN.randomizeBetween(150, 255), VN.randomizeBetween(60, 90), VN.randomizeBetween(5, 10), VN.randomizeBetween(5, 10), 15, 15, 30.0, VN.randomizeBetween(66, 255), VN.randomizeBetween(66, 255), VN.randomizeBetween(66, 255), VN.randomizeBetween(150, 255))
    end
end

function nextDialogue()
    dialogCounter = dialogCounter + 1
end 

function nextScene()
    nextSceneCounter = sceneCounter + 1
    core.callLuaEvent(EVENT_SCRIPT, "onNextSceneEvent", sceneCounter, nextSceneCounter)
    sceneCounter = nextSceneCounter
    core.getAudioManager().play_sfx("sweep")
    if sceneCounter > #sceneNames then
        resetScene()
    else
        updateScene()
        -- core.getAudioManager().stop_music(2000)
    end
end

function onUpdateDialogueScene()
    dialogue = scenes.getSceneView().getCurrentScene().getDataValue('dialogue')
    dialogueLen = scenes.getSceneView().getCurrentScene().getDataLength(dialogue)

    if dialogCounter < dialogueLen-1 then
        nextDialogue()
    else
	    nextScene()
    end
end

function registerKeyStuff()
	events.registerLongKeyDownEvent(K_SPACE, "onSpaceClickEvent") -- if space clicked then call onSpaceClickEvent in events.lua
	-- Made for convenience, so as not to do everything in one script
end

-- GLOBAL EVENTS --

-- Calling when game starting
function onGameStart()
    printLog("onGameStart")

    core.getAudioManager().load_music("assets/sound/hidamari.mp3")
    core.getAudioManager().play_music(-1, 2000)
    core.getAudioManager().set_music_volume(0.3)

    core.getAudioManager().load_sfx("sweep", "assets/sound/sweep.wav")


    core.setTitle("Random game title here")
    core.setIcon(render.getImageManager().load_image("assets/icon256.png"))

    loadScripts() -- Loading json data
    registerKeyStuff() -- loading key binds
end

-- Calling when mouse click
function onTouchEvent(button, x, y)
    printLog("onTouchEvent -> button ("..button..") clicked at ("..x..", "..y..")")
end

-- Calling when mouse move
function onTouchMoveEvent(x, y)
    -- printLog("onTouchMoveEvent -> ("..x..", "..y..")")
    if VN.overlapsZone(x, y, 111, 111, 0, 0, 555, 555) then
        printLog("zone: yes")
    end
end

-- Render (Calling every frame)
function onGameRender()
    drawScene()
end
