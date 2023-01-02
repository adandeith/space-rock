#main game file
import pygame as pg
import time
import sys
from settings import *
from projectile import *
from player import *
from objects import *
from object_renderer import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES) #crée un écran de surface res
        self.clock = pg.time.Clock()
        self.dt = 1
        self.projectiles = []
        self.rocks = []
        self.confettis = []
        self.title_screen = True
        self.game_over = False
        self.load_static_assets()
        self.new_game() #à l'initialisation, on lance la méthode nouveau jeu

    def load_static_assets(self):
        self.image_background = pg.image.load('assets/BackgroundLarge.png').convert() #on va chercher l'image dans le dossier des assets 
        self.image_background = pg.transform.scale(self.image_background, RES) #transforme l'image en fonction de la résolution

        self.image_ground = pg.image.load('assets/GroundLarge.png').convert()
        self.image_ground = pg.transform.scale(self.image_ground, (WIDTH, GROUND_RATIO))

        self.image_player = pg.image.load('assets/player/Swordfish_resize.png').convert_alpha()

        self.regular_font = pg.font.Font('assets/font/Franchise.ttf', int(REGULAR_FONT_SIZE))
        self.title_font = pg.font.Font('assets/font/Franchise.ttf', int(TITLE_FONT_SIZE))


    def new_game(self):

        self.projectiles.clear()
        self.rocks.clear()
        self.confettis.clear()
        
        self.title_screen = True
        self.game_over = False

        self.object_renderer = ObjectRenderer(self)
        self.player = Player(self)
        self.background = Background(self)
        self.ground = Ground(self)

        

    def check_event(self):
        '''checks if the player presses certain keys to create actions'''
        key = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT or key[pg.K_ESCAPE] : 
                pg.quit()
                sys.exit()
            '''if key[pg.K_SPACE]: #crée un objet de la classe Projectile à chaque clic sur Espace et le stock dans une liste 
                self.projectiles.append(Projectile(self))'''
            if key[pg.K_o]: 
                self.rocks.append(Rock(self))
            if key[pg.K_c]: 
                self.confettis.append(Confettis(self))
            if key[pg.K_RETURN] and self.title_screen :
                self.title_screen = False


    def update (self):
        '''updates the position of elements on screen and show the fps'''
        self.player.update()
        self.background.update()
        self.ground.update()

        for projectile in self.projectiles : 
            self.projectiles.remove(projectile) if projectile.is_offscreen() else projectile.update() #supprime l'object projectile de la la liste projectiles si l'objet est hors de l'écran (check si hors écran via la fonction spéciale is_offscreen de la classe Projectile())

        for confetti in self.confettis : 
            self.confettis.remove(confetti) if confetti.is_offscreen() else confetti.update()

        for rock in self.rocks :  
            self.rocks.remove(rock) if rock.is_offscreen() else rock.update()
         
        pg.display.flip()
        self.dt = self.clock.tick(FPS) #paramètre le nombre de fps max du jeu avec le paramètre fps et stock la valeur dans une variable dt
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}') #affiche les fps réels avec une décimale


    def draw(self):
        '''resets the screen and draw the updated elements on screen'''
        if not self.title_screen :
            self.background.draw()
            self.ground.draw()
            self.player.draw()
            for projectile in self.projectiles :
                projectile.draw()
            for object in self.rocks :
                object.draw()
            for confetti in self.confettis :
                confetti.draw()
            self.object_renderer.draw()
        else :
            self.object_renderer.title_screen()


    def run(self):
        while True :
            self.check_event()
            self.update()
            self.draw()

        
if __name__ == '__main__' :
    game = Game()
    game.run()
