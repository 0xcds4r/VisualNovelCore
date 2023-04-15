-------------------------------------- SCRIPT INFO --------------------------------------
-- SCRIPT_NAME = "VisualNovelDemo"
SCRIPT_AUTHOR = "0xcds4r"
SCRIPT_VERSION = "v0.3"
GAME_TITLE = "VNC DEMO"
GAME_ICON = "assets/icon256.png"

-------------------------------------- INCLUDES --------------------------------------

-- include project utils
@include 'utils/Utils'
@include 'utils/LogUtils'
@include 'utils/RenderUtils'
@include 'utils/SceneUtils'
@include 'utils/ButtonUtils'
@include 'utils/FileUtils'
@include 'utils/SaveUtils'

-- import python modules
@pyimport 'random:rnd'
@pyimport 'datetime'

-- import methods from test.lua
@method 'utils/test, ClassTest.func_class_test, ClassTest.func_test'

-------------------------------------- UTILS --------------------------------------
local fm = FileManager.new()
local pSceneUtils = SceneUtils:new()
local pFirstButton = Button:new()
local pSecondButton = Button:new()

-------------------------------------- DEBUG --------------------------------------
Log.print("Loaded new script: " .. SCRIPT_NAME .. " from: " .. SCRIPT_PATH)

-- ClassTest.func_class_test(2,5)
-- ClassTest.func_test(7,51)

-- num = rnd.randint(1, 10)
-- Log.print(num, "module-debug")

-- dt = datetime.datetime
-- now = dt.now()
-- current_time = now.strftime("%H:%M:%S")
-- Log.print(current_time, "module-debug")

-------------------------------------- GAME STUFF --------------------------------------

VN.putVar("game_state", 0)

function onSpaceEvent()
    if VN.getVar('game_state') == 2 then
        pSceneUtils:nextClickEvent()
    end
end

function initKeyStuff()
    events.registerKeyDownEvent(K_SPACE, "onSpaceEvent")
end

function initSFX()
    core.getAudioManager().load_sfx("sweep", "assets/sound/sweep.wav")
end

function initBgMusic()
    core.getAudioManager().load_music("assets/sound/hidamari.mp3")
    core.getAudioManager().play_music(-1, 7000)
    core.getAudioManager().set_music_volume(0.05)
end

function initButtons()
    pFirstButton:setId("firstBtn")
    pFirstButton:setText("Play")
    pFirstButton:setPos(SCREEN_WIDTH/2.5, SCREEN_HEIGHT/2.5)
    pFirstButton:setSize(200, 50)

    -- wtf, why i'm not using addText? idk, i like this shit
    pSecondButton:setId("secBtn")
    pSecondButton:setText("VNCore 0.6-stable")
    pSecondButton:setPos(SCREEN_WIDTH/2.5, SCREEN_HEIGHT/1.5)
    pSecondButton:setSize(200, 50)
    pSecondButton:setTextColor(0,0,0,255)
    pSecondButton:setBackgroundColor(0,0,0,0)
    -- pSecondButton:setDisabled(true)
end

-------------------------------------- GLOBAL EVENTS --------------------------------------

-- Calling when game starting
function onGameStart()
    VN.log("onGameStart")

    core.setTitle(GAME_TITLE)
    core.setIcon(render.getImageManager().load_image(GAME_ICON))

    initSFX()
    initBgMusic()
    initKeyStuff()
    initButtons()
    
    VN.putVar("game_state", 1)
    VN.putVar("test", 1)
    VN.delVar("test")

    -- Set the folder path to "data"
    -- fm:set_folder_path("data")

    -- Create a file called "example.txt" with the content "Hello, world!"
    -- fm:create_file("example.txt", "Hello, world!")

    -- save_game(1, "228")
    -- load_game(1)
    pSceneUtils:loadScripts()
end

-- Calling when mouse click
function onTouchEvent(button, x, y)
    -- Log.print("onTouchEvent -> button ("..button..") clicked at ("..x..", "..y..")")

    if VN.getVar('game_state') == 1 then
        if pFirstButton:isHovered(x, y) and pFirstButton:getPressed() == false then
            -- Log.print("First Button Pressed")
            pFirstButton:press()
        end

        return
    end

    pSceneUtils:nextClickEvent()
end

-- Calling when touch end
function onTouchEndEvent(button, x, y)
    if pFirstButton:isHovered(x, y) and pFirstButton:getPressed() == true then
        VN.putVar("game_state", 2)
        pFirstButton:unpress()
    end
end

-- Calling when touch move
function onTouchMoveEvent(x, y)
    -- todo
end

-- Render (Calling every frame)
function onGameRender()
    if VN.getVar('game_state') == 1 then
        pFirstButton:draw()
        pSecondButton:draw()

        x, y = VN.getMousePos()
        if pFirstButton:isHovered(x, y) then
            render.getButtonManager().set_hovered(true)
        else
            render.getButtonManager().set_hovered(false)
        end
    elseif VN.getVar('game_state') == 2 then
        pSceneUtils:drawScene()
    end
end
