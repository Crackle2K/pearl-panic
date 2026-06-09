"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: May 29th, 2026
Description: This file contains various different objects and sprites for Pearl Panic. It includes the main diver, the enemies, a few different obstacles, as well as the environment.
"""

import pygame, random
from data import DataHandler

class Sprites(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, width=32, height=32, image=None):
        """Sets up a generic sprite at the given position. If no image is provided, a plain white box is used as a stand-in."""
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.speed = pygame.math.Vector2(0, 0)

        # If no image was handed to us, create a default white surface so nothing ends up invisible
        if image is None:
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.fill((255, 255, 255, 255))

        self.image = image
        self.rect = self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt=0.0):
        """Moves the sprite based on its current speed and how much time has passed since the last frame."""
        self.pos.x += self.speed.x * dt
        self.pos.y += self.speed.y * dt
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface):
        """Draws this sprite onto the given surface."""
        surface.blit(self.image, self.rect)

    def position(self):
        """Returns the sprite's current position as a Vector2."""
        return self.pos

    def set_position(self, x, y):
        """Teleports the sprite to a new position instantly, updating both the logical position and the rect."""
        self.pos.update(x, y)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

class Player(Sprites):

    def __init__(self, x=120, y=120, screen_width=680, screen_height=480):
        """Creates the player diver at the given starting position, loading the image and wiring up all the movement, dash, and ability state."""
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
        self.top_boundary = 0
        self.bottom_boundary = screen_height
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
        self._slow_active = False
        self._slow_timer = 0.0
        self._slow_duration = 5.0
        self._pre_slow_speed = self.move_speed
        self._current_drag_active = False
        self._current_drag_speed = 0

    def movement(self):
        """Reads the keyboard every frame and sets the player's velocity accordingly."""
        keys = pygame.key.get_pressed()
        self.speed.update(0, 0)

        # If an ocean current is dragging the player, lock out horizontal control and only let them steer up and down
        if self._current_drag_active:
            self.speed.x = self._current_drag_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.speed.y -= self.move_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.speed.y += self.move_speed
        else:
            # Normal free movement so the player can go in any of the four directions
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.speed.x -= self.move_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.speed.x += self.move_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.speed.y -= self.move_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.speed.y += self.move_speed

    def update_sprite(self):
        """Flips the diver image to face whichever direction they're currently moving."""
        # If the player just started moving left and the image is still pointing right, flip it
        if self.speed.x < 0 and self._facing_right:
            self._facing_right = False
            self.image = pygame.transform.flip(self._base_image, True, False)
            self.mask = pygame.mask.from_surface(self.image)
        # If the player just started moving right and the image is still pointing left, flip it back
        elif self.speed.x > 0 and not self._facing_right:
            self._facing_right = True
            self.image = self._base_image
            self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt=0.0):
        """Runs every frame, handles movement, dashing, sprite direction, screen boundaries, slow effects, and oxygen drain."""
        self.movement()
        self.dash()

        # If a dash is currently happening, keep pushing the player in the dash direction until the timer runs out
        if self._dash_active:
            self._dash_timer += dt
            self.speed.x += self._dash_dir * (60 / self._dash_duration)
            # The dash has lasted its full duration, so turn it off
            if self._dash_timer >= self._dash_duration:
                self._dash_active = False

        self.update_sprite()
        super().update(dt)
        self.smoke_dash.update(dt)

        # Clamp the player's position so they can never wander off the edge of the screen
        self.pos.x = max(0, min(self.pos.x, self.screen_width - self.rect.width))
        self.pos.y = max(self.top_boundary, min(self.pos.y, self.bottom_boundary - self.rect.height))
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # Count down the jellyfish slow effect and restore normal speed once it's worn off
        if self._slow_active:
            self._slow_timer += dt
            if self._slow_timer >= self._slow_duration:
                self.move_speed = self._pre_slow_speed
                self._slow_active = False

        # Once the current sweeps the player all the way to the right edge, release them
        if self._current_drag_active and self.pos.x >= self.screen_width - self.rect.width:
            self._current_drag_active = False

        # Drain one point of oxygen every second
        self.oxygen_timer += dt
        if self.oxygen_timer >= 1.0:
            self.oxygen = max(0, self.oxygen - 1)
            self.oxygen_timer -= 1.0

    def lose_oxygen(self):
        """Penalises the player by removing 5 oxygen which is called when a shark hits them."""
        self.oxygen = max(0, self.oxygen - 5)

    def lose_speed(self):
        """Drops the player's movement speed by 10 which is available for hazards that need it."""
        self.move_speed = max(0, self.move_speed - 10)

    def apply_slow(self):
        """Drops the player's speed to a crawl for a few seconds which is triggered by jellyfish stings."""
        # Only save the pre-slow speed if we're not already slowed, so stacking jellyfish don't corrupt the saved value
        if not self._slow_active:
            self._pre_slow_speed = self.move_speed
        self.move_speed = 20
        self._slow_active = True
        self._slow_timer = 0.0

    def start_current_drag(self, speed=250):
        """Activates the ocean current effect, which forcibly sweeps the player horizontally across the screen."""
        self._current_drag_active = True
        self._current_drag_speed = speed

    def gain_pearl(self):
        """Adds one pearl to the player's collection."""
        self.pearls += 1

    def dash(self):
        """Checks every frame if the player pressed Shift and fires off a dash if the cooldown has cleared."""
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Shift triggers the dash but only if we're not already mid-dash, the cooldown is done, and we're not on level 1
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
        """Loads the smoke animation sprite sheet and chops it into individual frames, including a mirrored set for leftward dashes."""
        sheet = pygame.image.load("assets/animations/smoke-dash-animation.png").convert_alpha()
        frame_w = sheet.get_width() // self.FRAME_COUNT
        frame_h = sheet.get_height()
        self._frames = []

        # Cut the sprite sheet into frames going left to right across the strip
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
        """Starts the smoke animation at the given position, resetting it back to the first frame."""
        self.active = True
        self._frame = 0
        self._timer = 0.0
        self._x = x
        self._y = y
        self._facing_right = facing_right

    def update(self, dt):
        """Advances the smoke animation one frame at a time and stops it when it reaches the end."""
        # Nothing to do if the animation isn't currently playing
        if not self.active:
            return

        self._timer += dt

        # Step to the next frame once enough time has passed
        if self._timer >= self.FRAME_DURATION:
            self._timer -= self.FRAME_DURATION
            self._frame += 1

            # We've played through all the frames and the animation is done
            if self._frame >= self.FRAME_COUNT:
                self.active = False

    def draw(self, surface):
        """Draws the current smoke frame onto the surface, doing nothing if the animation isn't active."""
        # Skip drawing entirely if no dash animation is in progress
        if not self.active:
            return

        # Use the right-facing or left-facing frames depending on which way the player dashed
        frames = self._frames if self._facing_right else self._flipped
        surface.blit(frames[self._frame], (self._x, self._y))

class Shield(Sprites):
    def __init__(self, player):
        """Creates the bubble shield sprite and attaches it to the player to starts inactive and is only usable in level 3."""
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
        """Turns the shield on when the player presses R which only works on level 3 and only if the cooldown has expired."""
        current_time = pygame.time.get_ticks()

        # Only allow the shield on level 3, and only if it's not already active and the cooldown has cleared
        if not self.active and (current_time - self._last_used) >= self._cooldown and self.data_handler.get_saved_level() != 1 and self.data_handler.get_saved_level() != 2:
            self.active = True
            self._activated_time = current_time

    def update(self, dt=0.0):
        """Tracks the shield's duration each frame and keeps it glued to the player's position."""
        current_time = pygame.time.get_ticks()

        # Auto-deactivate the shield once its time window has passed and start the cooldown clock
        if self.active and (current_time - self._activated_time) >= self._duration:
            self.active = False
            self._last_used = current_time

        # Keep the shield centered slightly behind and above the player at all times
        self.pos.x = self.player.pos.x - 20
        self.pos.y = self.player.pos.y - 15
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

class Pearl(Sprites):
    def __init__(self, y_min=20, y_max=450):
        """Spawns a pearl at a random position within the given vertical range."""
        pearl_img = pygame.image.load("assets/images/pearl.png").convert_alpha()
        pearl_img = pygame.transform.scale(pearl_img, (30, 40))
        x = random.randint(10, 670)
        y = random.randint(y_min, y_max)
        super().__init__(x=x, y=y, width=40, height=40, image=pearl_img)

class Obstacle(Sprites):
    def __init__(self, x, y, width, height, image, damage=10):
        """Base class for anything that can hurt or interact with the player which stores how much damage this obstacle deals."""
        super().__init__(x=x, y=y, width=width, height=height, image=image)
        self.damage = damage

    def check_offscreen(self):
        """Removes the obstacle from the game once it's drifted far enough past the edge of the screen."""
        # If it's wandered well outside the visible play area in any direction, there's no reason to keep it around
        if (self.pos.x < -150 or self.pos.x > 800 or
            self.pos.y < -100 or self.pos.y > 600):
            self.kill()

class Shark(Obstacle):
    def __init__(self, y_min=50, y_max=400):
        """Spawns a shark just off the left edge of the screen at a random height, ready to swim across."""
        x = -150
        y = random.randint(y_min, y_max)

        shark_img = pygame.image.load("assets/images/shark.png").convert_alpha()
        shark_img = pygame.transform.smoothscale(shark_img, (150, 150))
        super().__init__(x=x, y=y, width=150, height=150, image=shark_img, damage=20)
        self.speed.x = random.randint(70, 120)

    def update(self, dt):
        """Moves the shark forward each frame and removes it once it's gone off the right side of the screen."""
        super().update(dt)
        self.check_offscreen()


class Jellyfish(Obstacle):
    def __init__(self, y_min=50, y_max=430, y_boundary=600):
        """Spawns a jellyfish that drifts in from the left with a randomised diagonal trajectory."""
        x = -40
        y = random.randint(y_min, y_max)
        self.initial_speed_x = random.randint(40, 80)
        self.initial_speed_y = random.randint(-60, 60)

        jelly_img = pygame.image.load("assets/images/jellyfish.png").convert_alpha()
        jelly_img = pygame.transform.smoothscale(jelly_img, (30, 40))

        super().__init__(x=x, y=y, width=30, height=40, image=jelly_img, damage=10)
        self.speed.x = self.initial_speed_x
        self.speed.y = self.initial_speed_y
        self.y_boundary = y_boundary

    def update(self, dt):
        """Moves the jellyfish each frame and stops it from sinking past the sea floor boundary."""
        super().update(dt)

        # If the jellyfish has hit the floor boundary, park it right at the bottom and kill its vertical drift
        if self.pos.y + self.rect.height > self.y_boundary:
            self.pos.y = self.y_boundary - self.rect.height
            self.speed.y = 0
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        self.check_offscreen()

class Current(Obstacle):
    def __init__(self):
        """Creates an ocean current that sweeps in from well off the left side of the screen."""
        x = -670
        self.push_speed = 250
        y = random.randint(80, 380)

        current_img = pygame.image.load("assets/images/current.png").convert_alpha()
        current_img = pygame.transform.smoothscale(current_img, (200, 200))

        super().__init__(x=x, y=y, width=200, height=200, image=current_img, damage=0)
        self.speed.x = self.push_speed
        self.push_force = 60

    def check_offscreen(self):
        """Removes the current once it has fully swept past the right edge of the screen."""
        # The current only ever exits on the right side, so that's the only direction we need to check
        if self.pos.x > 750:
            self.kill()

    def update(self, dt):
        """Moves the current across the screen each frame and cleans it up once it exits."""
        super().update(dt)
        self.check_offscreen()
