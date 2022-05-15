import pygame
import random
pygame.init()


# Set Window
win = pygame.display.set_mode((500, 500))

# Change Description
pygame.display.set_caption("First First Game")

# Load images
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound("bullet.wav")
hitSound = pygame.mixer.Sound("hit.wav")

music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

screenWidth = 500
score = 0

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.jumpHeight = 0.5
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 13, self.y + 12, 36, 49)

    def draw(self, window):
        if self.walkCount == 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                window.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(walkRight[0], (self.x, self.y))
            else:
                window.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 13, self.y + 12, 36, 49)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.x = 60
        self.y = 418
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans", 40)
        text = font1.render("Ouch!", 1, (255, 0, 0))
        win.blit(text, (self.hitbox[0], self.hitbox[1] - 20))
        pygame.display.update()
        i = 0
        while i < 150:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 151
                    pygame.quit()



class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, start, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.path = [self.start, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 7, self.y + 2, 50, 54)
        self.ishit = False
        self.health = 99
        self.visible = True

    def draw(self, window):
        self.move()
        if self.visible:
            if self.walkCount == 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            self.hitbox = (self.x + 7, self.y + 2, 50, 54)

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 51 - ((50/100) * (100 - self.health)), 10))

            if self.ishit:
                pygame.draw.rect(window, (255, 255, 255), self.hitbox, 2)
                self.ishit = False
            else:
                pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.vel:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x > self.path[0] + self.vel:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        self.ishit = True


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render(f"Boss Health: {100 - score}", 1, (0, 0, 0))
    win.blit(text, (300, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()  # prevents stamping


# Main Loop
font = pygame.font.SysFont("comicsans", 30, True)

man = Player(300, 418, 64, 64)
goblin = Enemy(100, 423, 64, 64, random.randint(0, 70), random.randint(380, 436))
#  bullet = Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing)
bullets = []
shootLoop = 0

run = True
while run:
    # frames per sec
    clock.tick(27)

    if goblin.hitbox[0] - goblin.hitbox[2] <= man.hitbox[0] <= goblin.hitbox[0] + goblin.hitbox[2]\
            and goblin.hitbox[1] - goblin.hitbox[3] <= man.hitbox[1] <= goblin.hitbox[1] + goblin.hitbox[3]:
        hitSound.play()
        man.hit()

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    # terminate game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.hitbox[1] + goblin.hitbox[3] + bullet.radius * 2 >= bullet.y >= goblin.hitbox[1] - bullet.radius * 2 \
                and goblin.hitbox[0] + goblin.hitbox[2] + bullet.radius * 2 >= bullet.x >= goblin.hitbox[0] - bullet.radius * 2:
            hitSound.play()
            goblin.hit()
            score += 1
            bullets.pop(bullets.index(bullet))

        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    # arrow keys and jumping
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screenWidth - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * man.jumpHeight * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()


pygame.quit()
