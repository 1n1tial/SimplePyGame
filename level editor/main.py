import pygame as pg
import sys
import button
import csv
import pickle

pg.init()

clock = pg.time.Clock()
FPS = 60

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pg.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pg.display.set_caption('Level Editor')

# define game var
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21

current_tile = 0

level = 0

# load images
pine1_img = pg.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pg.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pg.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pg.image.load('img/Background/sky_cloud.png').convert_alpha()
save_img = pg.image.load('img/save_btn.png').convert_alpha()
load_img = pg.image.load('img/load_btn.png').convert_alpha()

# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pg.image.load(f'img/tile/{x}.png').convert_alpha()
    img = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# def colors
green = (144, 201, 120)
white = (255, 255, 255)
red = (200, 25, 25)

# define font
font = pg.font.SysFont('Futura', 30)

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0


# draw text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# create function for drawing background
def draw_bg():
    screen.fill(green)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))


# draw grid
def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pg.draw.line(screen, white, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    # horizontal lines
    for r in range(ROWS + 1):
        pg.draw.line(screen, white, (0, r * TILE_SIZE), (SCREEN_WIDTH, r * TILE_SIZE))


# function for drawing world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


# create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

run = True
while run:
    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, white, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, white, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # save and load data
    if save_button.draw(screen):
        pickle_out = open(f'level{level}_data', 'wb')
        pickle.dump(world_data, pickle_out)
        pickle_out.close()
    #     with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
    #         writer = csv.writer(csvfile, delimiter=',')
    #         for row in world_data:
    #             writer.writerow(row)
    if load_button.draw(screen):
        # reset scroll back to start
        scroll = 0
        world_data = []
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
        # with open(f'level{level}_data.csv', newline='') as csvfile:
        #     reader = csv.reader(csvfile, delimiter=',')
        #     for x, row in enumerate(reader):
        #         for y, tile in enumerate(row):
        #             world_data[x][y] = int(tile)


    # draw tile panel and tiles
    pg.draw.rect(screen, green, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight the selected tile
    pg.draw.rect(screen, red, button_list[current_tile].rect, 3)

    # scroll the map
    if scroll_left and scroll >= 5 * scroll_speed:
        scroll -= 5 * scroll_speed

    if scroll_right and scroll <= MAX_COLS * TILE_SIZE - SCREEN_WIDTH - 5 * scroll_speed:
        scroll += 5 * scroll_speed

    # add new tiles to the screen
    # get mouse pos
    pos = pg.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check if the coordinates are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile value
        if pg.mouse.get_pressed()[0]:
            world_data[y][x] = current_tile
        if pg.mouse.get_pressed()[2]:
            world_data[y][x] = -1

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.key == pg.K_UP:
                level += 1
            if event.key == pg.K_DOWN and level > 0:
                level -= 1
            if event.key == pg.K_LEFT:
                scroll_left = True
            if event.key == pg.K_RIGHT:
                scroll_right = True
            if event.key == pg.K_RSHIFT:
                scroll_speed = 3
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                scroll_left = False
            if event.key == pg.K_RIGHT:
                scroll_right = False
            if event.key == pg.K_RSHIFT:
                scroll_speed = 1

    pg.display.update()
    clock.tick(FPS)
