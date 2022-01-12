#!/usr/bin/env python

import sys
import os
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

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        img_file = os.path.join(img_folder, 'spaceship.png')
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


class Rock(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        size = random.randint(20,70)
        self.image = pygame.Surface([size, size])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        x = random.randint(WIDTH-WIDTH/8, WIDTH)
        y = random.randint(0, HEIGHT)
        self.rect.center = (x, y)
        self.speed_x = random.randint(3,7)
        self.speed_y = random.randint(-1,1)

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


class Phaser(pygame.sprite.Sprite):

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30, 1])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        x = player.rect.center[0]+15
        y = player.rect.center[1]+6
        self.rect.center = (x,y)

        sound_file = os.path.join(sound_folder, 'phaser.ogg')
        self.phaser_sound = pygame.mixer.Sound(sound_file)
        self.playSound()

    def playSound(self):
        channel = self.phaser_sound.play()

    def update(self):
        self.rect.x += 10
        if self.rect.left > WIDTH:
            self.kill()

def checkCollisions():
    for r in all_rocks:
        if pygame.sprite.collide_rect_ratio(0.75)(player, r):
            sys.exit()
        for p in all_phasers:
            if pygame.sprite.collide_rect_ratio(0.75)(r, p):
                r.kill()
# Game init
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
sound_folder = os.path.join(game_folder, 'sound')

# sprites
all_sprites = pygame.sprite.Group()
all_phasers = pygame.sprite.Group()
all_rocks = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

rocks = []
num_rocks = 0
new_rock_interval = 4000

run = True
while run:
    clock.tick(FPS)
    ticks=pygame.time.get_ticks()

    if ticks >= (num_rocks+1)*new_rock_interval:
        print(ticks, type(ticks))
        rocks.append(Rock())
        all_sprites.add(rocks[-1])
        all_rocks.add(rocks[-1])
        num_rocks += 1
        new_rock_interval -= 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                phaser = Phaser(player)
                all_phasers.add(phaser)
                all_sprites.add(phaser)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
         player.y -= 1
    if keys[pygame.K_DOWN]:
        player.y += 1
    if keys[pygame.K_LEFT]:
        player.x -= 1
    if keys[pygame.K_RIGHT]:
        player.x += 1
    if keys[pygame.K_q]:
        print('quit')
        run = False

    # Update
    all_sprites.update()

    # Check collisions
    checkCollisions()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()
