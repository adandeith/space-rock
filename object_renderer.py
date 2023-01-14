import pygame as pg
from settings import *
import math, time
from pathfix import *

class ObjectRenderer():
    '''Class used to update and display fixed element on the game like text (score, lives...), game board, game over image...'''
    def __init__(self, game):
        self.game = game

        self.board_img = self.load_image(resource_path('assets\\img\\Board.png'))
        self.board_size = self.get_size(self.board_img)
        self.board_pos = ((WIDTH//2) - (self.board_size[0]//2)), 0

        self.regular_font = self.game.regular_font
        self.title_font = self.game.title_font
        self.instruction_font =self.game.instruction_font
        self.text_color = (0, 0, 0)


    def draw_board(self) :
        self.game.screen.blit(self.board_img, self.board_pos)

    def draw_score(self):
        #on récupère la position du board pour dessiner le score
        x = self.board_pos[0] + self.board_size[0]*0.81 
        y = self.board_pos[1] + self.board_size[1]*0.27
        pos = x, y 

        score = self.regular_font.render(f'x  {str(self.game.player.score).zfill(5)}', True, self.text_color)
        self.game.screen.blit(score, pos)

    def draw_health(self):
        x = self.board_pos[0] + self.board_size[0]*0.13 
        y = self.board_pos[1] + self.board_size[1]*0.27
        pos = x, y 

        health = self.regular_font.render(str(self.game.player.health), True, self.text_color)
        self.game.screen.blit(health, pos)

    def draw_special(self):
        x = self.board_pos[0] + self.board_size[0]*0.355 
        y = self.board_pos[1] + self.board_size[1]*0.35
        color = (231, 51, 42)
        visual_lenght = 125 #If the special bar changes size, the new size in pixel must be specified here
        #The width is calculated based on the max special score (SPECIAL INTERVAL) and the size of the bar
        width = (((self.game.player.special_score*100)/SPECIAL_ATTACK_INTERVAL)*visual_lenght)/100
        height = 16

        special = pg.draw.rect(self.game.screen, color, ((x,y), (width, height)))

    def title_screen(self):
        oscillation = self.set_oscillation()

        img = self.game.image_background
        img_pos = (0, 0)

        title_txt = 'Space Rocks'
        title_size = self.title_font.size(title_txt)
        title_pos = WIDTH//2 - title_size[0]//2, HEIGHT//2 - title_size[1]//2 + oscillation 
        title_display = self.title_font.render(str(title_txt), True, self.text_color)

        instruction_txt = 'Press Enter to play'
        instruction_size = self.instruction_font.size(instruction_txt)
        instruction_pos = WIDTH//2 - instruction_size[0]//2, title_pos[1] + title_size[1] + 40 
        instruction_display = self.instruction_font.render(str(instruction_txt), True, self.text_color)

        self.game.screen.blit(img, img_pos)
        self.game.screen.blit(title_display, title_pos)
        self.game.screen.blit(instruction_display, instruction_pos)

    def game_over(self):
        now = pg.time.get_ticks()
        oscillation = self.set_oscillation()
        img = self.game.image_background
        img_pos = (0, 0)

        title_txt = 'Game Over'
        title_size = self.title_font.size(title_txt)
        title_pos = WIDTH//2 - title_size[0]//2, HEIGHT//2 - title_size[1]//2 + oscillation 
        title_display = self.title_font.render(str(title_txt), True, self.text_color)

        instruction_txt = f'Your score : {self.game.player.score}'
        instruction_size = self.instruction_font.size(instruction_txt)
        instruction_pos = WIDTH//2 - instruction_size[0]//2, title_pos[1] + title_size[1] + 40  
        instruction_display = self.instruction_font.render(str(instruction_txt), True, self.text_color)

        instruction2_txt = 'Programming / Design / Sound       adandeith'
        instruction2_size = self.instruction_font.size(instruction2_txt)
        instruction2_pos = WIDTH//2 - instruction2_size[0]//2, instruction_pos[1] + instruction_size[1] + 25
        instruction2_display = self.instruction_font.render(str(instruction2_txt), True, self.text_color)

        instruction3_txt = "Main theme 'Street lamps'            penugwin"
        instruction3_size = self.instruction_font.size(instruction3_txt)
        instruction3_pos = WIDTH//2 - instruction3_size[0]//2, instruction2_pos[1] + instruction2_size[1] + 5 
        instruction3_display = self.instruction_font.render(str(instruction3_txt), True, self.text_color)

        self.game.screen.blit(img, img_pos)
        self.game.screen.blit(title_display, title_pos)
        self.game.screen.blit(instruction_display, instruction_pos)
        self.game.screen.blit(instruction2_display, instruction2_pos)
        self.game.screen.blit(instruction3_display, instruction3_pos)

        if now - self.game.player.death_time > GAMEOVER_TIME:
            self.game.new_game()

    def pause(self):
        oscillation = self.set_oscillation()

        title_txt = 'Pause'
        title_size = self.title_font.size(title_txt)
        title_pos = WIDTH//2 - title_size[0]//2, HEIGHT//2 - title_size[1]//2 + oscillation 
        title_display = self.title_font.render(str(title_txt), True, self.text_color)

        instruction_txt = 'Press Escape to resume'
        instruction_size = self.instruction_font.size(instruction_txt)
        instruction_pos = WIDTH//2 - instruction_size[0]//2, HEIGHT//2 + title_size[1] - instruction_size[1]//2 + oscillation 
        instruction_display = self.instruction_font.render(str(instruction_txt), True, self.text_color)

        self.game.screen.blit(title_display, title_pos)
        self.game.screen.blit(instruction_display, instruction_pos)


    def load_image(self, img):
        return pg.image.load(img).convert_alpha()

    def set_oscillation(self):
        return math.sin(time.time()*6)*6 

    def get_size(self, img):
        return img.get_width(), img.get_height()

    def draw(self):
        self.draw_board()
        self.draw_score()
        self.draw_health()
        self.draw_special()
