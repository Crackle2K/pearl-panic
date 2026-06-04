"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: May 29th, 2026
Description: This file contains various different objects and sprites for Pearl Panic. It includes the main diver, the enemies, a few different obstacles, as well as the environment.
"""

import pygame, random 
from data import DataHandler
class Sprites(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, width=32, height=32, image=None):

        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.speed = pygame.math.Vector2(0, 0)

        if image is None:
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.fill((255, 255, 255, 255))

        self.image = image
        self.rect = self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))
    
    def update(self, dt=0.0):
        self.pos.x += self.speed.x * dt
        self.pos.y += self.speed.y * dt
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
        self._data_handler = DataHandler()
        player_image = pygame.image.load("assets/images/diver.png").convert_alpha()
        player_image = pygame.transform.smoothscale(player_image, (40, 60))
        super().__init__(x=x, y=y, width=40, height=60, image=player_image)

        self.oxygen = 60
        self.oxygen_timer = 0.0
        self.move_speed = 100
        self.pearls = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._base_image = player_image
        self._facing_right = True
        self._dash_last_time = 0
        self._dash_cooldown = 1000
        self._dash_active = False
        self._dash_timer = 0.0
        self._dash_duration = 0.12
        self._dash_dir = 1
        self.smoke_dash = SmokeDash()
        self.data_handler = DataHandler()

    def movement(self):
        keys = pygame.key.get_pressed()
        self.speed.update(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed.x -= self.move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed.x += self.move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed.y -= self.move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed.y += self.move_speed
            
    def update_sprite(self):
        if self.speed.x < 0 and self._facing_right:
            self._facing_right = False
            self.image = pygame.transform.flip(self._base_image, True, False)
        elif self.speed.x > 0 and not self._facing_right:
            self._facing_right = True
            self.image = self._base_image

    def update(self, dt=0.0):
        self.movement()
        self.dash()
        if self._dash_active:
            self._dash_timer += dt
            self.speed.x += self._dash_dir * (60 / self._dash_duration)
            if self._dash_timer >= self._dash_duration:
                self._dash_active = False
        self.update_sprite()
        super().update(dt)
        self.smoke_dash.update(dt)
        self.pos.x = max(0, min(self.pos.x, self.screen_width - self.rect.width))
        self.pos.y = max(0, min(self.pos.y, self.screen_height - self.rect.height))
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.oxygen_timer += dt
        if self.oxygen_timer >= 1.0:
            self.oxygen = max(0, self.oxygen - 1)
            self.oxygen_timer -= 1.0

    def lose_oxygen(self):
        self.oxygen -= 5

    def lose_speed(self):
        self.move_speed = max(0, self.move_speed - 10)

    def gain_pearl(self):
        self.pearls += 1
        
    def dash(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            if not self._dash_active and (current_time - self._dash_last_time) >= self._dash_cooldown and self.data_handler.get_saved_level() != 1:
                self._dash_active = True
                self._dash_timer = 0.0
                self._dash_dir = 1 if self._facing_right else -1
                self.smoke_dash.play(self.pos.x - 5, self.pos.y + 10, self._facing_right)
                self._dash_last_time = current_time

class SmokeDash:
    FRAME_COUNT = 7
    FRAME_DURATION = 0.06

    def __init__(self):
        sheet = pygame.image.load("assets/animations/smoke-dash-animation.png").convert_alpha()
        frame_w = sheet.get_width() // self.FRAME_COUNT
        frame_h = sheet.get_height()
        self._frames = []
        for i in range(self.FRAME_COUNT):
            frame = sheet.subsurface(pygame.Rect(i * frame_w, 0, frame_w, frame_h))
            frame = pygame.transform.scale(frame, (50, 40))
            self._frames.append(frame)
        self._flipped = [pygame.transform.flip(f, True, False) for f in self._frames]
        self.active = False
        self._frame = 0
        self._timer = 0.0
        self._x = 0
        self._y = 0
        self._facing_right = True

    def play(self, x, y, facing_right):
        self.active = True
        self._frame = 0
        self._timer = 0.0
        self._x = x
        self._y = y
        self._facing_right = facing_right

    def update(self, dt):
        if not self.active:
            return
        self._timer += dt
        if self._timer >= self.FRAME_DURATION:
            self._timer -= self.FRAME_DURATION
            self._frame += 1
            if self._frame >= self.FRAME_COUNT:
                self.active = False

    def draw(self, surface):
        if not self.active:
            return
        frames = self._frames if self._facing_right else self._flipped
        surface.blit(frames[self._frame], (self._x, self._y))

class Shield(Sprites):
    def __init__(self, player):
        self.data_handler = DataHandler()
        shield_image = pygame.image.load("assets/images/bubble_shield.png").convert_alpha()
        shield_image = pygame.transform.smoothscale(shield_image, (90, 90))
        shield_image.set_alpha(128)
        super().__init__(x=player.pos.x, y=player.pos.y, width=80, height=90, image=shield_image)
        self.player = player
        self.active = False
        self._duration = 2000
        self._cooldown = 3000
        self._activated_time = 0
        self._last_used = 0

    def activate(self):
        current_time = pygame.time.get_ticks()
        if not self.active and (current_time - self._last_used) >= self._cooldown and self.data_handler.get_saved_level() != 1 and self.data_handler.get_saved_level() != 2:
            self.active = True
            self._activated_time = current_time

    def update(self, dt=0.0):
        current_time = pygame.time.get_ticks()
        if self.active and (current_time - self._activated_time) >= self._duration:
            self.active = False
            self._last_used = current_time
        self.pos.x = self.player.pos.x - 20
        self.pos.y = self.player.pos.y - 15
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        
class Pearl(Sprites):
    def __init__(self):  
        pearl_img = pygame.image.load("assets/images/pearl.png").convert_alpha()
        pearl_img = pygame.transform.scale(pearl_img, (30,40))
        x = random.randint(10, 670)
        y = random.randint(20, 450)
        super().__init__(x=x, y=y, width=40, height=40, image=pearl_img)

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
        x = 10
        y = random.randint(50, 400)
        
        shark_img = pygame.image.load("assets/images/shark.png").convert_alpha()
        shark_img = pygame.transform.smoothscale(shark_img, (150, 150))
        super().__init__(x=x, y=y, width= 150, height=150, image = shark_img, damage= 20 )
        self.speed.x = random.randint(70,120) 
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
        
        super().__init__(x=x, y=y, width=30, height=40, image=jelly_img, damage=10)
        self.speed.x = self.initial_speed_x
        self.speed.y = self.initial_speed_y

    def update(self, dt):
        super().update(dt)
        self.check_offscreen()

class Current(Obstacle):
    def __init__(self):
        
        x = -670
        self.push_speed = 250
        y = random.randint(80, 380)
        
        current_img = pygame.image.load("assets/images/current.png").convert_alpha()
        current_img = pygame.transform.smoothscale(current_img, (200, 200))
           
        super().__init__(x=x, y=y, width=200, height=200, image=current_img, damage=0)
        self.image = current_img
        self.speed.x = self.push_speed
        self.push_force = 60
    def check_offscreen(self):
        if self.pos.x > 750:
            self.kill()
    def update(self, dt):
        super().update(dt)
        self.check_offscreen()