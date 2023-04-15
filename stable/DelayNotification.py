import pygame

class DelayNotification:
    def __init__(self, core, x, y, text, text_color, background_color, font, font_size, delay):
        self.core = core
        self.background_color = background_color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font = font
        self.delay = delay
        self.pos = (x, y)
        self.start_time = self.core.GetTickCount()

        self.text_element = self.core.getRender().getTextManager().getTextElement()
        self.text_element.setText(self.text)
        self.text_element.setPosition(self.pos[0], self.pos[1])
        self.text_element.setFont(self.font)
        self.text_element.setFontSize(self.font_size)
        self.text_element.setAlign("left")
        self.text_element.setBold(False)
        self.text_element.setItalic(True)
        self.text_element.setTextColor(self.text_color[0], self.text_color[1], self.text_color[2], self.text_color[3])
        self.text_element.setBgColor(self.background_color[0], self.background_color[1], self.background_color[2], self.background_color[3])
        self.text_element.setStrokeColor(0, 0, 0, 255)
        self.text_element.setStrokeWidth(0.95)

    def update(self):
        self.text_element = self.core.getRender().getTextManager().getTextElement()
        self.text_element.setText(self.text)
        self.text_element.setPosition(self.pos[0], self.pos[1])
        self.text_element.setFont(self.font)
        self.text_element.setFontSize(self.font_size)
        self.text_element.setAlign("left")
        self.text_element.setBold(False)
        self.text_element.setItalic(True)
        self.text_element.setTextColor(self.text_color[0], self.text_color[1], self.text_color[2], self.text_color[3])
        self.text_element.setBgColor(self.background_color[0], self.background_color[1], self.background_color[2], self.background_color[3])
        self.text_element.setStrokeColor(0, 0, 0, 255)
        self.text_element.setStrokeWidth(0.95)

    def show(self):
        hidding_time = self.core.GetTickCount()
        elapsed_time = self.core.GetTickCount() - self.start_time
        if elapsed_time < self.delay:
            # Show the text
            self.update()
            self.text_element.draw()
            hidding_time = self.core.GetTickCount()
            return True
        else:
            alpha = 1.0 - (elapsed_time - self.delay) / 1000.0
            if alpha > 0:
                self.update()
                self.text_element.setAlpha(self.text_element.getAlpha() * alpha)
                self.text_element.draw()
                hidding_time = self.core.GetTickCount()
            return True

        return True