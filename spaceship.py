#!/usr/bin/env python

import sys
import os
from time import sleep
import random
import pygame
from pygame.locals import *

WIDTH = 700
HEIGHT = 480
CENTER = (WIDTH/2, HEIGHT/2)

FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

class GameError(Exception): pass

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

    def play(self):
        self.quit = 0
        while not self.quit:
            self._play()

    def _play(self):
        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.rocks = []
        self.num_hits = 0

        num_rocks = 0
        start_ticks = pygame.time.get_ticks()
        new_rock_interval = 3000

        self.game_over = 0
        while not self.game_over:
            self.clock.tick(FPS)
            ticks = pygame.time.get_ticks()

            if ticks-start_ticks >= (num_rocks+1) * new_rock_interval:
                num_rocks += 1
                print('ticks %s Rock %s' % (ticks, num_rocks))
                rock_name = 'rock_%s' % num_rocks
                self.rocks.append(Rock(rock_name, self))
                self.all_sprites.add(self.rocks[-1])
                self.all_rocks.add(self.rocks[-1])
                new_rock_interval -= 20

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = 1
                    self.quit = 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print('Player Quit')
                        self.game_over = 1
                        self.quit = 1
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

            # Update
            self.all_sprites.update()

            # Check collisions
            self.checkCollisions()

            # Draw / render
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            if ticks-start_ticks <= 3000:
                self.drawText('Get Ready', 22, 'center')
                self.drawText('Q - to Quit', 16, 'below_center')
            self.drawText(str(self.num_hits), 24, 'topleft')

            # *after* drawing everything, flip the display
            pygame.display.flip()

        # remove all sprites
        for s in self.all_sprites:
            print('killing sprite: %s' % s)
            s.kill()

        self.game_over = 0

    def checkCollisions(self):
        for r in self.all_rocks:
            # rock his player?
            if pygame.sprite.collide_rect_ratio(0.75)(self.player, r):
                self.player.destroy()
                self.drawText('Game Over', 32, 'center')
                sleep(2)
                self.game_over = 1

            # phaser hits rock?
            for p in self.all_phasers:
                if pygame.sprite.collide_rect_ratio(0.75)(r, p):
                    r.destroy()
                    self.num_hits += 1

    def drawText(self, raw_text, font_size, pos): #center=None, topleft=None):
        font = pygame.font.SysFont("comicsansms", font_size)
        text = font.render(raw_text, True, WHITE)
        if pos == 'center':
            rect = text.get_rect(center=CENTER)
        elif pos == 'below_center':
            rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+30))
        elif pos == 'topleft':
            rect = text.get_rect(topleft=(20, 10))
        else:
            raise GameError('drawText: Unrecognized position: %s' % pos)
        self.screen.blit(text, rect)
        pygame.display.flip()

class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)

        img_file = os.path.join(game.img_folder, 'spaceship.png')
        player_img = pygame.image.load(img_file).convert()

        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (int(WIDTH/5), HEIGHT/2)
        self.x = 0
        self.y = 0

    def __repr__(self):
        return 'player'

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

    def __init__(self, name, game):
        pygame.sprite.Sprite.__init__(self)
        self.name = name

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

    def __repr__(self):
        return self.name

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
