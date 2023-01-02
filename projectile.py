import pygame as pg
from settings import *

class Projectile(pg.sprite.Sprite):
    '''Class to create moving object like bullets where the player stands and update its position through time

    In order to get screen frame rate, player position etc, the class takes a 'game' argument which is 'self' if the class is called from the main game class '''
    def __init__(self, game) :
        super().__init__()
        self.game = game
        self.x = self.game.player.x + self.game.player.player_width
        self.y = self.game.player.y + self.game.player.player_height * PLAYER_GUN_POS_RATIO
        self.dt = self.game.dt
        self.direction = 1
        self.rect = pg.Rect(self.x, self.y, BULLET_SIZE, BULLET_SIZE) #création d'un rectangle équivalent à la balle tirée par le joueur (utilisé pour vérifier la collision)
    
    def move(self): 
        speed = self.direction * self.dt * BULLET_SPEED
        dx = speed
        dy = 0 #la balle ne se déplace pas sur l'axe y, elle ne fait qu'aller à droite (axe x)

        self.x += dx
        self.y += dy

        self.move_rect()

    def move_rect(self):
        '''Internal function to update the rect position of the projectile'''
        self.rect.topleft = (self.pos)

    def update(self):
        self.move()

    def draw(self):
        projectile = pg.draw.circle(self.game.screen, 'green', (self.pos), BULLET_SIZE)

    def is_offscreen(self) :
        if self.x > WIDTH or self.y < 0 :
            return True
        else :
            return False

    @property
    def pos(self):
        return self.x, self.y
