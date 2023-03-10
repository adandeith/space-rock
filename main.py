#main game file
import pygame as pg
import time
import sys
from settings import *
from projectile import *
from player import *
from objects import *
from object_renderer import *
from sound import *
from pathfix import *
from object_logic import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES) #crée un écran de surface res
        self.clock = pg.time.Clock()
        self.dt = 1
        self.projectiles = []
        self.special_projectiles = []
        self.rocks = []
        self.confettis = []
        self.best_score = 0
        self.title_screen = True
        self.game_over = False
        self.pause_screen = False
        self.ticker = 0
        self.load_static_assets()
        self.new_game() #à l'initialisation, on lance la méthode nouveau jeu

    def load_static_assets(self):
        self.image_background = pg.image.load(resource_path('assets\\img\\BackgroundLarge.png')).convert() #on va chercher l'image dans le dossier des assets 
        self.image_background = pg.transform.scale(self.image_background, RES) #transforme l'image en fonction de la résolution

        self.image_ground = pg.image.load(resource_path('assets\\img\\GroundLarge.png')).convert()
        self.image_ground = pg.transform.scale(self.image_ground, (WIDTH, GROUND_RATIO))

        self.image_player = pg.image.load(resource_path('assets\\player\\Swordfish_resize.png')).convert_alpha()

        self.regular_font = pg.font.Font(resource_path('assets\\font\\Franchise.ttf'), int(REGULAR_FONT_SIZE))
        self.title_font = pg.font.Font(resource_path('assets\\font\\Franchise.ttf'), int(TITLE_FONT_SIZE))
        self.instruction_font = pg.font.Font(resource_path('assets\\font\\Franchise.ttf'), int(INSTRUCTION_FONT_SIZE))


    def new_game(self):

        self.projectiles.clear()
        self.rocks.clear()
        self.confettis.clear()
        
        self.title_screen = True
        self.game_over = False
        self.pause_screen = False

        self.object_renderer = ObjectRenderer(self)
        self.player = Player(self)
        self.background = Background(self)
        self.ground = Ground(self)
        self.sound = Sound(self)
        self.spawn = Spawn(self)

        

    def check_event(self):
        '''checks if the player presses certain keys to create actions'''
        key = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT : 
                pg.quit()
                sys.exit()
            if key[pg.K_RETURN] and self.title_screen :
                if self.ticker <= 0 :
                    self.title_screen = False
                    self.ticker = KEYBOARD_PRESS_TIME
            if key[pg.K_ESCAPE] and not self.pause_screen and not self.game_over and not self.title_screen :
                if self.ticker <= 0 :
                    self.pause_screen = True
                    self.ticker = KEYBOARD_PRESS_TIME
            if key[pg.K_ESCAPE] and self.pause_screen :
                if self.ticker <= 0 :
                    self.pause_screen = False
                    self.ticker = KEYBOARD_PRESS_TIME


    def update (self):
        '''updates the position of elements on screen and show the fps'''
        if not self.title_screen and not self.pause_screen and not self.game_over :
            self.player.update()
            self.background.update()
            self.ground.update()
            self.spawn.update()

            for projectile in self.projectiles : 
                self.projectiles.remove(projectile) if projectile.is_offscreen() else projectile.update() #supprime l'object projectile de la la liste projectiles si l'objet est hors de l'écran (check si hors écran via la fonction spéciale is_offscreen de la classe Projectile())

            for special in self.special_projectiles : 
                self.special_projectiles.remove(special) if special.is_offscreen() else special.update()

            for confetti in self.confettis : 
                self.confettis.remove(confetti) if confetti.is_offscreen() else confetti.update()

            for rock in self.rocks :  
                self.rocks.remove(rock) if rock.is_offscreen() else rock.update()
         
        self.sound.update() 
        self.ticker -= 1
        pg.display.flip()
        self.dt = self.clock.tick(FPS) #paramètre le nombre de fps max du jeu avec le paramètre fps et stock la valeur dans une variable dt
        pg.display.set_caption(f'Space Rocks ({self.clock.get_fps() :.1f})') #affiche les fps réels avec une décimale


    def draw(self):
        '''resets the screen and draw the updated elements on screen'''
        if not self.title_screen and not self.game_over:
            self.background.draw()
            self.ground.draw()
            self.player.draw()
            for projectile in self.projectiles :
                projectile.draw()
            for special in self.special_projectiles :
                special.draw()
            for object in self.rocks :
                object.draw()
            for confetti in self.confettis :
                confetti.draw()
            self.object_renderer.draw()
            if self.pause_screen :
                self.object_renderer.pause()
        elif self.title_screen :
            self.object_renderer.title_screen()
        elif self.game_over :
            self.object_renderer.game_over()


    def run(self):
        while True :
            self.check_event()
            self.update()
            self.draw()

        
if __name__ == '__main__' :
    game = Game()
    game.run()
