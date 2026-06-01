
import pygame
import sys
import os

class Main:
    SCREEN_WIDTH = 680
    SCREEN_HEIGHT = 480

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pearl Panic")
        self.clock = pygame.time.Clock()
        self.show_intro()

    def show_intro(self):
        intro_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "intro.png")
        intro_img = pygame.image.load(intro_path).convert()
        intro_img = pygame.transform.scale(intro_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    waiting = False

            self.screen.blit(intro_img, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

Main()
