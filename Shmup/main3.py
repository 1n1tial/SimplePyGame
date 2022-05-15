import pygame


from main2 import *


class Stage1(Game):
    pass


class Stage2(Game):
    pass


class StartScreen:
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
        self.background = pygame.image.load(path.join(self.img_dir, "starfield(2).png")).convert()
        # background = pygame.transform.scale(background, (screen_width, screen_height))
        self.background_rect = self.background.get_rect()

    def new(self):
        self.show_start_screen()
        self.running = False

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

    def draw_text(self, text, size, x, y, color=white):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


class SplashScreen(Game):
    pass


class MainGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True


def showSplashScreen(game):
    splashScreen = SplashScreen()
    SplashScreen.new()
    game.current_mode = splashScreen.mode


def playCurrentMode(game):
    if game.current_mode == '1':
        stage1 = Stage1()
        stage1.new()
    elif game.current_mode == '2':
        stage2 = Stage2()
        stage2.new()


def changeMode(game):
    pass



startScreen = StartScreen()
mainGame = MainGame()

while startScreen.running:
    startScreen.new()

alive = True
while mainGame.running:
    while alive:
        showSplashScreen(mainGame)
        playing = True
        while playing:
            playCurrentMode(mainGame)
            changeMode(mainGame)
    mainGame.show_go_screen()
