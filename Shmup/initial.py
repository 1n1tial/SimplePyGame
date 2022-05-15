import pygame

# basic variables
screen_width = 600
screen_height = 720
title = 'Shmup!'
fps = 60
font_name = 'arial'
powerup_dur = 3000
shoot_delay1 = 350
shoot_delay2 = 150
powerup_spawn_rate = 0.04
fuel_drainage = 0.3
display_shield_text = False
display_gun_text = False
display_warning = False
display_bar = False

generic_var = 0

# layers
player_layer = 3
meteor_layer = 3
bullet_layer = 3
pow_layer = 2
explo_layer = 1

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)

yg1 = (100, 255, 0)
yg2 = (180, 255, 0)
yg3 = (200, 255, 0)

ry1 = (255, 200, 0)
ry2 = (255, 170, 0)
ry3 = (255, 90, 0)

# initialize pygame, create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()