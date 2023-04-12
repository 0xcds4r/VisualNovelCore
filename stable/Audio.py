import pygame
from pygame import mixer

class AudioManager:
    def __init__(self, core):
        self.core = core
        self.music = None
        self.sfx = {}

    def getCore(self):
        return self.core

    def load_music(self, file_path):
        pygame.mixer.music.load(file_path)

    def play_music(self, loop=-1, fade_in_time=0):
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.play(loop, fade_ms=fade_in_time)

    def stop_music(self, fade_out_time=0):
        pygame.mixer.music.fadeout(fade_out_time)

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def load_sfx(self, name, file_path):
        self.sfx[name] = pygame.mixer.Sound(file_path)

    def play_sfx(self, name, fade_in_time=0):
        self.sfx[name].fadeout(1000)
        self.sfx[name].play(fade_ms=fade_in_time)

    def stop_sfx(self, name, fade_out_time=0):
        self.sfx[name].fadeout(fade_out_time)

    def set_sfx_volume(self, name, volume):
        self.sfx[name].set_volume(volume)