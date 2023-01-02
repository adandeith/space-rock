import pygame as pg
from settings import *
import os
from collections import deque
from random import uniform, randint, random

error_compensation = 0.001


class Background :
    def __init__(self, game) :
        self.game = game
        self.x = 0
        self.y = 0
        self.image = self.game.image_background
        self.speed = SCROLL_SPEED - 2

    def update(self):
        self.x = (self.x - self.speed) % -WIDTH

    def draw (self):
        self.game.screen.blit(self.image, (self.x,self.y))
        self.game.screen.blit(self.image, (self.x + WIDTH-error_compensation,self.y))

class Ground(Background):
    def __init__(self, game):
        super().__init__(game)
        self.y = GROUND_Y_START #les vagues commencent à 82% de l'illustration totale en partant du haut
        self.speed = SCROLL_SPEED 
        self.image = self.game.image_ground


class FixedObject() :
    def __init__(self, game, image_path : str):
        self.game = game
        self.image = pg.image.load(image_path).convert_alpha()
        self.position = self.x, self.y = 0,0

    def draw(self):
        self.game.screen.blit(self.image, self.pos)

    @property
    def pos(self) :
        return self.x, self.y
    
    @property
    def size(self):
        '''Returns a tuple with with the width and height of the image'''
        return self.image.get_width(), self.image.get_height()


class Board(FixedObject):
    def __init__(self, game, image_path = 'assets/Board V2.2.png'):
        super().__init__(game, image_path)
        self.x = (WIDTH//2) - (self.size[0]//2) #centre le board au milieu de l'écran en haut
        self.y = 0

class GameOver(FixedObject):
    def __init__(self, game, image_path= 'assets/Game Over.png'):
        super().__init__(game, image_path)

class FlyingObject(pg.sprite.Sprite):
    '''Simple class to create an object going from the right side of the screen to the left
    
    The optionnal argument folder_name must the name of a sub-folder where images of the object are saved.
    For example : passing the argument folder_name = ROCK will generate a path ..\\assets\ROCK.

    If folder_name is not completed, the class will generate a circle with no image.
    '''
    def __init__(self, game, x = WIDTH, folder_name = None):
        super().__init__()
        self.game = game
        self.x = x
        self.y = randint(int(HEIGHT * 0.1), int(HEIGHT * 0.9))
        self.size = OBJECT_SIZE
        self.speed = FLYING_SPEED*uniform(0.3, 0.5)*self.game.dt
        self.path = folder_name
        self.used_image = None
        self.is_dead = False

        if not folder_name : 
            self.color = self.set_color()
            self.rect = pg.Rect(self.x, self.y, self.size, self.size)
        else :
            self.images = self.get_images(self.path)
            #self.image = pg.image.load(self.game.assets_dir + image_name).convert_alpha()
            self.used_image = self.images[0]
            self.rect = self.used_image.get_rect()
            self.rect.topleft = (self.pos)

    def set_color(self):
        random_number = random()
        random_color = ''
        if random_number >= 0.75 :
            random_color = 'red'
        elif random_number >= 0.5 :
            random_color = 'green'
        elif random_number >= 0.25 :
            random_color = "yellow"
        else :
            random_color = 'blue'
        return random_color

    def move(self):
        dx = - self.speed
        dy = 0

        self.x += dx
        self.y += dy

        self.move_rect()

    def move_rect(self):
        '''Internal function to update the rect position of the projectile'''
        self.rect.topleft = (self.pos)

    def update(self):
        self.move()

    def draw (self) :
        if self.used_image :
            object = self.game.screen.blit(self.used_image, self.rect)
        else :
            object = pg.draw.circle(self.game.screen, self.color, self.pos, self.size)  

    def is_offscreen(self) -> bool :
        if self.x + (2 * self.game.dt) <= 0 :
            return True
        else :
            return False

    def get_images(self, folder) :
        '''Internal function to search and stack images from a folder in a list-like element'''
        images = deque()
        for file in os.listdir(folder) :
            if os.path.isfile :
                img = pg.image.load(folder + '\\' + file).convert_alpha()
                images.append(img)
        return images

    def change_image(self):
        '''Function used to change the image of the object and resets the rect attribute to fit the new image'''
        self.used_image = self.images[1]
        self.rect = self.used_image.get_rect()
        self.rect.topleft = self.pos

    @property
    def pos(self):
        return self.x, self.y

class Rock(FlyingObject) :
    def __init__(self, game, x=WIDTH, folder_name = 'assets/rock'):
        super().__init__(game, x, folder_name)

    def check_collision(self) :
        if not self.is_dead and not self.is_offscreen():
            for projectile in self.game.projectiles :
                collision = projectile.rect.colliderect(self.rect)
                if collision :
                    self.change_image()
                    self.is_dead = True
                    self.game.projectiles.remove(projectile)
                    self.game.player.score += 1
                    break
                
        player_collision = self.game.player.rect.colliderect(self.rect)
        if not self.is_dead and not self.is_offscreen() and player_collision :
            self.change_image()
            self.is_dead = True
            self.game.player.get_damage(1)
            
    def update(self):
        self.check_collision()
        self.move()

class Confettis(FlyingObject) :
    def __init__(self, game, x=WIDTH):
        super().__init__(game, x)
