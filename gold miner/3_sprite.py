import pygame
import sys
import os

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30

RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Gold Miner")

default_offset_x_claw = 40
to_x = 0

LEFT = -1
RIGHT = 1
STOP = 0


class Claw(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center=pos)
        self.pos = pos
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.direction = LEFT
        self.ang_spd = 2.5
        self.ang = 10

    def update(self):
        if self.ang >= 170:
            self.ang = 170
            self.set_direction(RIGHT)
        if self.ang <= 10:
            self.ang = 10
            self.set_direction(LEFT)

        if self.direction == LEFT:
            self.ang += self.ang_spd
        elif self.direction == RIGHT:
            self.ang -= self.ang_spd
        elif self.direction == STOP:
            pass

        self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, -self.ang, 1)
        offset_rotated = self.offset.rotate(self.ang)
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, scrn):
        scrn.blit(self.image, self.rect)
        pygame.draw.circle(scrn, RED, self.pos, 3)
        pygame.draw.line(scrn, BLACK, self.pos, self.rect.center, 5)


class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=pos)


def setup_gemstone():
    gemstone_group.add(Gemstone(gemstone_images[0], (200, 380)))
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500)))
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380)))
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 400)))


clock = pygame.time.Clock()

# load images
current_path = os.path.dirname(__file__)
# load background
bg_img = pygame.image.load(os.path.join(current_path, "background.png"))
# load gemstone img
gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")),
    pygame.image.load(os.path.join(current_path, "big_gold.png")),
    pygame.image.load(os.path.join(current_path, "stone.png")),
    pygame.image.load(os.path.join(current_path, "diamond.png"))
]

gemstone_group = pygame.sprite.Group()
setup_gemstone()

claw_img = pygame.image.load(os.path.join(current_path, 'claw.png'))
claw = Claw(claw_img, (SCREEN_WIDTH // 2, 110))


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            claw.set_direction(STOP)

    screen.blit(bg_img, (0, 0))

    claw.update()

    gemstone_group.draw(screen)
    claw.draw(screen)
    pygame.display.update()


pygame.quit()
sys.exit()

