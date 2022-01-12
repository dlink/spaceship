import pygame
from pygame.locals import *
import sys
import os

WIDTH = 500
HEIGHT = 340 #480 
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
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.x = 0
        self.y = 0

    def update(self):
        self.rect.x += (5 + self.x)
        self.rect.y += self.y

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
        self.playSound()

    def playSound(self):
        phaser_sound = pygame.mixer.Sound(sound_file)
        channel = phaser_sound.play()

    def update(self):
        self.rect.x += 10
        if self.rect.left > WIDTH:
            self.kill()
    

# Game init
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
img_file = os.path.join(img_folder, 'spaceship.png')
player_img = pygame.image.load(img_file).convert()
sound_folder = os.path.join(game_folder, 'sound')
sound_file = os.path.join(sound_folder, 'phaser.ogg')

# sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                phaser = Phaser(player)
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

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()
