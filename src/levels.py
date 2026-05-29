import data, pygame 

class levels():
    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((680,480))
        self.screen.blit()
        pygame.display.flip()
class level1(levels):
    def __init__(self):
        super().__init__()
        bg_img = pygame.image.load('beach.png').convert() 
        bg_img = pygame.transform.scale(bg_img, (680, 480))

class level2(levels):
    def __init__(self):
        super().__init__()
        bg_img = pygame.image.load('ocean.png').convert()
        bg_img = pygame.transform.scale(bg_img, (680, 480))
class level3(levels):
    def __init__(self):
        super().__init__() 
        bg_img = pygame.image.load('cave.png').convert()
        bg_img = pygame.transform.scale(bg_img, (680, 480))


