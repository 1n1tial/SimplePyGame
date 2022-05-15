# game options/settings
TITLE = "Jumpy!"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# player properties
player_acc = 0.5
player_friction = -0.12
player_grav = 0.8
player_jump = 20

# game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 5000
CLOUD_LAYER = 0
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2

# starting platforms
platform_list = [(0, HEIGHT - 40),
                 (WIDTH / 2 - 50, HEIGHT * 0.75),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
light_blue = (0, 160, 150)
bgcolor = light_blue
