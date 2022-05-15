import pygame as pg
import sys
import random

vec = pg.math.Vector2

# constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
FPS = 60

# define colors
bg_color = (175, 215, 70)
grass_color = (167, 209, 61)
fruit_color = (126, 166, 114)
body_color = (183, 111, 122)


# game variables
cell_size = 40
cell_number = 20

# initialize game
pg.init()
screen = pg.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pg.display.set_caption('snake')
clock = pg.time.Clock()
game_font = pg.font.Font('font/PoetsenOne-Regular.ttf', 25)

# load images
# fruit image
fruit_img = pg.image.load('img/apple.png').convert_alpha()


# define game functions
def exit_game():
    pg.quit()
    sys.exit()


# define game classes
class Snake:
    def __init__(self):
        # load snake images
        self.head_up = pg.image.load('img/head_up.png').convert_alpha()
        self.head_down = pg.image.load('img/head_down.png').convert_alpha()
        self.head_right = pg.image.load('img/head_right.png').convert_alpha()
        self.head_left = pg.image.load('img/head_left.png').convert_alpha()

        self.tail_up = pg.image.load('img/tail_up.png').convert_alpha()
        self.tail_down = pg.image.load('img/tail_down.png').convert_alpha()
        self.tail_right = pg.image.load('img/tail_right.png').convert_alpha()
        self.tail_left = pg.image.load('img/tail_left.png').convert_alpha()

        self.body_vertical = pg.image.load('img/body_vertical.png').convert_alpha()
        self.body_horizontal = pg.image.load('img/body_horizontal.png').convert_alpha()

        self.body_tr = pg.image.load('img/body_tr.png').convert_alpha()
        self.body_tl = pg.image.load('img/body_tl.png').convert_alpha()
        self.body_br = pg.image.load('img/body_br.png').convert_alpha()
        self.body_bl = pg.image.load('img/body_bl.png').convert_alpha()

        # initialize snake dir
        self.body = [vec(7, 10), vec(6, 10), vec(5, 10)]
        self.direction = vec(1, 0)
        self.head = self.head_right
        self.tail = self.tail_right
        self.new_block = False

    def draw_snake(self):
        self.head = self.update_head_graphics()
        self.tail = self.update_tail_graphics()

        for i, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pg.Rect(x_pos, y_pos, cell_size, cell_size)

            if i == 0:
                screen.blit(self.head, block_rect)
            elif i == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[i - 1] - block
                next_block = block - self.body[i + 1]
                if previous_block == next_block:
                    if previous_block == vec(1, 0) or previous_block == vec(-1, 0):
                        screen.blit(self.body_horizontal, block_rect)
                    else:
                        screen.blit(self.body_vertical, block_rect)
                else:
                    if (previous_block == vec(1, 0) and next_block == vec(0, 1)) or \
                            (previous_block == vec(0, -1) and next_block == vec(-1, 0)):
                        screen.blit(self.body_tr, block_rect)
                    elif (previous_block == vec(0, -1) and next_block == vec(1, 0)) or \
                            (previous_block == vec(-1, 0) and next_block == vec(0, 1)):
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block == vec(-1, 0) and next_block == vec(0, -1)) or \
                            (previous_block == vec(0, 1) and next_block == vec(1, 0)):
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block == vec(0, 1) and next_block == vec(-1, 0)) or \
                            (previous_block == vec(1, 0) and next_block == vec(0, -1)):
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_direction = self.body[0] - self.body[1]
        if head_direction == vec(1, 0):
            self.head = self.head_right
        elif head_direction == vec(-1, 0):
            self.head = self.head_left
        elif head_direction == vec(0, 1):
            self.head = self.head_down
        elif head_direction == vec(0, -1):
            self.head = self.head_up

        return self.head

    def update_tail_graphics(self):
        tail_direction = self.body[-1] - self.body[-2]
        if tail_direction == vec(1, 0):
            self.tail = self.tail_right
        elif tail_direction == vec(-1, 0):
            self.tail = self.tail_left
        elif tail_direction == vec(0, 1):
            self.tail = self.tail_down
        elif tail_direction == vec(0, -1):
            self.tail = self.tail_up

        return self.tail

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pg.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        # pg.draw.rect(screen, fruit_color, fruit_rect)
        screen.blit(fruit_img, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = vec(self.x, self.y)  # topleft = (0, 0), 0 <= x, y <= cell_number - 1


class MainGame:
    def __init__(self):
        # create main game objects
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.draw_score()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        # if snake hits wall
        if not (0 <= self.snake.body[0].x <= cell_number - 1) or not (0 <= self.snake.body[0].y <= cell_number - 1):
            self.game_over()

        # if snake hit itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        exit_game()

    def draw_grass(self):
        for col in range(cell_number):
            for row in range(cell_number):
                grass_rect = pg.Rect(row * cell_size, col * cell_size, cell_size, cell_size)
                if (row + col) % 2:
                    pg.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surf = game_font.render(score_text, True, (56, 74, 12))
        screen.blit(score_surf, (10, 10))


# create main game
main_game = MainGame()

# set timer
SCREEN_UPDATE = pg.USEREVENT
pg.time.set_timer(SCREEN_UPDATE, 150)

# main game loop
while True:

    # fill background
    screen.fill(bg_color)

    # event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit_game()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit_game()

            if event.key == pg.K_UP:
                if abs(main_game.snake.direction.y) != 1:
                    main_game.snake.direction = vec(0, -1)
            if event.key == pg.K_DOWN:
                if abs(main_game.snake.direction.y) != 1:
                    main_game.snake.direction = vec(0, 1)
            if event.key == pg.K_LEFT:
                if abs(main_game.snake.direction.x) != 1:
                    main_game.snake.direction = vec(-1, 0)
            if event.key == pg.K_RIGHT:
                if abs(main_game.snake.direction.x) != 1:
                    main_game.snake.direction = vec(1, 0)

        if event.type == SCREEN_UPDATE:
            main_game.update()

    # draw
    main_game.draw_elements()

    # update
    pg.display.update()

    # framerate
    clock.tick(FPS)
