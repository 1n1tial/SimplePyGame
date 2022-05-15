# Tilemap Demo

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


# HeadsUpDisplay functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = green
    elif pct > 0.3:
        col = yellow
    else:
        col = red
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, white, outline_rect, 2)


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        snd_folder = path.join(game_folder, "snd")
        music_folder = path.join(game_folder, "music")
        self.map_folder = path.join(game_folder, "maps")
        self.title_font = path.join(img_folder, "ZOMBIE.TTF")
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 150))
        self.hit_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.hit_screen.fill((255, 30, 0, 100))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.zombie_img = pg.image.load(path.join(img_folder, ZOMBIE_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        self.zombie_splats = []
        for splat in ZOMBIE_SPLATS:
            s = pg.image.load(path.join(img_folder, splat)).convert_alpha()
            s = pg.transform.scale(s, (64, 64))
            self.zombie_splats.append(s)
        # sound load
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.mobs = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, "tiled1.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        '''
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == "Z":
                    self.zombie = Mob(self, col, row)
        '''
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "zombie":
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name in ["health item", "shotgun item"]:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.effects_sounds["level start"].set_volume(0.1)
        self.effects_sounds["level start"].play()

    def run(self):
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        # player hits items
        hits_item = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits_item:
            if hit.type == "health item" and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)
                self.effects_sounds["health_up"].play()
            if hit.type == 'shotgun item':
                hit.kill()
                self.player.weapon = 'shotgun'
                self.effects_sounds['shotgun_pickup'].play()

        # bullets hit mobs
        hits_mob = pg.sprite.groupcollide(self.mobs, self.bullets, False, False)
        for mob in hits_mob:
            hits_bullet = pg.sprite.groupcollide(self.bullets, self.mobs, True, False)
            for bullet in hits_bullet:
                mob.health -= bullet.dmg
                mob.vel += vec(bullet.knockback, 0).rotate(vec(1, 0).angle_to(bullet.dir))

        # zombie hits player
        if not self.player.damaged:
            hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
            for hit in hits:
                if random() < 0.7:
                    choice(self.player_hit_sounds).play()
                self.player.health -= ZOMBIE_DAMAGE
                hit.vel = vec(0, 0)
                if self.player.health <= 0:
                    self.playing = False
            if hits:
                self.player.hit()
                self.player.pos += vec(ZOMBIE_KNOCKBACK, 0).rotate(-hits[0].rot)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, lightgrey, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, lightgrey, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(bgcolor)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, blue, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, blue, self.camera.apply_rect(wall.rect), 1)
        # pg.draw.rect(self.screen, white, self.player.hit_rect, 2)
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        if self.player.got_hit:
            if pygame.time.get_ticks() - self.player.hit_time < 200:
                self.screen.blit(self.hit_screen, (0, 0))
            else:
                self.player.got_hit = False
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, red, WIDTH / 2, HEIGHT / 2, "center")
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

                if event.key == pg.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
