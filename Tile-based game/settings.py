import pygame as pg
vec = pg.math.Vector2

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
darkgrey = (40, 40, 40)
lightgrey = (100, 100, 100)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
brown = (106, 55, 5)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Tilemap Demo"
bgcolor = brown

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = "manBlue_gun.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# wall settings
WALL_IMG = "tileGreen_39.png"

# mob settings
ZOMBIE_IMG = "zombie1_hold.png"
ZOMBIE_SPEEDS = [75, 100, 150, 250]
ZOMBIE_HIT_RECT = pg.Rect(0, 0, 35, 35)
ZOMBIE_HEALTH = 100
ZOMBIE_DAMAGE = 10
ZOMBIE_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

# weapon settings
BULLET_IMG = "bullet.png"
WEAPONS = {}
WEAPONS["pistol"] = {"speed": 500,
                     'lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'knockback': 100,
                     'size': 'lg',
                     'count': 1}
WEAPONS["shotgun"] = {"speed": 400,
                      'lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'knockback': 20,
                      'size': 'sm',
                      'count': 12}
# BULLET_SPEED = 600
# BULLET_LIFETIME = 1000
# BULLET_RATE = 150
# KICKBACK = 200
# GUN_SPREAD = 5  # RNG
# BULLET_DAMAGE = 10
# BULLET_KNOCKBACK = 100

# visual effects
MUZZLE_FLASHES = ["whitePuff15.png", "whitePuff16.png", "whitePuff17.png", "whitePuff18.png"]
FLASH_DUR = 40
ZOMBIE_SPLATS = ["splat green.png", "splat red.png"]
DAMAGE_ALPHA = [i for i in range(255, 0, -5)]


# sound effects
PLAYER_HIT_SOUNDS = ["8.wav", "9.wav", "10.wav", "11.wav"]
ZOMBIE_MOAN_SOUNDS = ["brains2.wav", "brains3.wav", "zombie-roar-1.wav", "zombie-roar-2.wav", "zombie-roar-3.wav",
                      "zombie-roar-4.wav", "zombie-roar-5.wav", "zombie-roar-6.wav", "zombie-roar-7.wav"]
ZOMBIE_HIT_SOUNDS = ["splat-15.wav"]
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav']}
EFFECTS_SOUNDS = {"level start": "level_start.wav",
                  "health_up": "health_pack.wav",
                  "shotgun_pickup": "gun_pickup.wav"}

# music
BG_MUSIC = "espionage.ogg"

# layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# items
ITEM_IMAGES = {"health item": "health_pack.png",
               "shotgun item": "obj_shotgun.png"}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 20
BOB_SPEED = 0.6
