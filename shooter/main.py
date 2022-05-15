import pygame as pg
import os
import sys
import random
import csv
import button

pg.init()

clock = pg.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Shooter')

# game var
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 1
screen_scroll = 0
bg_scroll = 0
start_game = False
MAX_LEVELS = 3

# colors
bg_color = (144, 201, 120)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# player action var
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False


# load images
# button images
start_img = pg.image.load('img/start_btn.png').convert_alpha()
exit_img = pg.image.load('img/exit_btn.png').convert_alpha()
restart_img = pg.image.load('img/restart_btn.png').convert_alpha()
# background
pine1_img = pg.image.load('img/background/pine1.png').convert_alpha()
pine2_img = pg.image.load('img/background/pine2.png').convert_alpha()
mountain_img = pg.image.load('img/background/mountain.png').convert_alpha()
sky_img = pg.image.load('img/background/sky_cloud.png').convert_alpha()
# store tile in a list
tile_img_list = []
for i in range(TILE_TYPES):
    img = pg.image.load(f'img/tile/{i}.png').convert_alpha()
    img = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_img_list.append(img)
# bullet
bullet_img = pg.image.load('img/icons/bullet.png').convert_alpha()
# grenade
grenade_img = pg.image.load('img/icons/grenade.png').convert_alpha()
# pick up boxes
health_box_img = pg.image.load('img/icons/health_box.png')
ammo_box_img = pg.image.load('img/icons/ammo_box.png')
grenade_box_img = pg.image.load('img/icons/grenade_box.png')
item_images = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img
}


def draw_bg():
    screen.fill(bg_color)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))


def draw_text(text, font_type, size, color, x, y):
    font = pg.font.SysFont(font_type, size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def reset_level():
    enemies.empty()
    bullets.empty()
    grenades.empty()
    explosions.empty()
    item_boxes.empty()
    decorations.empty()
    water_group.empty()
    exits.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


class Soldier(pg.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pg.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.direction = 1
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pg.time.get_ticks()
        self.shoot_cooldown = 0
        self.start_ammo = ammo
        self.ammo = ammo
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        # ai
        self.move_counter = 0
        self.vision = pg.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        # load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            # count number of frames
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pg.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed = speed
        self.vel_y = 0
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.check_alive()
        self.update_animation()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement var
        screen_scroll = 0
        dx = 0
        dy = 0

        # assign movement var if moving left/right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check collision
        for tile in world.obstacle_list:
            # check for collision in x dir
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # if the ai has hit a wall; make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            # y dir
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # check for collision with water
        if pg.sprite.spritecollide(self, water_group, 0):
            self.health = 0

        # check for collision with exit
        level_complete = False
        if pg.sprite.spritecollide(self, exits, 0):
            level_complete = True

        # check if fallen off the map
        if self.rect.top >= SCREEN_HEIGHT:
            self.health = 0

        # check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # update rect pos
        self.rect.x += dx
        self.rect.y += dy
        self.x, self.y = self.rect.center

        # update scroll based on player pos
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.ammo -= 1
            self.shoot_cooldown = 20
            Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery,
                   self.direction)

    def ai(self):
        if self.alive and player.alive:
            if random.randint(1, 200) == 1 and not self.idling:
                self.idling = True
                self.update_action(0)  # 0: idle
                self.idling_counter = 50
            # check if ai is near player
            if self.vision.colliderect(player.rect):
                # stop running and face the player
                self.update_action(0)
                self.shoot()
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    elif self.direction == -1:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # 1: run
                    self.move_counter += 1
                    # update ai vision
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        # scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed
        if pg.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            if self.frame_index == len(self.animation_list[self.action]):
                if self.action != 3:
                    self.frame_index = 0
                else:
                    self.frame_index = len(self.animation_list[self.action]) - 1

    def update_action(self, new_action):
        # check if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pg.transform.flip(self.image, self.flip, 0), self.rect)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        pg.sprite.Sprite.__init__(self, bullets)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.direction = direction

    def update(self):
        # move bullet
        self.rect.x += self.speed * self.direction + screen_scroll
        # delete bullet
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()

        # check collision
        # with characters
        if pg.sprite.spritecollide(player, bullets, False):
            if player.alive:
                self.kill()
                player.health -= 5
        for enemy in enemies:
            if pg.sprite.spritecollide(enemy, bullets, False):
                if enemy.alive:
                    self.kill()
                    enemy.health -= 25
        # with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()


class Grenade(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        pg.sprite.Sprite.__init__(self, grenades)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        # trajectory movement
        self.vel_y += GRAVITY
        dx = self.speed * self.direction
        dy = self.vel_y

        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        # check for collision with level
        for tile in world.obstacle_list:
            # collision w/ walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
            # collision w/ ground/ceiling
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above ground, i.e. falling
                elif self.vel_y >= 0:
                    self.speed *= 0.4
                    self.vel_y *= -0.4
                    if abs(dy) < 0.5:
                        self.speed = 0
                        self.vel_y = 0

        # countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            Explosion(self.rect.x, self.rect.y, 0.5)
            # do damage to anyone within range
            if abs(self.rect.centerx - player.x) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.y) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemies:
                if abs(self.rect.centerx - enemy.x) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - enemy.y) < TILE_SIZE * 2:
                    enemy.health -= 50


class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y, scale):
        pg.sprite.Sprite.__init__(self, explosions)
        self.images = []
        for num in range(1, 6):
            img = pg.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.counter = 0

    def update(self):
        # scroll
        self.rect.x += screen_scroll

        EXPLOSION_SPD = 4
        # update explosion animation
        self.counter += 1
        if self.counter >= EXPLOSION_SPD:
            self.counter = 0
            self.frame_index += 1
            try:
                self.image = self.images[self.frame_index]
            except IndexError:
                self.kill()


class ItemBox(pg.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pg.sprite.Sprite.__init__(self, item_boxes)
        self.item_type = item_type
        self.image = item_images[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())

    def update(self):
        # scroll
        self.rect.x += screen_scroll
        # check if the player has picked up the box
        if pg.sprite.collide_rect(player, self):
            # check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 5
            elif self.item_type == 'Grenade':
                player.grenades += 3

            # delete box
            self.kill()


class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update with new health
        self.health = health
        pg.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pg.draw.rect(screen, green, (self.x, self.y, int(150 * self.health / self.max_health), 20))
        pg.draw.rect(screen, black, (self.x - 2, self.y - 2, 153, 23), 2)


class World:
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = tile_img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = img, img_rect
                    if tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile == 9 or tile == 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif 14 >= tile >= 11:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decorations.add(decoration)
                    elif tile == 15:
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 5)
                        health_bar = HealthBar(10, 10, player.health, player.max_health)
                    elif tile == 16:
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0)
                        enemies.add(enemy)
                    elif tile == 17:
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_boxes.add(item_box)
                    elif tile == 18:
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_boxes.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_boxes.add(item_box)
                    elif tile == 20:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exits.add(exit)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pg.sprite.Sprite):
    def __init__(self, img, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())

    def update(self):
        self.rect.x += screen_scroll


class Water(pg.sprite.Sprite):
    def __init__(self, img, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())

    def update(self):
        self.rect.x += screen_scroll


class Exit(pg.sprite.Sprite):
    def __init__(self, img, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())

    def update(self):
        self.rect.x += screen_scroll


# create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)


# create sprites
bullets = pg.sprite.Group()
grenades = pg.sprite.Group()
enemies = pg.sprite.Group()
explosions = pg.sprite.Group()
item_boxes = pg.sprite.Group()
decorations = pg.sprite.Group()
water_group = pg.sprite.Group()
exits = pg.sprite.Group()


# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for y, row in enumerate(reader):
        for x, tile in enumerate(row):
            world_data[y][x] = int(tile)

world = World()
player, health_bar = world.process_data(world_data)


run = True
while run:

    if not start_game:
        # draw menu
        screen.fill(bg_color)
        # add buttons
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            pg.quit()
            sys.exit()

    else:
        # update bg
        draw_bg()
        # update world
        world.draw()
        # HUD
        # player health
        health_bar.draw(player.health)
        # show ammo
        draw_text('AMMO: ', 'Futura', 30, white, 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + x * 10, 40))
        # show grenades
        draw_text('GRENADES: ', 'Futura', 30, white, 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + x * 15, 62))

        # update player actions
        if player.alive:
            # shoot bullets
            if shoot:
                player.shoot()
            # throw grenades
            elif grenade and not grenade_thrown and player.grenades > 0:
                Grenade(player.x + player.rect.size[0] * 0.5 * player.direction,
                        player.rect.top, player.direction)
                grenade_thrown = True
                player.grenades -= 1

            if player.in_air:
                player.update_action(2)  # 2:jump
            elif moving_left or moving_right:
                if not player.in_air:
                    player.update_action(1)  # 1:run
            else:
                player.update_action(0)  # 0:idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            # check if level is completed
            if level_complete:
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for y, row in enumerate(reader):
                            for x, tile in enumerate(row):
                                world_data[y][x] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)


        else:
            screen_scroll = 0
            if restart_button.draw(screen):
                bg_scroll = 0
                world_data = reset_level()
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for y, row in enumerate(reader):
                        for x, tile in enumerate(row):
                            world_data[y][x] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data)

        player.update()
        for enemy in enemies:
            enemy.ai()
            enemy.update()
            enemy.draw()
        bullets.update()
        grenades.update()
        explosions.update()
        item_boxes.update()
        decorations.update()
        water_group.update()
        exits.update()

        # draw section
        player.draw()
        bullets.draw(screen)
        grenades.draw(screen)
        explosions.draw(screen)
        item_boxes.draw(screen)
        decorations.draw(screen)
        water_group.draw(screen)
        exits.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.key == pg.K_a:
                moving_left = True
            if event.key == pg.K_d:
                moving_right = True
            if event.key == pg.K_w and player.alive:
                player.jump = True
            if event.key == pg.K_SPACE:
                shoot = True
            if event.key == pg.K_q:
                grenade = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_a:
                moving_left = False
            if event.key == pg.K_d:
                moving_right = False
            if event.key == pg.K_SPACE:
                shoot = False
            if event.key == pg.K_q:
                grenade = False
                grenade_thrown = False

    pg.display.update()
    clock.tick(60)
