"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: June 2nd, 2026
Description: This file contains the level classes for Pearl Panic. It includes a base level class as well as individual implementations for each of the three playable stages.
"""

import pygame
from sprites import Player

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
        self.bg_img = pygame.image.load("assets/images/beach.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

class level2(level):
    def __init__(self, screen):
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/ocean.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
class level3(level):
    def __init__(self, screen):
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/cave.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))



