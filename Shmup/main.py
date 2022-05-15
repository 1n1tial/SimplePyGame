# Art from Kenney.nl
# Call the Shots(bgm) by Slynk

import random
import sys

from pygame.constants import *

from initial import *
from particles import *

from os import path

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")

font_name = pygame.font.match_font("arial")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_start_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, screen_width // 2, screen_height // 4)
    draw_text(screen, "Arrow Keys Move, Hold Space to Fire", 22,
              screen_width // 2, screen_height // 2)
    draw_text(screen, "Watch your fuel gauge", 22,
              screen_width // 2, screen_height // 2 + 35)
    draw_text(screen, "Press a key to begin", 25,
              screen_width // 2, screen_height // 1.5)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "GAME OVER", 64, screen_width // 2, screen_height // 4)
    draw_text(screen, f"Your score was {score}", 22,
              screen_width // 2, screen_height // 2)
    draw_text(screen, "Press a key to try again", 25,
              screen_width // 2, screen_height // 1.5)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 21
        # pygame.draw.circle(self.image, (255, 255, 25, 0), self.rect.center, self.radius)
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 45
        self.velx = 0
        self.shield = 100
        self.fuel = 100
        self.shoot_delay = shoot_delay1
        self.last_shot = pygame.time.get_ticks()
        self.lives = 1
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.gun_power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.gun_power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_dur:
            self.gun_power = 1
            self.power_time = pygame.time.get_ticks()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.centerx = screen_width // 2
            self.rect.bottom = screen_height - 15

        self.velx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.velx = -5
        if keystate[pygame.K_RIGHT]:
            self.velx = 5

        self.rect.x += self.velx

        if keystate[pygame.K_SPACE]:
            self.shoot()

        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup_gun(self):
        self.gun_power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        # autofire
        if self.gun_power == 1:
            self.shoot_delay = shoot_delay1
        elif self.gun_power >= 2:
            self.shoot_delay = shoot_delay2
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (screen_width // 2, -2000)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0

    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, red, outline_rect)
    pygame.draw.rect(surf, green, fill_rect)


def draw_fuel_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    if pct > 100:
        pct = 100

    bar_length = 20
    bar_height = 400
    fill = (pct / 100) * bar_height
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, bar_length, fill)
    pygame.draw.rect(surf, white, outline_rect, 2)
    if pct > 55:
        pygame.draw.rect(surf, green, fill_rect)
    if 55 >= pct > 50:
        pygame.draw.rect(surf, yg1, fill_rect)
    if 50 >= pct > 45:
        pygame.draw.rect(surf, yg2, fill_rect)
    if 45 >= pct > 40:
        pygame.draw.rect(surf, yg3, fill_rect)
    if 40 >= pct > 20:
        pygame.draw.rect(surf, yellow, fill_rect)
    if 20 >= pct > 17:
        pygame.draw.rect(surf, ry1, fill_rect)
    if 17 >= pct > 14:
        pygame.draw.rect(surf, ry2, fill_rect)
    if 14 >= pct > 10:
        pygame.draw.rect(surf, ry3, fill_rect)
    if 10 >= pct > 0:
        pygame.draw.rect(surf, red, fill_rect)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_gun_powerup_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0

    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, white, outline_rect, 2)
    pygame.draw.rect(surf, yellow, fill_rect)


class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images[random.choice(["large", "med", "small"])])
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = x
        self.rect.y = y
        # self.rect.x = random.randrange(0, screen_width - self.rect.width)
        # self.rect.y = random.randrange(-140, -80)
        self.velx = random.randrange(-3, 3)
        self.vely = random.randrange(1, 8)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.velx
        self.rect.y += self.vely
        if self.rect.top > screen_height + 5 or self.rect.right < -5 \
                or self.rect.left > screen_width + 5:
            self.rect.x = random.randrange(0, screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.vely = random.randrange(1, 8)
        if game_over:
            self.kill()


class LargeMeteor(Meteor):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images["large"])
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = x
        self.rect.y = y
        self.velx = random.randrange(-3, 3)
        self.vely = random.randrange(1, 4)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


class MedMeteor(Meteor):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images["med"])
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = x
        self.rect.y = y
        self.velx = random.randrange(-3, 3)
        self.vely = random.randrange(3, 7)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


class SmallMeteor(Meteor):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images["small"])
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = x
        self.rect.y = y
        self.velx = random.randrange(-3, 3)
        self.vely = random.randrange(5, 9)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


class MedFakeMeteor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images["med"])
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = x
        self.rect.centery = y
        self.velx = random.randrange(-6, 6)
        self.vely = random.randrange(1, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.velx
        self.rect.y += self.vely
        if self.rect.top > screen_height + 5 or self.rect.right < -5 \
                or self.rect.left > screen_width + 5 or game_over:
            self.kill()


class SmallFakeMeteor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images["small"])
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = x
        self.rect.centery = y
        self.velx = random.randrange(-8, 8)
        self.vely = random.randrange(2, 4)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.velx
        self.rect.y += self.vely
        if self.rect.top > screen_height + 5 or self.rect.right < -5 \
                or self.rect.left > screen_width + 5 or game_over:
            self.kill()


def spawn_meteor_top():
    m1 = LargeMeteor(random.randrange(0, screen_width), random.randrange(-140, -80))
    m2 = MedMeteor(random.randrange(0, screen_width), random.randrange(-140, -80))
    m3 = SmallMeteor(random.randrange(0, screen_width), random.randrange(-140, -80))
    m = random.choice([m1, m2, m3])
    all_sprites.add(m)
    meteors.add(m)
    if m == m1:
        meteors_large.add(m)
    elif m == m2:
        meteors_med.add(m)
    else:
        meteors_small.add(m)


def spawn_med_mob(x, y):
    m = MedMeteor(x, y)
    all_sprites.add(m)
    meteors.add(m)
    meteors_med.add(m)


def spawn_small_mob(x, y):
    m = SmallMeteor(x, y)
    all_sprites.add(m)
    meteors.add(m)
    meteors_small.add(m)


def spawn_med_fake_mob(x, y):
    m = MedFakeMeteor(x, y)
    all_sprites.add(m)
    meteors.add(m)
    meteors_fake_med.add(m)


def spawn_small_fake_mob(x, y):
    m = SmallFakeMeteor(x, y)
    all_sprites.add(m)
    meteors.add(m)
    meteors_fake_small.add(m)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (8, 40))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vely = -15

    def update(self):
        self.rect.y += self.vely

        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = powup_images[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.vely = 5

    def update(self):
        self.rect.y += self.vely

        # kill it if it moves off the bottom of the screen
        if self.rect.top > screen_height + 10:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 45

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Load all game graphics

# background
background = pygame.image.load(path.join(img_dir, "starfield(2).png")).convert()
# background = pygame.transform.scale(background, (screen_width, screen_height))
background_rect = background.get_rect()

# player
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange(2).png")).convert()
player_lives_img = pygame.transform.scale(player_img, (25, 19))
player_lives_img.set_colorkey(black)

# bullet
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()

# meteor
meteor_images = {"large": [], "med": [], "small": []}
meteor_list_large = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png', 'meteorBrown_big4.png']
meteor_list_med = ['meteorBrown_med1.png', 'meteorBrown_med3.png']
meteor_list_small = ['meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png',
                     'meteorBrown_tiny2.png']

for img in meteor_list_large:
    meteor_images["large"].append(pygame.image.load(path.join(img_dir, img)).convert())
for img in meteor_list_med:
    meteor_images["med"].append(pygame.image.load(path.join(img_dir, img)).convert())
for img in meteor_list_small:
    meteor_images["small"].append(pygame.image.load(path.join(img_dir, img)).convert())

# explosion
explosion_anim = {"large": [], "small": [], "player": []}
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_large = pygame.transform.scale(img, (75, 75))
    explosion_anim["large"].append(img_large)
    img_small = pygame.transform.scale(img, (32, 32))
    explosion_anim["small"].append(img_small)
    filename = "sonicExplosion0{}.png".format(i)
    img_player = pygame.image.load(path.join(img_dir, filename)).convert()
    img_player.set_colorkey(black)
    explosion_anim["player"].append(img_player)

# powerups
powup_images = {"shield": pygame.image.load(path.join(img_dir, "shield_gold_powup.png")).convert(),
                "gun": pygame.image.load(path.join(img_dir, "bolt_gold_powup.png")).convert()}

# load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "laser_sound.wav"))
expl_sounds = []
for snd in ['explo_sound1.wav', 'explo_sound2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
shield_dmg_sound = pygame.mixer.Sound(path.join(snd_dir, "Shield Damage.wav"))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, "ship_explode.ogg"))
powup_sound = pygame.mixer.Sound(path.join(snd_dir, "Power-up.wav"))
pygame.mixer.music.load(path.join(snd_dir, "Call The Shots - Slynk.mp3"))
pygame.mixer.music.set_volume(0.1)

all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()
meteors_large = pygame.sprite.Group()
meteors_med = pygame.sprite.Group()
meteors_small = pygame.sprite.Group()
meteors_fake_med = pygame.sprite.Group()
meteors_fake_small = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    spawn_meteor_top()
score = 0
player_particles = []
# last_spawn = pygame.time.get_ticks()

show_start_screen()
pygame.mixer.music.play(loops=-1)

# main game loop
game_over = False
running = True
while running:
    if game_over:
        for sprite in all_sprites:
            sprite.kill()
        pygame.mixer.music.stop()
        show_go_screen()
        pygame.mixer.music.play(-1)
        game_over = False


        # restart
        all_sprites = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            spawn_meteor_top()
        score = 0
        generic_var = 0
        player_particles = []
        display_bar = False

    # keep loop running at a proper speed
    clock.tick(fps)

    # process of inputs as events
    for event in pygame.event.get():

        # closing the game
        if event.type == pygame.QUIT:
            running = False

        # fire bullet (not autofire)
        # elif event.type == pygame.KEYDOWN:
        # if event.key == pygame.K_SPACE:
        # player.shoot()

    # update
    all_sprites.update()

    # check if powerup hit a player
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "shield":
            powup_sound.play()
            player.shield += 20
            if player.shield >= 100:
                player.shield = 100
            display_shield_text = True
            shieldtxt_start_time = pygame.time.get_ticks()

        elif hit.type == "gun":
            powup_sound.play()
            player.powerup_gun()
            display_gun_text = True
            guntxt_start_time = pygame.time.get_ticks()
            display_bar = True
            bar_start_time = pygame.time.get_ticks()

    # check if any mob hit a player
    hits = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
    for hit in hits:
        if player.shield > 0:
            player.shield -= hit.radius * 2
            shield_dmg_sound.play()
            expl = Explosion(hit.rect.center, "small")
            all_sprites.add(expl)
            spawn_meteor_top()

            if player.shield <= 0:
                player.shield = 0
                display_warning = True
                warntxt_start_time = pygame.time.get_ticks()

        elif player.shield == 0:
            death_expl = Explosion(player.rect.center, "player")
            all_sprites.add(death_expl)
            player_die_sound.play()
            player.hide()
            player.lives -= 1
            player.shield = 100


    # check if any bullet hit a mob
    def meteor_hit_action(group):
        global score
        hits = pygame.sprite.groupcollide(group, bullets, True, True)
        for hit in hits:
            score += 5
            player.fuel += 5
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'large')
            all_sprites.add(expl)
            if group == meteors_large:
                spawn_med_mob(hit.rect.centerx, hit.rect.centery)
                spawn_med_fake_mob(hit.rect.centerx, hit.rect.centery)
            elif group == meteors_med:
                spawn_small_mob(hit.rect.centerx, hit.rect.centery)
                spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
            elif group == meteors_fake_med:
                spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
                spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
            elif group == meteors_small:
                spawn_meteor_top()
            elif group == meteors_fake_small:
                pass
            if random.random() > 1 - powerup_spawn_rate:
                pow = PowerUp(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)


    for m in [meteors_large, meteors_med, meteors_fake_med, meteors_small, meteors_fake_small]:
        meteor_hit_action(m)

    # fuel
    player.fuel -= fuel_drainage
    if player.fuel > 100:
        player.fuel = 100
    if player.fuel <= 0 and generic_var == 0:
        death_expl = Explosion(player.rect.center, "player")
        all_sprites.add(death_expl)
        player_die_sound.play()
        player.hide()
        player.lives = 0
        player.shield = 100
        generic_var = 1

    # if the player died, and the explosion finished
    if player.lives == 0 and not death_expl.alive():
        game_over = True

    # fill screen and draw sprites
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {score}", 20, screen_width - 50, 10)
    draw_text(screen, "Shield Durability", 18, 57, 5)
    draw_shield_bar(screen, 8, 30, player.shield)
    draw_fuel_bar(screen, 13, 100, player.fuel)
    # draw_lives(screen, 10, screen_height - 50, player.lives, player_lives_img)

    # draw particles behind player
    for i in range(3):
        player_particles.append([[player.rect.centerx, player.rect.bottom], [random.randint(0, 300) / 100 - 1.5, 3], random.randint(3, 5)])

    for particle in player_particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.12
        particle[1][1] -= 0.1
        # pygame.draw.circle(screen, (0, 0, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2] * 2))

        radius = particle[2] * 3
        screen.blit(circle_surf(radius, (200, 0, 20)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGBA_ADD)

        if particle[2] <= 0 or game_over:
            player_particles.remove(particle)

    # lighting for bullet
    for bullet in bullets:
        bullet_radius = 3
        for i in range(10):
            screen.blit(circle_surf(bullet_radius*i, (20, 20, 20)), (bullet.rect.centerx - bullet_radius*i, bullet.rect.y), special_flags=BLEND_RGBA_ADD)

    powup_images['gun'].set_colorkey(black)
    fuel_rect = powup_images['gun'].get_rect()
    fuel_rect.x = 15
    fuel_rect.y = 63
    screen.blit(powup_images['gun'], fuel_rect)

    if display_shield_text:
        draw_text(screen, "Shield Recovered!", 30, screen_width // 2, screen_height // 3)

        if pygame.time.get_ticks() - shieldtxt_start_time > 500:
            display_shield_text = False

    if display_gun_text:
        draw_text(screen, "Gun Powered Up!", 30, screen_width // 2, screen_height // 3)

        if pygame.time.get_ticks() - guntxt_start_time > 500:
            display_gun_text = False

    if display_warning:
        draw_text(screen, "Warning!\nShield is Down!", 30, screen_width // 2, screen_height // 3)

        if pygame.time.get_ticks() - warntxt_start_time > 500:
            display_warning = False

    if display_bar:
        draw_gun_powerup_bar(screen, 12, 50,
                             (powerup_dur - pygame.time.get_ticks() + bar_start_time) * 100 / powerup_dur)

        if pygame.time.get_ticks() - bar_start_time > powerup_dur:
            display_bar = False

    # display flip (update entirety)
    pygame.display.flip()

    # print(player.lives, generic_var)
    # try:
    #     print(player.lives, death_expl.alive(), generic_var)
    # except NameError:
    #     pass


pygame.quit()
sys.exit()
