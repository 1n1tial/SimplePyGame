# Jumpy! - platform game

# credits
# art by Kenney.nl
# sfx provided by https://jfxr.frozenfractal.com/
# Somewhere in the Elevator (as bgm_start1) by Peachtea@You're Perfect Studio
# Yippee (as bgm_start2) by Snabisch
# happytune (as bgm1) by syncopika
# Sophomore Makeout (as bgm2) by Silent Partner
# Take You Home Tonight (as bgm3) by Vibe Tracks


import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "img")

        # load high score
        with open(path.join(self.dir, HS_FILE), "r") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        # load cloud images
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, "cloud{}.png".format(i))).convert())

        # load sounds
        self.snd_dir = path.join(self.dir, "snd")
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, "jump1.wav"))

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        for plat in platform_list:
            Platform(self, *plat)
        self.mob_timer = pg.time.get_ticks()
        pg.mixer.music.load(path.join(self.snd_dir, "bgm1.ogg"))
        pg.mixer.music.set_volume(0.8)
        for i in range(5):
            c = Cloud(self)
            c.rect.y += 500
        self.run()

    def run(self):
        # game loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # game loop - update
        self.all_sprites.update()

        # spawn a mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]) and self.mobs.__len__() < 1:
            self.mob_timer = now
            Mob(self)

        # collision w/mobs
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        # collision check w/platforms - only if falling
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if lowest.rect.left - 7 <= self.player.pos.x <= lowest.rect.right + 7:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
                        self.player.boosting = False

        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(100) < 10:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / (cloud.distance/10)), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # spawn new platforms to keep their number
        while len(self.platforms) <= 5:
            width = random.randrange(50, 100)
            Platform(self,
                     random.randrange(0, WIDTH - width),
                     random.randrange(-75, -30))

        # if player hits powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == "boost":
                self.player.vel.y = -BOOST_POWER
                # to prevent jumpcut from stopping the boost
                self.player.boosting = True

        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

    def events(self):
        # game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # game loop - draw
        self.screen.fill(bgcolor)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, white, WIDTH / 2, 15)

        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(path.join(self.snd_dir, "bgm_start2.ogg"))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(loops=-1)
        self.screen.fill(bgcolor)
        self.draw_text(TITLE, 48, white, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows move, Space to jump", 22, white, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, white, WIDTH / 2, HEIGHT / 1.5)
        self.draw_text(f"High Score: {self.highscore}", 22, white, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue? screen
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, "bgm_start2.ogg"))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(loops=-1)
        self.screen.fill(bgcolor)
        self.draw_text("GAME OVER", 48, white, WIDTH / 2, HEIGHT / 4)
        self.draw_text(f"Score: {self.score}", 22, white, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, white, WIDTH / 2, HEIGHT / 1.5)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, white, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.highscore))
        else:
            self.draw_text(f"High Score: {self.highscore}", 22, white, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
