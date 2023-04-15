Button = {}

function Button:new(o)
	o = o or {}
	setmetatable(o, self)
	self.__index = self

	self.id = ""
    self.text = ""
    self.x = 0
    self.y = 0
    self.w = 0
    self.h = 0
    self.font = "assets/arial.ttf"
    self.font_size = 25
    self.text_color_r = 255
	self.text_color_g = 255
	self.text_color_b = 255
	self.text_color_a = 255
	self.bg_color_r = 25
	self.bg_color_g = 25
	self.bg_color_b = 25
	self.bg_color_a = 255
	self.hover_color_r = 25
	self.hover_color_g = 25
	self.hover_color_b = 25
	self.hover_color_a = 155
	self.disabled = false
	self.pressed = false

  	return o
end

function Button:setId(text)
	self.id = id
end

function Button:setText(text)
	self.text = text
end

function Button:setPos(x, y)
	self.x = x
	self.y = y
end

function Button:setSize(w, h)
	self.w = w
	self.h = h
end

function Button:setFontData(font, size)
	self.font = font
	self.font_size = size
end

function Button:setTextColor(r, g, b, a)
	self.text_color_r = r
	self.text_color_g = g
	self.text_color_b = b
	self.text_color_a = a
end

function Button:setBackgroundColor(r, g, b, a)
	self.bg_color_r = r
	self.bg_color_g = g
	self.bg_color_b = b
	self.bg_color_a = a
end

function Button:setHoverColor(r, g, b, a)
	self.hover_color_r = r
	self.hover_color_g = g
	self.hover_color_b = b
	self.hover_color_a = a
end

local function isInRect(x, y, rectX, rectY, rectW, rectH)
    return x >= rectX and x <= rectX + rectW and y >= rectY and y <= rectY + rectH
end

function Button:press()
	self.pressed = true
end

function Button:unpress()
	self.pressed = false
end

function Button:getPressed()
	return self.pressed
end

function Button:isHovered(x, y)
	if isInRect(x, y, self.x, self.y, self.w, self.h) then
		return true
    end

    return false
end

function Button:isPressed(x, y)
	if self.pressed and isInRect(x, y, self.x, self.y, self.w, self.h) then
		return true
    end

    return false
end

function Button:draw()
	render.getButtonManager().createButton(self.id)
    render.getButtonManager().setText(self.text)
    render.getButtonManager().setFont(self.font, self.font_size)
    render.getButtonManager().setColorRGBA(self.text_color_r, self.text_color_g, self.text_color_b, self.text_color_a)
    render.getButtonManager().setSize(self.w, self.h)
    render.getButtonManager().setPosition(self.x, self.y)
    render.getButtonManager().set_bg_color_rgba(self.bg_color_r, self.bg_color_g, self.bg_color_b, self.bg_color_a) 
    render.getButtonManager().set_hover_color_rgba(self.hover_color_r, self.hover_color_g, self.hover_color_b, self.hover_color_a) 
    render.getButtonManager().setDisabled(self.disabled)
    render.getButtonManager().draw()
end