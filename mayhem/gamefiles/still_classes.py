from gamefiles import config as c

import random
import math
import pygame

pygame.init()
pygame.mixer.quit()

class Frame(c.SPRITE):
    '''Class for obstacles and frame objects.'''
    def __init__(self, image, pos):
        c.SPRITE.__init__(self)
        self.import_image = image
        self.image = self.import_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Barrel(c.SPRITE):
    '''Class for fuel barrel objects. '''
    def __init__(self):
        c.SPRITE.__init__(self)
        self.import_image = c.BARREL
        self.image = self.import_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, c.SCREEN_X)
        self.rect.y = random.randint(0, c.SCREEN_Y-100)


class Score(c.SPRITE):
    '''Class for writing player scores on screen.
       Takes a text string and a set of coordinates
       as input.'''
    def __init__(self, text, pos):
        c.SPRITE.__init__(self)
        self.text = text
        self.pos = pos
        self.value = 0
        input = "{}: {}".format(self.text, self.value)
        self.import_image = c.FONT.render(input, True, c.WHITE)
        self.image = self.import_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update(self):
        input = "{}: {}".format(self.text, self.value)
        self.import_image = c.FONT.render(input, True, c.WHITE)
        self.image = self.import_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos


class Gauge(c.SPRITE):
    '''Class for ship fuel gauge object.
       Takes initialized ship object as input.'''
    def __init__(self, ship):
        c.SPRITE.__init__(self)
        self.ship = ship

        height = round(self.ship.fuel / c.MAXFUEL * self.ship.rect.h)
        start_point = (self.ship.rect.x - 5, self.ship.rect.y)
        gauge = pygame.Surface((3, height))

        if 0 < height < 10:
            gauge.fill(c.RED)
        elif height >= 10:
            gauge.fill(c.GREEN)
        elif height == 0:
            gauge.fill(c.BLACK)

        self.import_image = gauge
        self.image = self.import_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_point


    def update(self):
        height = round(self.ship.fuel / c.MAXFUEL * self.ship.rect.h)
        start_point = (self.ship.rect.x - 5, self.ship.rect.y)
        gauge = pygame.Surface((3, height))

        if 0 < height < 10:
            gauge.fill(c.RED)
        elif height >= 10:
            gauge.fill(c.GREEN)
        elif height == 0:
            gauge.fill(c.BLACK)

        self.import_image = gauge
        self.image = self.import_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_point
