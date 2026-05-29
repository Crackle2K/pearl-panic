"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: May 29th, 2026
Description: This file contains various different objects and sprites for Pearl Panic. It includes the main diver, the enemies, a few different obstacles, as well as the environment.
"""

import pygame

class Sprites(pygame.sprite.Sprite):
    
    def __init__(self, x=0, y=0, width=32, height=32, *groups):
        
        super.__init__(*groups)
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        
        if image is None:
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.fill((255, 255, 255, 255))

        self.image = image
        self.rect = self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))
    
    def update(self, dt=0.0):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def position(self):
        return self.pos

    def set_position(self, x, y):
        self.pos.update(x, y)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        
class Player(Sprites):
    
    def __init__(self, x=120, y=120):
        
        player_image = pygame.image.load("assets/images/diver.png").convert_alpha()
        player_image = pygame.transform.smoothscale(player_image, (40, 60))
        super().__init__(x=x, y=y, width=40, height=60, image=player_image)
        
        self.oxygen = 60
        self.speed = 100
        self.pearls = 0
        
    def movement():
        pass
    
    def update_sprite(self):
        pass
    
    def lose_oxygen(self):
        self.oxygen -= 5
        
    def lose_speed(self):
        pass
    
    def gain_pearl(self):
        self.pearls += 1
        
class Obstacle(Sprites):
    pass

class Shark(Obstacle):
    pass

class Jellyfish(Obstacle):
    pass

class Current(Obstacle):
    pass