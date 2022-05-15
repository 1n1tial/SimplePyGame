import pygame
from pygame.constants import *
import sys
import random
from initial import *
from sprites import *
from particles import circle_surf
from os import path


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


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(font_name)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'img')
        # Load all game graphics

        # background
        self.background = pygame.image.load(path.join(self.img_dir, "starfield(2).png")).convert()
        # background = pygame.transform.scale(background, (screen_width, screen_height))
        self.background_rect = self.background.get_rect()

        self.snd_dir = path.join(self.dir, 'snd')
        # load all game sounds
        self.shoot_sound = pygame.mixer.Sound(path.join(self.snd_dir, "laser_sound.wav"))
        self.expl_sounds = []
        for snd in ['explo_sound1.wav', 'explo_sound2.wav']:
            self.expl_sounds.append(pygame.mixer.Sound(path.join(self.snd_dir, snd)))
        self.shield_dmg_sound = pygame.mixer.Sound(path.join(self.snd_dir, "Shield Damage.wav"))
        self.player_die_sound = pygame.mixer.Sound(path.join(self.snd_dir, "ship_explode.ogg"))
        self.powup_sound = pygame.mixer.Sound(path.join(self.snd_dir, "Power-up.wav"))

    def spawn_meteor_top(self):
        if random.random() < 1/3:
            LargeMeteor(self, random.randrange(0, screen_width), random.randrange(-140, -80))
        elif 1/3 <= random.random() < 2/3:
            MedMeteor(self, random.randrange(0, screen_width), random.randrange(-140, -80))
        else:
            SmallMeteor(self, random.randrange(0, screen_width), random.randrange(-140, -80))

    def spawn_med_mob(self, x, y):
        m = MedMeteor(self, x, y)

    def spawn_small_mob(self, x, y):
        m = SmallMeteor(self, x, y)

    def spawn_med_fake_mob(self, x, y):
        m = MedFakeMeteor(self, x, y)

    def spawn_small_fake_mob(self, x, y):
        m = SmallFakeMeteor(self, x, y)

    def new(self):
        # restart
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.meteors = pygame.sprite.Group()
        self.meteors_large = pygame.sprite.Group()
        self.meteors_med = pygame.sprite.Group()
        self.meteors_small = pygame.sprite.Group()
        self.meteors_fake_med = pygame.sprite.Group()
        self.meteors_fake_small = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player = Player(self)
        for i in range(8):
            self.spawn_meteor_top()
        self.score = 0
        self.generic_var = 0
        self.player_particles = []
        self.display_bar = False
        self.display_shield_text = False
        self.display_gun_text = False
        self.display_warning = False
        self.display_bar = False

        pygame.mixer.music.load(path.join(self.snd_dir, "Call The Shots - Slynk.mp3"))
        pygame.mixer.music.set_volume(0.1)
        self.run()

    def run(self):
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)

    def update(self):
        # update
        self.all_sprites.update()

        # check if powerup hit a player
        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hits:
            if hit.type == "shield":
                self.powup_sound.play()
                self.player.shield += 20
                if self.player.shield >= 100:
                    self.player.shield = 100
                self.display_shield_text = True
                self.shieldtxt_start_time = pygame.time.get_ticks()

            elif hit.type == "gun":
                self.powup_sound.play()
                self.player.powerup_gun()
                self.display_gun_text = True
                self.guntxt_start_time = pygame.time.get_ticks()
                self.display_bar = True
                self.bar_start_time = pygame.time.get_ticks()

        # check if any mob hit a player
        hits = pygame.sprite.spritecollide(self.player, self.meteors, True, pygame.sprite.collide_circle)
        for hit in hits:
            if self.player.shield > 0:
                self.player.shield -= hit.radius * 2
                self.shield_dmg_sound.play()
                expl = Explosion(self, hit.rect.center, "small")
                self.all_sprites.add(expl)
                self.spawn_meteor_top()

                if self.player.shield <= 0:
                    self.player.shield = 0
                    self.display_warning = True
                    self.warntxt_start_time = pygame.time.get_ticks()

            elif self.player.shield == 0:
                self.death_expl = Explosion(self, self.player.rect.center, "player")
                self.all_sprites.add(self.death_expl)
                self.player_die_sound.play()
                self.player.hide()
                self.player.lives -= 1
                self.player.shield = 100

        # check if any bullet hit a mob
        def meteor_hit_action(group):
            hits = pygame.sprite.groupcollide(group, self.bullets, True, True)
            for hit in hits:
                self.score += 5
                self.player.fuel += 5
                random.choice(self.expl_sounds).play()
                expl = Explosion(self, hit.rect.center, 'large')
                self.all_sprites.add(expl)
                if group == self.meteors_large:
                    self.spawn_med_mob(hit.rect.centerx, hit.rect.centery)
                    self.spawn_med_fake_mob(hit.rect.centerx, hit.rect.centery)
                elif group == self.meteors_med:
                    self.spawn_small_mob(hit.rect.centerx, hit.rect.centery)
                    self.spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
                elif group == self.meteors_fake_med:
                    self.spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
                    self.spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
                elif group == self.meteors_small:
                    self.spawn_meteor_top()
                elif group == self.meteors_fake_small:
                    pass
                if random.random() > 1 - powerup_spawn_rate:
                    pow = PowerUp(self, hit.rect.center)
                    self.all_sprites.add(pow)
                    self.powerups.add(pow)

        for m in [self.meteors_large, self.meteors_med, self.meteors_fake_med, self.meteors_small,
                  self.meteors_fake_small]:
            meteor_hit_action(m)

        # fuel
        self.player.fuel -= fuel_drainage
        if self.player.fuel > 100:
            self.player.fuel = 100
        if self.player.fuel <= 0 and self.generic_var == 0:
            death_expl = Explosion(self.player.rect.center, "player")
            self.all_sprites.add(death_expl)
            self.player_die_sound.play()
            self.player.hide()
            self.player.lives = 0
            self.player.shield = 100
            self.generic_var = 1

        # if the player died, and the explosion finished
        if self.player.lives == 0 and not self.death_expl.alive():
            self.playing = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # fill screen and draw sprites
        screen.fill(black)
        screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(screen)
        self.draw_text(f"Score: {self.score}", 20, screen_width - 50, 10)
        self.draw_text("Shield Durability", 18, 57, 5)
        draw_shield_bar(screen, 8, 30, self.player.shield)
        draw_fuel_bar(screen, 13, 100, self.player.fuel)
        # draw_lives(screen, 10, screen_height - 50, player.lives, player_lives_img)

        # draw particles behind player
        for i in range(3):
            self.player_particles.append(
                [[self.player.rect.centerx, self.player.rect.bottom], [random.randint(0, 300) / 100 - 1.5, 3],
                 random.randint(3, 5)])

        for particle in self.player_particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.12
            particle[1][1] -= 0.1
            # pygame.draw.circle(screen, (0, 0, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2] * 2))

            radius = particle[2] * 3
            screen.blit(circle_surf(radius, (0, 200, 20)), (int(particle[0][0] - radius), int(particle[0][1] - radius)),
                        special_flags=BLEND_RGBA_ADD)

            if particle[2] <= 0 or not self.playing:
                self.player_particles.remove(particle)

        # lighting for bullet
        for bullet in self.bullets:
            bullet_radius = 3
            for i in range(7):
                screen.blit(circle_surf(bullet_radius * i, (20, 20, 20)),
                            (bullet.rect.x - bullet_radius * i, bullet.rect.centery - bullet_radius * i + 3 * i + 10),
                            special_flags=BLEND_RGB_ADD)

        # self.powup_images['gun'].set_colorkey(black)
        # fuel_rect = self.powup_images['gun'].get_rect()
        # fuel_rect.x = 15
        # fuel_rect.y = 63
        # screen.blit(self.powup_images['gun'], fuel_rect)

        if self.display_shield_text:
            self.draw_text("Shield Recovered!", 30, screen_width // 2, screen_height // 3)

            if pygame.time.get_ticks() - self.shieldtxt_start_time > 500:
                self.display_shield_text = False

        if self.display_gun_text:
            self.draw_text("Gun Powered Up!", 30, screen_width // 2, screen_height // 3)

            if pygame.time.get_ticks() - self.guntxt_start_time > 500:
                self.display_gun_text = False

        if self.display_warning:
            self.draw_text("Warning!\nShield is Down!", 30, screen_width // 2, screen_height // 3)

            if pygame.time.get_ticks() - self.warntxt_start_time > 500:
                self.display_warning = False

        if self.display_bar:
            draw_gun_powerup_bar(screen, 12, 50,
                                 (powerup_dur - pygame.time.get_ticks() + self.bar_start_time) * 100 / powerup_dur)

            if pygame.time.get_ticks() - self.bar_start_time > powerup_dur:
                self.display_bar = False

        # display flip (update entirety)
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.blit(self.background, self.background_rect)
        self.draw_text("SHMUP!", 64, screen_width // 2, screen_height // 4)
        self.draw_text("Arrow Keys Move, Hold Space to Fire", 22,
                       screen_width // 2, screen_height // 2)
        self.draw_text("Watch your fuel gauge", 22,
                       screen_width // 2, screen_height // 2 + 35)
        self.draw_text("Press a key to begin", 25,
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

    def show_go_screen(self):
        if not self.running:
            return
        screen.blit(self.background, self.background_rect)
        self.draw_text("GAME OVER", 64, screen_width // 2, screen_height // 4)
        self.draw_text(f"Your score was {self.score}", 22,
                       screen_width // 2, screen_height // 2)
        self.draw_text("Press a key to try again", 25,
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

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, x, y, color=white):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


# mainGame = Game()
# mainGame.show_start_screen()
# while mainGame.running:
#     mainGame.new()
#     mainGame.show_go_screen()
#
# pygame.quit()
# sys.exit()
