"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: June 2nd, 2026
Description: This file contains the level classes for Pearl Panic. It includes a base level class as well as individual implementations for each of the three playable stages.
"""

import pygame
import math
from sprites import Player
import sprites

SEA_LEVEL_Y = 185
SEA_FLOOR_Y = 400

class level():

    def __init__(self, screen):
        """Sets up everything the level needs — the screen, player, shield, spawn timers, fonts, and pearl counter assets."""
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
        self.pearl_font = pygame.font.Font("assets/fonts/retroica.ttf", 22)
        self.shark_y_min = 50
        self.shark_y_max = 400
        self.pearl_y_min = 20
        self.pearl_y_max = 450
        self.jelly_y_min = 50
        self.jelly_y_max = 430
        self.jelly_y_boundary = 600

        # Load and cache a small pearl icon to use in the HUD counter so we don't reload it every frame
        pearl_img = pygame.image.load("assets/images/pearl.png").convert_alpha()
        self._pearl_icon = pygame.transform.scale(pearl_img, (22, 29))

    def spawn_pearl(self):
        """Counts frames and drops a new pearl into the level once the spawn interval has passed."""
        self.pearl_frames += 1

        # Once enough frames have gone by, it's time to add a new pearl to the world
        if self.pearl_frames >= self.pearl_interval:
            new_pearl = sprites.Pearl(y_min=self.pearl_y_min, y_max=self.pearl_y_max)
            self.obstacle_group.add(new_pearl)
            self.pearl_frames = 0

    def spawn_shark(self):
        """Counts frames and releases a new shark from off-screen once the spawn interval has passed."""
        self.shark_frames += 1

        # Time to send another shark across the screen
        if self.shark_frames >= self.shark_interval:
            new_shark = sprites.Shark(y_min=self.shark_y_min, y_max=self.shark_y_max)
            self.obstacle_group.add(new_shark)
            self.shark_frames = 0

    def spawn_jellyfish(self):
        """Counts frames and launches a new jellyfish once the spawn interval has passed."""
        self.jelly_frames += 1

        # Enough frames have passed — send in a jellyfish
        if self.jelly_frames >= self.jelly_interval:
            new_jelly = sprites.Jellyfish(y_min=self.jelly_y_min, y_max=self.jelly_y_max, y_boundary=self.jelly_y_boundary)
            self.obstacle_group.add(new_jelly)
            self.jelly_frames = 0

    def spawn_current(self):
        """Counts frames and sweeps a new ocean current onto the screen once the spawn interval has passed."""
        self.current_frames += 1

        # Time to push another current across the level
        if self.current_frames >= self.current_interval:
            new_current = sprites.Current()
            self.obstacle_group.add(new_current)
            self.current_frames = 0

    def handle_spawns(self):
        """Override this in each subclass to control which obstacles and pickups appear in that level."""
        pass

    def update(self, dt=0.0):
        """Runs every game frame — spawns obstacles, handles input for the shield, updates all sprites, and processes collisions."""
        self.handle_spawns()
        keys = pygame.key.get_pressed()

        # If the player pressed R, try to pop the bubble shield
        if keys[pygame.K_r]:
            self.shield.activate()

        self.shield.update(dt)
        self.player.update(dt)
        self.obstacle_group.update(dt)

        # When the shield is active, it destroys anything it touches rather than letting it reach the player
        if self.shield.active:
            pygame.sprite.spritecollide(self.shield, self.obstacle_group, True, pygame.sprite.collide_mask)

        # Only check player collisions when the shield is down — the shield handles its own hits above
        if not self.shield.active:
            hits = pygame.sprite.spritecollide(self.player, self.obstacle_group, False, pygame.sprite.collide_mask)

            # Go through every sprite the player is currently touching and apply the right effect
            for hit in hits:
                if isinstance(hit, sprites.Shark):
                    # Shark hit — costs the player a chunk of oxygen and then disappears
                    self.player.lose_oxygen()
                    hit.kill()
                elif isinstance(hit, sprites.Jellyfish):
                    # Jellyfish sting — slows the player down for a few seconds
                    self.player.apply_slow()
                    hit.kill()
                elif isinstance(hit, sprites.Current):
                    # Ocean current — grabs the player and drags them across the screen
                    self.player.start_current_drag(hit.push_speed)
                elif isinstance(hit, sprites.Pearl):
                    # Pearl collected — add it to the player's total and remove it from the world
                    self.player.gain_pearl()
                    hit.kill()

    def draw(self):
        """Draws everything visible in the level — background, player, effects, enemies, and HUD elements."""
        self.screen.blit(self.bg_img, (0, 0))
        self.player.smoke_dash.draw(self.screen)
        self.player.draw(self.screen)

        # Only draw the shield bubble when it's actually active
        if self.shield.active:
            self.shield.draw(self.screen)

        self.obstacle_group.draw(self.screen)
        self.draw_oxygen_bar()
        self.draw_pearl_counter()

    def draw_oxygen_bar(self):
        """Draws the circular oxygen gauge in the bottom-left corner, changing colour as the oxygen runs low."""
        radius = 35
        cx = 55
        cy = self.SCREEN_HEIGHT - 55

        pygame.draw.circle(self.screen, (10, 25, 45), (cx, cy), radius)

        max_oxygen = 60
        oxygen = self.player.oxygen
        ratio = oxygen / max_oxygen

        # Pick a colour for the arc based on how much oxygen is left — green, orange, then red when critical
        if ratio > 0.5:
            arc_color = (0, 180, 255)
        elif ratio > 0.25:
            arc_color = (255, 165, 0)
        else:
            arc_color = (220, 50, 50)

        # Only draw the arc when there's actually some oxygen left to show
        if ratio > 0:
            arc_rect = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)
            start_angle = math.pi / 2
            stop_angle = math.pi / 2 + ratio * 2 * math.pi
            pygame.draw.arc(self.screen, arc_color, arc_rect, start_angle, stop_angle, 6)

        pygame.draw.circle(self.screen, (50, 80, 110), (cx, cy), radius, 2)

        text_surf = self.oxygen_font.render(str(oxygen), True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(cx, cy))
        self.screen.blit(text_surf, text_rect)

    def draw_pearl_counter(self):
        """Draws a pearl counter in the top-right corner showing how many pearls the player has collected out of 10."""
        padding = 10
        icon_w = 22
        icon_h = 29

        count_text = f"{self.player.pearls} / 10"
        text_surf = self.pearl_font.render(count_text, True, (255, 240, 200))
        text_w = text_surf.get_width()
        text_h = text_surf.get_height()

        row_h = max(icon_h, text_h)
        total_w = icon_w + 8 + text_w + padding * 2
        total_h = row_h + padding * 2

        x = self.SCREEN_WIDTH - total_w - 10
        y = 10

        # Draw a semi-transparent dark background pill so the counter is readable over any level background
        bg_surf = pygame.Surface((total_w, total_h), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (0, 15, 30, 185), bg_surf.get_rect(), border_radius=8)
        self.screen.blit(bg_surf, (x, y))
        pygame.draw.rect(self.screen, (0, 80, 120), pygame.Rect(x, y, total_w, total_h), 1, border_radius=8)

        # Centre the pearl icon vertically inside the pill
        icon_y = y + padding + (row_h - icon_h) // 2
        self.screen.blit(self._pearl_icon, (x + padding, icon_y))

        # Centre the text vertically and place it just to the right of the icon
        text_y = y + padding + (row_h - text_h) // 2
        self.screen.blit(text_surf, (x + padding + icon_w + 8, text_y))


class level1(level):

    def __init__(self, screen):
        """Sets up level 1 (The Beach) — loads the beach background and restricts play to below the sea surface."""
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/beach.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.player.top_boundary = SEA_LEVEL_Y
        self.shark_y_min = SEA_LEVEL_Y
        self.pearl_y_min = SEA_LEVEL_Y

    def handle_spawns(self):
        """Level 1 only has sharks and pearls — keeps things simple for the opening stage."""
        self.spawn_shark()
        self.spawn_pearl()

class level2(level):

    def __init__(self, screen):
        """Sets up level 2 (The Open Ocean) — loads the ocean background and adds a sea floor ceiling to the play area."""
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/ocean.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.player.bottom_boundary = SEA_FLOOR_Y
        self.shark_y_max = SEA_FLOOR_Y - 150
        self.jelly_y_max = SEA_FLOOR_Y - 40
        self.jelly_y_boundary = SEA_FLOOR_Y
        self.pearl_y_max = SEA_FLOOR_Y - 40

    def handle_spawns(self):
        """Level 2 introduces jellyfish on top of sharks — dodge both to collect pearls."""
        self.spawn_shark()
        self.spawn_jellyfish()
        self.spawn_pearl()

class level3(level):

    def __init__(self, screen):
        """Sets up level 3 (The Deep Cave) — loads the cave background and throws everything at the player."""
        super().__init__(screen)
        self.bg_img = pygame.image.load("assets/images/cave.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def handle_spawns(self):
        """Level 3 is the full gauntlet — sharks, jellyfish, ocean currents, and pearls all at once."""
        self.spawn_shark()
        self.spawn_jellyfish()
        self.spawn_current()
        self.spawn_pearl()
