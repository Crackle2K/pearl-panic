import pygame, os

class level():
    def __init__(self, screen):
        self.screen = screen 
        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()
        self.bg_img = None
    def update(self):
        pass 
    def draw(self):
        self.screen.blit(self.bg_img, (0,0))
class level1(level):
    def __init__(self, screen):
        super().__init__(screen)
        beach_path = os.path.join(os.path.dirname(__file__), "assets", "images", "beach.png")
        self.bg_img = pygame.image.load(beach_path).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

class level2(level):
    def __init__(self, screen):
        super().__init__(screen)
        ocean_path = os.path.join(os.path.dirname(__file__), "assets", "images", "ocean.png")
        self.bg_img = pygame.image.load(ocean_path).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
class level3(level):
    def __init__(self, screen):
        super().__init__(screen)
        cave_path = os.path.join(os.path.dirname(__file__), "assets", "images", "cave.png")
        self.bg_img = pygame.image.load(cave_path).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))



