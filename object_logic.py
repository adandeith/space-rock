import pygame as pg
from settings import *
from objects import *
from random import randint

class Spawn():
    '''Basic class to determine whether or not a rock should spawn
    
    The object of the class should be called by its update method'''
    def __init__(self, game):
        self.game = game
        self.spawn_ticker = 0

    def set_spawn_ticker(self, base):
        random = randint(0, 3)

        if base < SPECIAL_ATTACK_INTERVAL :
            ticker_value = random * (100/(base + 1))
        elif base < 50 :
            ticker_value = random * (400/(base + 1))
        elif base < 100 :
            ticker_value = random * (800/(base + 1))
        else :
            ticker_value = random * (1200/(base + 1))

        return ticker_value

    def spawn(self):
        if self.spawn_ticker <= 0 :
            self.game.rocks.append(Rock(self.game))
            self.spawn_ticker = self.set_spawn_ticker(self.game.player.score) #uses the score of the player to determine the spawn rate

    def update(self):
        self.spawn()
        self.spawn_ticker -= 1
