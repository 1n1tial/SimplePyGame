import pygame
from pygame import mixer

# initialize the game
pygame.init()

# create clock
clock = pygame.time.Clock()

# create and refactor the game screen(window) as 'win'
screen_width = 800
screen_height = 1000
win = pygame.display.set_mode((screen_width, screen_height))

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space-invaders-icon.png")
pygame.display.set_icon(icon)

# load images
playerImg = pygame.image.load("space-invaders-player.png")
enemyImg = pygame.image.load("space-invaders-enemy.png")
bulletImg = pygame.image.load("bullet.png")
bg = pygame.image.load("background(800x1000).png")

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# scoring
text_score_x = 10
text_score_y = 10


def draw_text(window, text, font_type, font_size, x, y):
    font = pygame.font.Font(font_type, font_size)
    text = font.render(text, True, (255, 255, 255))
    window.blit(text, (x, y))


def show_score(window, x, y):
    draw_text(win, f"Score: {score_value}", "freesansbold.ttf", 32, x, y)


def game_over(window):
    font_over = pygame.font.Font("freesansbold.ttf", 64)
    text_over = font_over.render("Game Over", True, (255, 255, 255))
    window.blit(text_over, (200, 250))

class Player:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.invisible_border = 30
        self.vel = vel

    def draw(self, window):
        window.blit(playerImg, (self.x, self.y))


class Enemy:
    def __init__(self, x, y, start, end, vel_x, vel_y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.start = start
        self.end = end
        self.vel_x = vel_x
        self.vel_y = vel_y

    def draw(self, window):
        window.blit(enemyImg, (self.x, self.y))
        self.move()

    def move(self):
        if self.vel_x > 0:
            if self.x <= self.end - self.width - self.vel_x:
                self.x += self.vel_x
            else:
                self.vel_x *= -1
                self.y += self.vel_y
        else:
            if self.x >= self.start - self.vel_x:
                self.x += self.vel_x
            else:
                self.vel_x *= -1
                self.y += self.vel_y

    def hit(self):
        bullets.remove(bullet)
        enemies.remove(self)

    def victory(self):
        enemies.clear()


class Projectile:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel

    def draw(self, window):
        window.blit(bulletImg, (self.x, self.y))
        self.move()

    def move(self):
        if self.y >= self.vel:
            self.y -= self.vel
        else:
            bullets.pop(bullets.index(self))

def show_go_screen():
    draw_text(win, "Game Over", "freesansbold.ttf", 64, screen_width/2, screen_height/4)
    draw_text(win, "Arrow keys move, Space to fire", "freesansbold.ttf", 22,
             screen_width/2, screen_height/2)
    draw_text(win, "Press a key to begin", "freesansbold.ttf", 18, screen_width/2, screen_height/1.5)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def redraw_game_window():
    player.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    show_score(win, text_score_x, text_score_y)

    pygame.display.update()


# game loop
game_over = True
run = True
while run:
    if game_over:
        show_go_screen()
        game_over = False

        # define player, enemy
        player = Player(screen_width // 2 - 32, screen_height - 90, 10)
        enemies = []
        num_of_enemies_horizontal = 11
        num_of_enemies_vertical = 5
        btwn = 50
        for x in range(1, num_of_enemies_horizontal + 1):
            for y in range(1, num_of_enemies_vertical + 1):
                enemies.append(Enemy(x * btwn, y * btwn, x * btwn, x * btwn + screen_width - btwn * num_of_enemies_horizontal - 32, 3, 20))
        bullets = []
        score_value = 0

    # time delay
    clock.tick(50)

    win.blit(bg, (0, 0))

    # keyboard press and player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x >= player.vel + player.invisible_border:
        player.x -= player.vel
    elif keys[pygame.K_RIGHT] and player.x <= screen_width - player.width - player.vel - player.invisible_border:
        player.x += player.vel

    # terminate game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if len(bullets) < 1:
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                bullets.append(Projectile(player.x + player.width//2 - 16, player.y - 32, 8))

    for bullet in bullets:
        for enemy in enemies:
            if enemy.x - 10 <= bullet.x <= enemy.x + enemy.width + 10 \
                    and enemy.y - enemy.height <= bullet.y <= enemy.y + enemy.height:
                enemy.hit()
                score_value += 1
                collision_sound = mixer.Sound("explosion.wav")
                collision_sound.play()

    for enemy in enemies:
        if enemy.y >= player.y - enemy.height - 50:
            enemy.victory()
            game_over = True

    redraw_game_window()

pygame.quit()