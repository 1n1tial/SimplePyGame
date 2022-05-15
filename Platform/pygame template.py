# pygame template - skeleton for a new pygame project
import pygame
import random
from settings import *

# initialize game and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

# game loop
running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill(black)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
