#!/usr/bin/env python

import sys
import os
from time import sleep
import random
import pygame
from pygame.locals import *

WIDTH = 700
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

class Game():

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Spaceship")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # set up asset folders
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'img')
        self.sound_folder = os.path.join(self.game_folder, 'sound')

        # sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_phasers = pygame.sprite.Group()
        self.all_rocks = pygame.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.rocks = []
        self.num_rocks = 0
        self.new_rock_interval = 4000

    def play(self):
        run = True
        while run:
            self.clock.tick(FPS)
            ticks = pygame.time.get_ticks()

            if ticks >= (self.num_rocks+1) * self.new_rock_interval:
                self.num_rocks += 1
                print('ticks %s Rock %s' % (ticks, self.num_rocks))
                self.rocks.append(Rock(self))
                self.all_sprites.add(self.rocks[-1])
                self.all_rocks.add(self.rocks[-1])
                self.new_rock_interval -= 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        phaser = Phaser(self)
                        self.all_sprites.add(phaser)
                        self.all_phasers.add(phaser)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                 self.player.y -= 1
            if keys[pygame.K_DOWN]:
                self.player.y += 1
            if keys[pygame.K_LEFT]:
                self.player.x -= 1
            if keys[pygame.K_RIGHT]:
                self.player.x += 1
            #if keys[pygame.K_q]:
            #    self.print('quit')
            #    run = False

            # Update
            self.all_sprites.update()

            # Check collisions
            self.checkCollisions()

            # Draw / render
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            # *after* drawing everything, flip the display
            pygame.display.flip()

    def checkCollisions(self):
        for r in self.all_rocks:
            if pygame.sprite.collide_rect_ratio(0.75)(self.player, r):
                self.player.destroy()
                sleep(2)
                sys.exit()
            for p in self.all_phasers:
                if pygame.sprite.collide_rect_ratio(0.75)(r, p):
                    r.destroy()

class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)

        img_file = os.path.join(game.img_folder, 'spaceship.png')
        player_img = pygame.image.load(img_file).convert()

        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/4, HEIGHT/2)
        self.x = 0
        self.y = 0

    def update(self):
        self.rect.x += (1 + self.x)
        self.rect.y += self.y

        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH

        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

    def destroy(self):
        print('player destroyed')
        sound_file = os.path.join(game.sound_folder, 'explosion.ogg')
        destroyed_sound = pygame.mixer.Sound(sound_file)
        channel = destroyed_sound.play()

class Rock(pygame.sprite.Sprite):

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)

        #img_file = os.path.join(self.img_folder, 'rock.png')
        #rock_img = pygame.image.load(img_file).convert()
        #self.image = rock_img

        size = random.randint(20,70)
        self.image = pygame.Surface([size, size])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        x = random.randint(int(WIDTH-WIDTH/8), WIDTH)
        y = random.randint(0, HEIGHT)
        self.rect.center = (x, y)
        self.speed_x = random.randint(3,7)
        self.speed_y = random.randint(-2,2)

    def update(self):
        self.rect.x -= self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left > WIDTH:
            self.kill()

        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH

        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

    def destroy(self):
        sound_file = os.path.join(game.sound_folder, 'destroyed.ogg')
        destroyed_sound = pygame.mixer.Sound(sound_file)
        channel = destroyed_sound.play()
        self.kill()

class Phaser(pygame.sprite.Sprite):

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30, 1])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        x = game.player.rect.center[0]+15
        y = game.player.rect.center[1]+6
        self.rect.center = (x,y)

        sound_file = os.path.join(game.sound_folder, 'phaser.ogg')
        self.phaser_sound = pygame.mixer.Sound(sound_file)
        self.playSound()

    def playSound(self):
        channel = self.phaser_sound.play()

    def update(self):
        self.rect.x += 10
        if self.rect.left > WIDTH:
            self.kill()

if __name__ == '__main__':
    game = Game()
    game.play()

