import pygame as pg
from settings import *
import math, time

class ObjectRenderer():
    '''Class used to update and display fixed element on the game like text (score, lives...), game board, game over image...'''
    def __init__(self, game):
        self.game = game

        self.board_img = self.load_image('assets/Board.png')
        self.board_size = self.get_size(self.board_img)
        self.board_pos = ((WIDTH//2) - (self.board_size[0]//2)), 0

        self.regular_font = self.game.regular_font
        self.title_font = self.game.title_font
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

    def title_screen(self):
        oscilation = math.sin(time.time()*6)*6 

        img = self.game.image_background
        img_pos = (0, 0)

        title_txt = 'Space Rocks'
        title_size = self.title_font.size(title_txt)
        title_pos = WIDTH//2 - title_size[0]//2, HEIGHT//2 - title_size[1]//2 + oscilation 
        title_display = self.title_font.render(str(title_txt), True, self.text_color)

        instruction_txt = 'Press Enter to play'
        instruction_size = self.regular_font.size(instruction_txt)
        instruction_pos = WIDTH//2 - instruction_size[0]//2, HEIGHT//2 + title_size[1] - instruction_size[1]//2 + oscilation 
        instruction_display = self.regular_font.render(str(instruction_txt), True, self.text_color)

        self.game.screen.blit(img, img_pos)
        self.game.screen.blit(title_display, title_pos)
        self.game.screen.blit(instruction_display, instruction_pos)

    def game_over(self):
        img = self.game.image_background
        img_pos = (0, 0)

        txt = 'Game Over'
        txt_size = self.title_font.size(txt)
        text_pos = WIDTH//2 - txt_size[0]//2, HEIGHT//2 - txt_size[1]//2
        display = self.title_font.render(str(txt), True, self.text_color)

        self.game.screen.blit(img, img_pos)
        self.game.screen.blit(display, text_pos)


    def load_image(self, img):
        return pg.image.load(img).convert_alpha()

    def get_size(self, img):
        return img.get_width(), img.get_height()

    def draw(self):
        self.draw_board()
        self.draw_score()
        self.draw_health()
