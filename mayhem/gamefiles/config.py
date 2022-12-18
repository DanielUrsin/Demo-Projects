import pygame
pygame.init()
pygame.mixer.quit()

# Setting up pygame display window
SCREEN_X = 1920
SCREEN_Y = 1080
SCREENSIZE = (SCREEN_X, SCREEN_Y)
SCREEN = pygame.display.set_mode(SCREENSIZE, )#pygame.FULLSCREEN)
pygame.display.set_caption("Mayhem Clone 2k")
FONT = pygame.font.Font(None, 35)
SPRITE = pygame.sprite.Sprite

######### Game settings ###############
REFRESH = 75
GRAVITY = 1500 / REFRESH
MAXSPEED = 375 / REFRESH
ACCELERATION = 6000 / REFRESH
STARTINGFUEL = 400
MAXFUEL = 500
CONSUME = 20 / REFRESH
STARTINGANGLE = 90.0
TILTRATE = 180 / REFRESH
#######################################

WHITE = (175, 175, 175)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (100, 100, 255)
GREEN = (0, 255, 0)
BULLETBLUE = (200, 200, 255)

LEFT_SPAWN = SCREEN_X * 1/8, SCREEN_Y * 1/2
RIGHT_SPAWN = SCREEN_X * 7/8, SCREEN_Y * 1/2

# Dynamic object graphics
SHIP_ACC = pygame.image.load('gamefiles/spaceship1_accelerating.png').convert()
SHIP_COAST = pygame.image.load('gamefiles/spaceship1_coasting.png').convert()
BARREL = pygame.image.load('gamefiles/Barrel.png').convert()
BULLET = pygame.Surface((10, 10)).convert()
pygame.draw.circle(BULLET, BULLETBLUE, (5, 5), 2, 0)

# Stationary object graphics
FRAME_HORIZONTAL = pygame.Surface((SCREEN_X, 10)).convert()
FRAME_HORIZONTAL.fill(WHITE)
FRAME_VERTICAL = pygame.Surface((10, SCREEN_Y)).convert()
FRAME_VERTICAL.fill(WHITE)
OBSTACLE = pygame.Surface((10, SCREEN_Y/2 - 100)).convert()
OBSTACLE.fill(WHITE)
