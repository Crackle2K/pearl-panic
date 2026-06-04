"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: June 2nd, 2026
Description: This file contains the level classes for Pearl Panic. It includes a base level class as well as individual implementations for each of the three playable stages.
"""

import pygame
import math
from sprites import Player
import sprites

class level():
    
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()
        self.bg_img = None
        self.player = Player(120, 120, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.shield = sprites.Shield(self.player)
        self.obstacle_group = pygame.sprite.Group()
        self.shark_frames = 0 
        self.jelly_frames = 0
        self.current_frames = 0
        self.shark_interval = 120
        self.jelly_interval = 180
        self.current_interval = 150
        self.pearl_interval = 100
        self.pearl_frames = 0
        self.oxygen_font = pygame.font.Font("assets/fonts/retroica.ttf", 30)
    def spawn_pearl(self):
        self.pearl_frames +=1
        if self.pearl_frames >= self.pearl_interval:
            new_pearl = sprites.Pearl() 
            self.obstacle_group.add(new_pearl)
            self.pearl_frames = 0

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.shield.activate()
        self.shield.update(dt)
        self.player.update(dt)
        self.obstacle_group.update(dt)
        if self.shield.active:
            pygame.sprite.spritecollide(self.shield, self.obstacle_group, True)

    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.player.draw(self.screen)
        if self.shield.active:
            self.shield.draw(self.screen)
        self.obstacle_group.draw(self.screen)
        self.draw_oxygen_bar()

    def draw_oxygen_bar(self):
        radius = 35
        cx = 55
        cy = self.SCREEN_HEIGHT - 55

        pygame.draw.circle(self.screen, (10, 25, 45), (cx, cy), radius)

        max_oxygen = 60
        oxygen = self.player.oxygen
        ratio = oxygen / max_oxygen

        if ratio > 0.5:
            arc_color = (0, 180, 255)
        elif ratio > 0.25:
            arc_color = (255, 165, 0)
        else:
            arc_color = (220, 50, 50)

        if ratio > 0:
            arc_rect = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)
            start_angle = math.pi / 2
            stop_angle = math.pi / 2 + ratio * 2 * math.pi
            pygame.draw.arc(self.screen, arc_color, arc_rect, start_angle, stop_angle, 6)

        pygame.draw.circle(self.screen, (50, 80, 110), (cx, cy), radius, 2)

        text_surf = self.oxygen_font.render(str(oxygen), True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(cx, cy))
        self.screen.blit(text_surf, text_rect)

class level1(level):
    
    def __init__(self, screen):
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/beach.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
    def handle_spawns(self):
        self.spawn_shark()
        self.spawn_pearl()
class level2(level):
    
    def __init__(self, screen):
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/ocean.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
    def handle_spawns(self):
        self.spawn_shark()
        self.spawn_jellyfish()
        self.spawn_pearl()
        
class level3(level):
    
    def __init__(self, screen):
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/cave.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
    def handle_spawns(self):
        self.spawn_shark()
        self.spawn_jellyfish()
        self.spawn_current()
        self.spawn_pearl()


