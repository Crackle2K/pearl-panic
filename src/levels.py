import data, pygame, os

class levels():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((680,480))
        self.screen.blit()
        pygame.display.flip()
class level1(levels):
    def __init__(self):
        super().__init__()
        beach_path = os.path.join(os.path.dirname(__file__), "assets", "images", "beach.png")
        beach_img = pygame.image.load(beach_path).convert()
        beach_img = pygame.transform.scale(beach_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

class level2(levels):
    def __init__(self):
        super().__init__()
        ocean_path = os.path.join(os.path.dirname(__file__), "assets", "images", "beach.png")
        ocean_img = pygame.image.load(ocean_path).convert()
        ocean_img = pygame.transform.scale(ocean_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
class level3(levels):
    def __init__(self):
        super().__init__() 
        cave_path = os.path.join(os.path.dirname(__file__), "assets", "images", "beach.png")
        cave_img = pygame.image.load(cave_path).convert()
        cave_img = pygame.transform.scale(cave_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))



