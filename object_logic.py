import pygame as pg
from settings import *
from objects import *
from random import randint

class Spawn():
    '''Basic class to determine whether or not a rock or a confetti should spawn
    
    The object of the class should be called by its update method'''
    def __init__(self, game):
        self.game = game
        self.spawn_ticker = 0
        self.stop_rock_spawn = False
        self.has_celebrated = False

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

    def spawn_rocks(self):
        if self.spawn_ticker <= 0 and not self.stop_rock_spawn :
            self.game.rocks.append(Rock(self.game))
            self.spawn_ticker = self.set_spawn_ticker(self.game.player.score) #uses the score of the player to determine the spawn rate

    def spawn_confettis(self):
        if not self.has_celebrated :
            if self.game.player.check_best_score() :
                self.stop_rock_spawn = True
                now = pg.time.get_ticks()
            
                if now - self.game.player.best_score_time < CELEBRATION_TIME * 0.7 :
                        if self.spawn_ticker <= 0 :
                            self.game.confettis.append(Confettis(self.game))
                            self.spawn_ticker = 1
                elif now - self.game.player.best_score_time < CELEBRATION_TIME :
                    pass #this gives the player a few seconds before the rocks start spawning again
                else :
                    self.has_celebrated = True
                    self.stop_rock_spawn = False


    def update(self):
        self.spawn_rocks()
        self.spawn_confettis()
        self.spawn_ticker -= 1
