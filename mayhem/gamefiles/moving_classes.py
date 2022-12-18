from gamefiles import config as c

import random
import math
import pygame
from gamefiles.still_classes import Gauge

pygame.init()
pygame.mixer.quit()


class Movement():
    '''Parrent class for all moving on-screen objects.'''
    def __init__(self):
        self.gravity = c.GRAVITY
        self.fuel = c.STARTINGFUEL
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.acc_x = 0.0
        self.acc_y = 0.0
        # Object spawning angle
        self.orientation = c.STARTINGANGLE
        self.tilt = 0
        self.rect = 0
        # Total lenght of acceleration vector
        self.acc_t = 0
        self.consume = 0
        # Sets object reaction state
        self.live = 0
        # Multiplies score gained by fly time
        self.multiplier = 1



    def move(self):
        '''Controls movement and speed of all moving objects'''
        # Makes a ships flight time a factor of score calculation
        if self.live == 1:
            self.multiplier += 0.001

        self.fuel -= self.consume

        # Limits ship fuel capacity
        if self.fuel > c.MAXFUEL:
            self.fuel = c.MAXFUEL
        if self.fuel < 0:
            self.fuel = 0

        # Cancel acceleration if no fuel
        if self.fuel == 0:
            self.import_image = c.SHIP_COAST
            self.acc_x = 0
            self.acc_y = 0

        # Reverses acceleration on y-axis
        self.acc_y *= -1

        # Changes speed based on acceleration.
        # Speed values multiplied by 1000 for higher accuracy
        self.speed_x *= 1000
        self.speed_y *= 1000
        self.speed_x += self.acc_x
        self.speed_y += self.acc_y
        if self.live:
            self.speed_y += self.gravity

        self.speed_x = self.speed_x / 1000
        self.speed_y = self.speed_y / 1000

        #Keeps object speeds inside bounds
        if self.speed_x > self.max_speed:
            self.speed_x = self.max_speed
        if self.speed_x < -self.max_speed:
            self.speed_x = -self.max_speed
        if self.speed_y > self.max_speed:
            self.speed_y = self.max_speed
        if self.speed_y < -self.max_speed:
            self.speed_y = -self.max_speed

        # Changes position based on speed.
        # Rect atributes can not be floats!
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y


    def rotate(self):
        '''Changes acceleration vector and object image orientation
           according to angle. Used by all moving objects.'''
        self.orientation += self.tilt
        self.orientation = self.orientation % 360
        self.acc_x = self.acc_t * math.cos(math.radians(self.orientation))
        self.acc_y = self.acc_t * math.sin(math.radians(self.orientation))

        # Rotate object
        rotated = pygame.transform.rotate(self.import_image, self.orientation - 90)
        rotate_rect = rotated.get_rect()
        chop_rect = self.import_image.get_rect()
        w = (rotate_rect.w - chop_rect.w) /2
        h = (rotate_rect.h - chop_rect.h) /2
        self.image = rotated.subsurface(w, h, self.rect.w, self.rect.h)


class Ship(c.SPRITE, Movement):
    '''Ship object class. Inherits from Movement.'''
    def __init__(self, spawn_point):
        c.SPRITE.__init__(self)
        Movement.__init__(self)
        self.import_image = c.SHIP_COAST
        self.image = self.import_image
        self.rect = self.image.get_rect()
        self.spawn_point = spawn_point
        self.rect.x, self.rect.y = self.spawn_point
        self.x, self.y = self.spawn_point
        # Defines object gravity and max speed.
        self.max_speed = c.MAXSPEED
        # Rect size is equal to imported image size.
        self.rect.w, self.rect.h = 40, 40
        self.bullet_list = pygame.sprite.Group()
        self.fuelgauge = Gauge(self)


    # Key press input functions for ship movement
    def tilt_clockwise(self):
        self.live = 1
        self.tilt = c.TILTRATE
    def tilt_counterclockwise(self):
        self.live = 1
        self.tilt = -c.TILTRATE
    def tilt_stop(self):
        self.tilt = 0
    def accelerate(self):
        self.live = 1
        self.consume = c.CONSUME
        self.acc_t = c.ACCELERATION
        if self.fuel != 0:
            self.import_image = c.SHIP_ACC
    def acceleration_stop(self):
        self.consume = 0
        self.acc_t = 0
        self.import_image = c.SHIP_COAST
    def fire(self):
        self.live = 1
        if len(self.bullet_list) < 4:
            bullet = Bullet(self.orientation, self.rect.center)
            self.bullet_list.add(bullet)

    def reset(self):
        """Used by Game class to set ship in initial state."""
        if self.live:
            self.__init__(self.spawn_point)



    def update(self):

        self.rotate()
        self.move()
        self.bullet_list.update()


class Bullet(c.SPRITE, Movement):
    '''Bullet class. Inherits from Movement.'''
    def __init__(self, orientation, center):
        c.SPRITE.__init__(self)
        Movement.__init__(self)
        self.import_image = c.BULLET
        self.image = self.import_image
        self.orientation = orientation
        self.rect = self.image.get_rect()

        # Bullet x and y speed vectors are calculated based on parrent
        # ship orientation and total speed vector magnitude.
        self.speed_t = 20
        self.speed_x = self.speed_t * math.cos(math.radians(self.orientation))
        self.speed_y = -1 * self.speed_t * math.sin(math.radians(self.orientation))
        self.gravity = c.GRAVITY
        self.max_speed = 20
        self.rect.x, self.rect.y = center
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        self.move()
