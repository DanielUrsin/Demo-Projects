import random
import math
import time
import pygame
from pygame.sprite import spritecollideany

from gamefiles import config as c
from gamefiles.moving_classes import Movement, Ship, Bullet
from gamefiles.still_classes import Barrel, Frame, Gauge, Score

# Initializes Pygame, but kills the "mixer" module.
# "Mixer" module is buggy and clogs the processor.
pygame.init()
pygame.mixer.quit()


class Game:
    '''Main game running class. Holds sprite lists and defines
       important game functions/methods.'''

    def __init__(self):
        # Defining sprite groups. Greatly siplifies game runtime.
        self.ship_list = pygame.sprite.Group()
        self.barrel_list = pygame.sprite.Group()
        self.still_objects_list = pygame.sprite.Group()
        self.dynamic_objects_list = pygame.sprite.Group()

        # Defining P1 objects
        self.ship1 = Ship(c.LEFT_SPAWN)
        self.P1_score = Score('Player1', (30, c.SCREEN_Y - 75))
        self.ship_list.add(self.ship1)
        self.dynamic_objects_list.add(self.P1_score)
        self.dynamic_objects_list.add(self.ship1.fuelgauge)

        # Defining P2 objects
        self.ship2 = Ship(c.RIGHT_SPAWN)
        self.P2_score = Score('Player2', (c.SCREEN_X-200, c.SCREEN_Y - 75))
        self.ship_list.add(self.ship2)
        self.dynamic_objects_list.add(self.P2_score)
        self.dynamic_objects_list.add(self.ship2.fuelgauge)

        # Defining other ingame objects
        self.barrel_list.add(Barrel())
        self.barrel_list.add(Barrel())
        self.still_objects_list.add(Frame(c.FRAME_HORIZONTAL, (0, 0)))
        self.still_objects_list.add(Frame(c.FRAME_HORIZONTAL, (0, c.SCREEN_Y - 10)))
        self.still_objects_list.add(Frame(c.FRAME_HORIZONTAL, (0, c.SCREEN_Y - 110)))
        self.still_objects_list.add(Frame(c.FRAME_VERTICAL, (0, 0)))
        self.still_objects_list.add(Frame(c.FRAME_VERTICAL, (c.SCREEN_X - 10, 0)))
        self.still_objects_list.add(Frame(c.OBSTACLE, (c.SCREEN_X * 1/4, c.SCREEN_Y * 1/4)))
        self.still_objects_list.add(Frame(c.OBSTACLE, (c.SCREEN_X * 3/4, c.SCREEN_Y * 1/4)))


    def events(self):
        '''Event loop function. Handles all key-presses and the quit event.'''
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                # Ship 1 movement
                if event.key == pygame.K_w:
                    self.ship1.accelerate()
                if event.key == pygame.K_a:
                    self.ship1.tilt_clockwise()
                if event.key == pygame.K_d:
                    self.ship1.tilt_counterclockwise()
                if event.key == pygame.K_SPACE:
                    self.ship1.fire()
                # Ship 2 movement
                if event.key == pygame.K_UP:
                    self.ship2.accelerate()
                if event.key == pygame.K_LEFT:
                    self.ship2.tilt_clockwise()
                if event.key == pygame.K_RIGHT:
                    self.ship2.tilt_counterclockwise()
                if event.key == pygame.K_RCTRL:
                    self.ship2.fire()
            if event.type == pygame.KEYUP:
                # Stop ship movement on key up
                if event.key == pygame.K_w:
                    self.ship1.acceleration_stop()
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.ship1.tilt_stop()
                if event.key == pygame.K_UP:
                    self.ship2.acceleration_stop()
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.ship2.tilt_stop()


    def collide(self):
        '''Method in game class for handling in-game object collisions.'''

        # Removes bullets when they make contact with still objects
        pygame.sprite.groupcollide(self.still_objects_list, self.ship1.bullet_list, False, True)
        pygame.sprite.groupcollide(self.still_objects_list, self.ship2.bullet_list, False, True)

        # Respawns barrels if they are spawned inside other objects
        for object in self.barrel_list:
            overlap = pygame.sprite.spritecollideany(object, self.still_objects_list)
            if overlap != None:
                object.kill()
                self.barrel_list.add(Barrel())

        # P1 and P2 collision
        if pygame.sprite.collide_rect(self.ship1, self.ship2):
            if self.ship1.live:
                self.P1_score.value -= 5
                self.ship1.reset()
            if self.ship2.live:
                self.P2_score.value -= 5
                self.ship2.reset()

        # P1 fuel barrel collision
        f_coll = spritecollideany(self.ship1, self.barrel_list)
        if f_coll != None:
            f_coll.kill()
            self.barrel_list.add(Barrel())
            self.P1_score.value += 5
            self.ship1.fuel += 300
        # P1 envionment collision
        e_coll = spritecollideany(self.ship1, self.still_objects_list)
        if e_coll != None and self.ship1.live:
            self.ship1.reset()
            self.P1_score.value -= 50
        # P1 shot down by P2
        b_coll = spritecollideany(self.ship1, self.ship2.bullet_list)
        if b_coll != None and self.ship1.live:
            self.ship1.reset()
            self.P2_score.value += 100 * self.ship1.multiplier

        # P2 fuel barrel collision
        f_coll = spritecollideany(self.ship2, self.barrel_list)
        if f_coll != None:
            f_coll.kill()
            self.barrel_list.add(Barrel())
            self.P2_score.value += 5
            self.ship2.fuel += 300
        # P2 envionment collision
        e_coll = spritecollideany(self.ship2, self.still_objects_list)
        if e_coll != None and self.ship2.live:
            self.ship2.reset()
            self.P2_score.value -= 50
        # P2 shot down by P1
        b_coll = spritecollideany(self.ship2, self.ship1.bullet_list)
        if b_coll != None and self.ship2.live:
            self.ship2.reset()
            self.P2_score.value += 100 * self.ship1.multiplier


    def draw(self):
        '''Drawing all on-screen objects.'''
        self.still_objects_list.draw(c.SCREEN)
        self.ship_list.draw(c.SCREEN)
        self.ship1.bullet_list.draw(c.SCREEN)
        self.ship2.bullet_list.draw(c.SCREEN)
        self.barrel_list.draw(c.SCREEN)
        self.dynamic_objects_list.draw(c.SCREEN)


    def update(self):
        '''Updates all moving on-screen objects.'''
        self.ship_list.update()
        self.dynamic_objects_list.update()


    def run(self):
        '''Game loop method. Calls all game functions,
           manages drawing of objects to screen and
           manages display updates.'''

        time1 = time.time()
        while True:
            c.SCREEN.fill(c.BLACK)
            self.update()
            self.events()
            self.collide()
            self.draw()

            # Forcing fixed frametime for smooth gameplay.
            time2 = time.time()
            waiting = round(1000.0/c.REFRESH - (time2 - time1)*1000)
            time1 = time2

            pygame.display.update()
            pygame.time.wait(waiting)
