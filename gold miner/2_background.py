import pygame
import sys
import os

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Gold Miner")

clock = pygame.time.Clock()

# load images
current_path = os.path.dirname(__file__)
bg_img = pygame.image.load(os.path.join(current_path, "background.png"))


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_img, (0, 0))
    pygame.display.update()


pygame.quit()
sys.exit()

