from initial import *
import pygame
import random
from os import path


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = player_layer
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.img = pygame.image.load(path.join(self.game.img_dir, "playerShip1_orange(2).png")).convert()
        self.img.set_colorkey(black)
        self.lives_img = pygame.transform.scale(self.img, (25, 19))
        self.lives_img.set_colorkey(black)
        self.image = pygame.transform.scale(self.img, (50, 38))
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
            bullet = Bullet(self.game, self.rect.centerx, self.rect.top)
            self.game.all_sprites.add(bullet)
            self.game.bullets.add(bullet)
            self.game.shoot_sound.play()

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
    def __init__(self, game, x, y):
        self._layer = meteor_layer
        self.groups = game.all_sprites, game.meteors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.meteor_images = {"large": [], "med": [], "small": []}
        self.meteor_list_large = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
                                  'meteorBrown_big4.png']
        self.meteor_list_med = ['meteorBrown_med1.png', 'meteorBrown_med3.png']
        self.meteor_list_small = ['meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png',
                                  'meteorBrown_tiny2.png']

        for img in self.meteor_list_large:
            self.meteor_images["large"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_med:
            self.meteor_images["med"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_small:
            self.meteor_images["small"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())

        self.image_orig = random.choice(self.meteor_images[random.choice(["large", "med", "small"])])
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


class LargeMeteor(Meteor):
    def __init__(self, game, x, y):
        self._layer = meteor_layer
        self.groups = game.all_sprites, game.meteors, game.meteors_large
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.meteor_images = {"large": [], "med": [], "small": []}
        self.meteor_list_large = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
                                  'meteorBrown_big4.png']
        self.meteor_list_med = ['meteorBrown_med1.png', 'meteorBrown_med3.png']
        self.meteor_list_small = ['meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png',
                                  'meteorBrown_tiny2.png']

        for img in self.meteor_list_large:
            self.meteor_images["large"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_med:
            self.meteor_images["med"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_small:
            self.meteor_images["small"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        self.image_orig = random.choice(self.meteor_images["large"])
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
    def __init__(self, game, x, y):
        self._layer = meteor_layer
        self.groups = game.all_sprites, game.meteors, game.meteors_med
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.meteor_images = {"large": [], "med": [], "small": []}
        self.meteor_list_large = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
                                  'meteorBrown_big4.png']
        self.meteor_list_med = ['meteorBrown_med1.png', 'meteorBrown_med3.png']
        self.meteor_list_small = ['meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png',
                                  'meteorBrown_tiny2.png']

        for img in self.meteor_list_large:
            self.meteor_images["large"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_med:
            self.meteor_images["med"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_small:
            self.meteor_images["small"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        self.image_orig = random.choice(self.meteor_images["med"])
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
    def __init__(self, game, x, y):
        self._layer = meteor_layer
        self.groups = game.all_sprites, game.meteors, game.meteors_small
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.meteor_images = {"large": [], "med": [], "small": []}
        self.meteor_list_large = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
                                  'meteorBrown_big4.png']
        self.meteor_list_med = ['meteorBrown_med1.png', 'meteorBrown_med3.png']
        self.meteor_list_small = ['meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png',
                                  'meteorBrown_tiny2.png']

        for img in self.meteor_list_large:
            self.meteor_images["large"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_med:
            self.meteor_images["med"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_small:
            self.meteor_images["small"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        self.image_orig = random.choice(self.meteor_images["small"])
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


class MedFakeMeteor(Meteor):
    def __init__(self, game, x, y):
        self._layer = meteor_layer
        self.groups = game.all_sprites, game.meteors, game.meteors_fake_med
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.meteor_images = {"large": [], "med": [], "small": []}
        self.meteor_list_large = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
                                  'meteorBrown_big4.png']
        self.meteor_list_med = ['meteorBrown_med1.png', 'meteorBrown_med3.png']
        self.meteor_list_small = ['meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png',
                                  'meteorBrown_tiny2.png']

        for img in self.meteor_list_large:
            self.meteor_images["large"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_med:
            self.meteor_images["med"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_small:
            self.meteor_images["small"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        self.image_orig = random.choice(self.meteor_images["med"])
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

    def update(self):
        self.rotate()
        self.rect.x += self.velx
        self.rect.y += self.vely
        if self.rect.top > screen_height + 5 or self.rect.right < -5 \
                or self.rect.left > screen_width + 5:
            self.kill()


class SmallFakeMeteor(Meteor):
    def __init__(self, game, x, y):
        self._layer = meteor_layer
        self.groups = game.all_sprites, game.meteors, game.meteors_fake_small
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.meteor_images = {"large": [], "med": [], "small": []}
        self.meteor_list_large = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
                                  'meteorBrown_big4.png']
        self.meteor_list_med = ['meteorBrown_med1.png', 'meteorBrown_med3.png']
        self.meteor_list_small = ['meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png',
                                  'meteorBrown_tiny2.png']

        for img in self.meteor_list_large:
            self.meteor_images["large"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_med:
            self.meteor_images["med"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        for img in self.meteor_list_small:
            self.meteor_images["small"].append(pygame.image.load(path.join(self.game.img_dir, img)).convert())
        self.image_orig = random.choice(self.meteor_images["small"])
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

    def update(self):
        self.rotate()
        self.rect.x += self.velx
        self.rect.y += self.vely
        if self.rect.top > screen_height + 5 or self.rect.right < -5 \
                or self.rect.left > screen_width + 5:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = enemy_layer
        self.groups = game.all_sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.img = pygame.image.load(path.join(self.game.img_dir, "playerShip1_orange(2).png")).convert()
        self.img.set_colorkey(black)
        self.lives_img = pygame.transform.scale(self.img, (25, 19))
        self.lives_img.set_colorkey(black)
        self.image = pygame.transform.scale(self.img, (50, 38))
        self.rect = self.image.get_rect()
        self.radius = 21
        # pygame.draw.circle(self.image, (255, 255, 25, 0), self.rect.center, self.radius)
        self.rect.center = x, y
        self.velx = enemy_vel

    def update(self):
        self.rect.x += self.velx




class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = bullet_layer
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.bullet_img = pygame.image.load(path.join(self.game.img_dir, "laserRed16(2).png")).convert()
        self.image = pygame.transform.scale(self.bullet_img, (8, 40))
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
    def __init__(self, game, center):
        self._layer = pow_layer
        self.groups = game.all_sprites, game.powerups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = random.choice(["shield", "gun"])
        self.powup_images = {"shield": pygame.image.load(path.join(self.game.img_dir, "shield_gold_powup.png")).convert(),
                             "gun": pygame.image.load(path.join(self.game.img_dir, "bolt_gold_powup.png")).convert()}
        self.image = self.powup_images[self.type]
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
    def __init__(self, game, center, size):
        self._layer = explo_layer
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = size
        self.explosion_anim = {"large": [], "small": [], "player": []}
        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join(self.game.img_dir, filename)).convert()
            img.set_colorkey(black)
            img_large = pygame.transform.scale(img, (75, 75))
            self.explosion_anim["large"].append(img_large)
            img_small = pygame.transform.scale(img, (32, 32))
            self.explosion_anim["small"].append(img_small)
            filename = "sonicExplosion0{}.png".format(i)
            img_player = pygame.image.load(path.join(self.game.img_dir, filename)).convert()
            img_player.set_colorkey(black)
            self.explosion_anim["player"].append(img_player)
        self.image = self.explosion_anim[self.size][0]
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
            if self.frame == len(self.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

