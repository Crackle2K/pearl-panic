"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: June 2nd, 2026
Description: This file contains the level classes for Pearl Panic. It includes a base level class as well as individual implementations for each of the three playable stages.
"""

import pygame
from sprites import Player
import sprites

class level():
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()
        self.bg_img = None
        self.player = Player(120, 120, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.obstacle_group = pygame.sprite.Group()
        self.shark_frames = 0 
        self.jelly_frames = 0
        self.current_frames = 0
        self.shark_interval = 120
        self.jelly_interval = 180
        self.current_interval = 150
    def spawn_shark(self):
        self.shark_frames += 1
        if self.shark_frames >= self.shark_interval:
            new_shark = sprites.Shark() 
            self.obstacle_group.add(new_shark)
            self.shark_frames = 0 

    def spawn_jellyfish(self):
        self.jelly_frames += 1
        if self.jelly_frames >= self.jelly_interval:
            new_jelly = sprites.Jellyfish()
            self.obstacle_group.add(new_jelly)
            self.jelly_frames = 0

    def spawn_current(self):
        self.current_frames += 1
        if self.current_frames >= self.current_interval:
            new_current = sprites.Current()
            self.obstacle_group.add(new_current)
            self.current_frames = 0
    def handle_spawns(self):
        pass

    def update(self, dt=0.0):
        self.handle_spawns()
        self.player.update(dt)
        self.obstacle_group.update(dt)
    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.player.draw(self.screen)
        self.obstacle_group.draw(self.screen)

class level1(level):
    def __init__(self, screen):
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/beach.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    def handle_spawns(self):
        self.spawn_shark()
class level2(level):
    def __init__(self, screen):
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/ocean.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    def handle_spawns(self):
        self.spawn_shark()
        self.spawn_jellyfish()
class level3(level):
    def __init__(self, screen):
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/cave.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    def handle_spawns(self):
        self.spawn_shark()
        self.spawn_jellyfish()
        self.spawn_current()


