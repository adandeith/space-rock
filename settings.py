#screen settings
RES = WIDTH, HEIGHT =1200, 720 #900,600
FPS = 60
SCROLL_SPEED = 3.5
REGULAR_FONT_SIZE = 25
TITLE_FONT_SIZE = 125

#player settings
PLAYER_POS = x,y = WIDTH//4, HEIGHT //2
PLAYER_SPEED = 0.4
PLAYER_SIZE = 20
PLAYER_SCALE = 1
PLAYER_GUN_POS_RATIO = 1 - 0.22
PLAYER_LIVES = 9
SHOOTING_INTERVAL = 15

#ground settings
GROUND_RATIO = HEIGHT * 0.18 #the background (900x600px) was designed so that the wave part is roughly 108px heigh -> 108/600 = 18%
GROUND_Y_START = HEIGHT - GROUND_RATIO

#projectile settings
BULLET_SPEED = 0.25
BULLET_SIZE = 5

#objects settings
OBJECT_SIZE = 10
FLYING_SPEED = 1
HIT_Y_MARGIN = 1

#other settings
GAMEOVER_TIME = 4000 #pygame counts in milliseconds, 5000ms = 5s
KEYBOARD_PRESS_TIME = 10