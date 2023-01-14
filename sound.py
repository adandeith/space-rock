import pygame as pg
from settings import *
from pathfix import *

class Sound():
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'assets\\sound\\'
        self.hit = pg.mixer.Sound(resource_path(self.path + 'hitHurt.wav'))
        self.explosion = pg.mixer.Sound(resource_path(self.path + 'explosion.wav'))
        self.big_explosion = pg.mixer.Sound(resource_path(self.path + 'bigExplosion.wav'))
        self.shoot = pg.mixer.Sound(resource_path(self.path + 'laserShoot.wav'))
        self.missile = pg.mixer.Sound(resource_path(self.path + 'missileShoot.wav'))
        self.theme = pg.mixer.music.load(resource_path(self.path + 'retroTheme.mp3'))

        self.hit.set_volume(0.4)
        self.shoot.set_volume(0.045)
        self.missile.set_volume(0.4)
        self.explosion.set_volume(0.25)

        pg.mixer.music.set_volume(0.6)

        self.plays_theme = False

    def update(self):
        if not self.game.title_screen and not self.plays_theme :
            pg.mixer.music.play(-1)
            self.plays_theme = True
        
        pg.mixer.music.set_volume(0.15) if self.game.pause_screen else pg.mixer.music.set_volume(0.6)

        if self.game.game_over :
            pg.mixer.music.fadeout(int(GAMEOVER_TIME)) 


