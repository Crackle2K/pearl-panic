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
        
class Obstacle(Sprites):
    def __init__(self, x, y, width, height, image, damage=10):
        super().__init__(x=x, y=y, width=width, height=height, image=image)
        self.damage = damage
    def check_offscreen(self):
        if (self.pos.x < -150 or self.pos.x > 800 or 
            self.pos.y < -100 or self.pos.y > 600):
            self.kill()

class Shark(Obstacle):
    def __init__(self):
        x = 700
        y = random.randint(50, 400)
        
        shark_img = pygame.image.load("assets/images/shark.png").convert_alpha()
        shark_img = pygame.transform.smoothscale(shark_img, (80, 40))
        super().init(x=x, y=y, width= 80, height=40, damage= 20 )
        self.image = shark_img
        self.speed.x = random.randint(-120, -70) 

    def update(self, dt):
        super().update(dt)
        self.check_offscreen()


class Jellyfish(Obstacle):
    def __init__(self):
        x = -40
        y = random.randint(50, 430)
        self.initial_speed_x = random.randint(40, 80)
        self.initial_speed_y = random.randint(-60, 60)
       
        jelly_img = pygame.image.load("assets/images/jellyfish.png").convert_alpha()
        jelly_img = pygame.transform.smoothscale(jelly_img, (30, 40))
        
        super().__init__(x=x, y=y, width=30, height=40, damage=10)
        self.image = jelly_img
        self.speed.x = self.initial_speed_x
        self.speed.y = self.initial_speed_y

    def update(self, dt):
        super().update(dt)
        self.check_offscreen()

class Current(Obstacle):
    def __init__(self):
        
        x = -700
        self.speed = 250

        y = random.randint(80, 380)
        
        current_img = pygame.image.load("assets/images/current.png").convert_alpha()
        current_img = pygame.transform.smoothscale(current_img, (680, 50))
           
        super().__init__(x=x, y=y, width=680, height=50, damage=0)
        self.image = current_img
        self.vel.x = self.speed
        self.push_force = 60

    def update(self, dt):
        super().update(dt)
        self.check_offscreen()