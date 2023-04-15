import pygame
from Log import Log

class Animation:
    def __init__(self, renderer, name, images, frame_duration):
        self.images = images
        self.renderer = renderer
        self.frame_duration = frame_duration
        self.num_frames = len(images)
        self.current_frame = 0
        self.frame_timer = 0
        self.name = name

    def __del__(self):
        self.images = []
        self.renderer = None
        self.frame_duration = 0
        self.num_frames = 0
        self.current_frame = 0
        self.frame_timer = 0
        self.name = None
    
    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames
    
    def draw(self, x, y):
        self.renderer.getCore().getRender().getDisplay().blit(self.images[self.current_frame], (x, y))

class FadeAnimation(Animation):
    def __init__(self, renderer, name, image, duration, fadeIn=True, autoFadeOut=False, autoFadeIn=False):
        super().__init__(renderer, name, [image], duration)
        self.alpha = 0
        self.fade_in = fadeIn
        self.auto_fade_out = autoFadeOut
        self.auto_fade_in = autoFadeIn
    
    def __del__(self):
        self.alpha = 0
        self.fade_in = False
        self.auto_fade_out = False
        self.auto_fade_in = False

    def setFadeIn(self, state):
        self.fade_in = state

    def update(self, dt):
        super().update(dt)
        if self.fade_in:
            self.alpha += int(255 * dt / self.frame_duration)
            if self.alpha >= 255:
                self.alpha = 255
                if self.auto_fade_out:
                    self.setFadeIn(False)
        else:
            self.alpha -= int(255 * dt / self.frame_duration)
            if self.alpha <= 0:
                self.alpha = 0
                if self.auto_fade_in:
                    self.setFadeIn(True)
    
    def draw(self, x, y):
        image = self.images[self.current_frame]
        image.set_alpha(self.alpha)
        self.renderer.getCore().getRender().getDisplay().blit(image, (x, y))

class AnimationRenderer:
    def __init__(self, core):
        Log.print("Initializing AnimationRenderer..")
        self.animations = {}
        self.core = core

    def getCore(self):
        return self.core
    
    def add_animation(self, name, images, frame_duration, fade=False, fade_duration=1000, fadeIn=True, autoFadeOut=False, autoFadeIn=False):
        if fade:
            animation = FadeAnimation(self, name, images[0], fade_duration, fadeIn, autoFadeOut, autoFadeIn)
        else:
            animation = Animation(self, name, images, frame_duration, fadeIn, autoFadeOut, autoFadeIn)
        self.animations[name] = animation

    def clear_animation(self, name):
        if self.animations[name]:
            del self.animations[name]

    def clear_animations(self):
        for name in list(self.animations.keys()):
            if self.animations[name]:
                del self.animations[name]
        self.animations = {}

    def setFadeDirection(self, name, fade_in):
        self.animations[name].setFadeIn(dir)
    
    def update(self, dt):
        for animation in self.animations.values():
            animation.update(dt)
    
    def draw(self, name, x, y):
        self.animations[name].draw(x, y)

    def draw_all(self):
        for animation in self.animations.values():
            animation.draw(0, 0)