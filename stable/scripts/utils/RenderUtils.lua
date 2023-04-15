RenderUtils = {}

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

function RenderUtils.initialize()
    Log.print("Initializing RenderUtils..", "RenderUtils")
	local render = VN.getCore().getRender()
    render.getRenderFlags().set_flags(FLAG_USE_DEFAULT_DISPLAY_FLAGS | FLAG_USE_DEFAULT_SURFACE_FLAGS | FLAG_DONT_AUTO_RENDER_IMAGES | FLAG_DONT_LOAD_DEFAULT_FONT)
    render.setScreenSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    render.Initialize()
end

function RenderUtils.renderSubtitle(speaker, text)
	local render = VN.getCore().getRender()
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