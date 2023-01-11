import pygame as pg
from settings import *
from pathfix import *

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
        self.color = (58, 242, 75) #green parrot #(1, 215, 88) #emerald green

    def move(self): 
        speed = self.direction * self.dt * BULLET_SPEED
        dx = speed
        dy = 0 #la balle ne se déplace pas sur l'axe y, elle ne fait qu'aller à droite (axe x)

        self.x += dx
        self.y += dy

        self.move_rect()

    def move_rect(self):
        '''Internal method to update the rect position of the projectile'''
        self.rect.topleft = (self.pos)

    def update(self):
        self.move()

    def draw(self):
        projectile = pg.draw.circle(self.game.screen, self.color, (self.pos), BULLET_SIZE)
    def is_offscreen(self) :
        if self.x > WIDTH or self.y < 0 :
            return True
        else :
            return False

    @property
    def pos(self):
        return self.x, self.y

class SpecialProjectile(Projectile):
    def __init__(self, game):
        super().__init__(game)
        self.image = pg.image.load(resource_path('assets\\img\\Missile.png')).convert_alpha()
        self.rect = self.image.get_rect(top = self.game.player.y - self.image.get_height() - 15 , height = self.image.get_height() + 15)
        self.y = self.game.player.y + ((self.game.player.player_height * PLAYER_GUN_POS_RATIO) - (self.image.get_height())) 
        #to have the image appear exactly where the gun stands, divide self.image.get_height() by 2
        #shooting the missile lower is visually more accurate but the player has to go down a bit after he shot in order to avoid the rocks, which is inconvenient and defeats the purpose of having a special attack

    def draw(self):
        self.game.screen.blit(self.image, self.pos)
