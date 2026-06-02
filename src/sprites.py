"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: May 29th, 2026
Description: This file contains various different objects and sprites for Pearl Panic. It includes the main diver, the enemies, a few different obstacles, as well as the environment.
"""

import pygame

class Sprites(pygame.sprite.Sprite):
    
    def __init__(self, x=0, y=0, width=32, height=32, image=None, *groups):

        super().__init__(*groups)
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

    def __init__(self, x=120, y=120, screen_width=680, screen_height=480):

        player_image = pygame.image.load("assets/images/diver.png").convert_alpha()
        player_image = pygame.transform.smoothscale(player_image, (40, 60))
        super().__init__(x=x, y=y, width=40, height=60, image=player_image)

        self.oxygen = 60
        self.speed = 100
        self.pearls = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._base_image = player_image
        self._facing_right = True
        self._dash_last_time = 0
        self._dash_cooldown = 1000

    def movement(self):
        keys = pygame.key.get_pressed()
        self.vel.update(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel.y += self.speed

        if self.vel.length() > 0:
            self.vel.scale_to_length(self.speed)

    def update_sprite(self):
        if self.vel.x < 0 and self._facing_right:
            self._facing_right = False
            self.image = pygame.transform.flip(self._base_image, True, False)
        elif self.vel.x > 0 and not self._facing_right:
            self._facing_right = True
            self.image = self._base_image

    def update(self, dt=0.0):
        self.movement()
        self.dash()
        self.update_sprite()
        super().update(dt)
        self.pos.x = max(0, min(self.pos.x, self.screen_width - self.rect.width))
        self.pos.y = max(0, min(self.pos.y, self.screen_height - self.rect.height))
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def lose_oxygen(self):
        self.oxygen -= 5

    def lose_speed(self):
        self.speed = max(0, self.speed - 10)

    def gain_pearl(self):
        self.pearls += 1
        
    def dash(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            if (current_time - self._dash_last_time) >= self._dash_cooldown:
                if self._facing_right:
                    self.vel.x += (self.speed * 30)
                else:
                    self.vel.x -= (self.speed * 30)
                self._dash_last_time = current_time
        
        
class Obstacle(Sprites):
    pass

class Shark(Obstacle):
    pass

class Jellyfish(Obstacle):
    pass

class Current(Obstacle):
    pass