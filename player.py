import pygame as pg
from settings import *
from main import Game
from projectile import Projectile, SpecialProjectile


class Player(pg.sprite.Sprite):
    def __init__(self, game : Game) :
        super().__init__()
        self.game = game
        self.x, self.y = PLAYER_POS
        self.image = self.game.image_player
        self.rect = self.image.get_rect()
        self.player_width = self.image.get_width()
        self.player_height = self.image.get_height()
        self._health = PLAYER_LIVES
        self._score = 0
        self._death_time = 9000
        self._ticker_shoot = 0
        self._ticker_damage = 0
        self._special_score = 0
        self._best_score_time = 0
        self.best_score_found = False

    def check_shoot(self):
        key = pg.key.get_pressed()
        shoot = key[pg.K_SPACE]
        special_shoot = key[pg.K_s]
        if shoot and self.ticker_shoot <= 0 :
            self.game.projectiles.append(Projectile(self.game))
            self.ticker_shoot = SHOOTING_INTERVAL
            self.game.sound.shoot.play()

        if special_shoot and self.special_score == SPECIAL_ATTACK_INTERVAL :
            self.game.special_projectiles.append(SpecialProjectile(self.game))
            self.special_score = 0
            self.game.sound.missile.play()

    def set_special_score(self, score):
        ds = self.special_score + score
        if ds <= SPECIAL_ATTACK_INTERVAL :
            self.special_score += score

    def get_damage(self, damage):
        '''Method used to damage the player health
        
        When the player gets damage, a ticker is set.
        At each frame, the ticker gets -1 in the update method. If the player is touched while the ticker is superior to 0, he doesn't get any damage.
        This allows the player some invicibility time between two touches'''
        if self.ticker_damage <= 0 :
            self.health -= damage
            self.ticker_damage = INVINCIBILITY_TIME
            self.game.sound.hit.play()
            self.check_game_over()

    def check_game_over(self):
        if self.health <=0 :
            self.game.game_over = True
            self.death_time = pg.time.get_ticks()
            if self.score > self.game.best_score :
                self.game.best_score = self.score

    def check_best_score(self) -> bool :
        '''Method to check if the current score is higher than the one in the last game
        If a best score is found, the time will be updated (best_score_time) and the method will return True'''
        if not self.best_score_found :
                self.best_score_time = pg.time.get_ticks()
        if self.score > self.game.best_score and self.game.best_score > 0 :
            self.best_score_found = True
            return True


    def check_move(self):
        key = pg.key.get_pressed()
        go_left = key[pg.K_LEFT] 
        go_right = key[pg.K_RIGHT]  
        go_up = key[pg.K_UP] 
        go_down = key[pg.K_DOWN]
        
        dx, dy = 0, 0
        speed = self.game.dt * PLAYER_SPEED

        #simple up, down, left and right controls
        if go_left :
            dx = -speed
            dy = 0
        if go_right :
            dx = speed
            dy = 0
        if go_up :
            dx = 0
            dy = -speed
        if go_down :
            dx = 0
            dy = speed

        #combined controls
        if go_left and go_up :
            dx = -speed
            dy = -speed
        if go_left and go_down :
            dx = -speed
            dy = speed
        if go_right and go_up :
            dx = speed
            dy = -speed
        if go_right and go_down:
            dx = speed
            dy = speed

        self.check_wall_collision(dx,dy)


    def check_wall_collision(self, dx, dy):
        '''Internal method to check if the player will go off screen when pressing a key and moving'''
        x_position = self.x + dx
        y_position = self.y + dy

        if x_position + self.player_width <= WIDTH :
            if x_position >= 0 :
                self.x += dx
        if y_position + self.player_height <= HEIGHT :
            if y_position >= 0 :
                self.y += dy

    def move_rect(self):
        '''Internal method to update the rect position of the projectile'''
        self.rect.topleft = (self.pos)

    def draw(self):
        #pg.draw.circle(self.game.screen, 'white', (self.x, self.y), PLAYER_SIZE)
        try :
            player = self.game.screen.blit(self.image, (self.x, self.y))
        except :
            player = pg.draw.circle(self.game.screen, 'white', (self.x, self.y), PLAYER_SIZE)

    def update(self):
        self.check_move()
        self.move_rect()
        self.check_shoot()
        self.ticker_shoot -= 1
        self.ticker_damage -= 1

    @property
    def pos(self) :
        return self.x, self.y

    @property
    def health(self):
        return self._health

    @property
    def death_time(self):
        return self._death_time

    @property
    def score(self):
        return self._score

    @property
    def special_score(self):
        return self._special_score

    @special_score.setter
    def special_score(self, new_value):
        self._special_score = new_value

    @property
    def ticker_shoot(self):
        return self._ticker_shoot

    @ticker_shoot.setter
    def ticker_shoot(self, new_value):
        self._ticker_shoot = new_value

    @property
    def ticker_damage(self):
        return self._ticker_damage

    @ticker_damage.setter
    def ticker_damage(self, new_value):
        self._ticker_damage = new_value

    @health.setter
    def health(self, new_value):
        self._health = new_value

    @score.setter
    def score(self, new_value):
        self._score = new_value

    @death_time.setter
    def death_time(self, new_value):
        self._death_time = new_value

    @property
    def best_score_time(self):
        return self._best_score_time 

    @best_score_time.setter
    def best_score_time(self, new_value):
        self._best_score_time = new_value