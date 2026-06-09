"""
Authors: Dinesh Sinnathamby and Dhani Shah
Date: May 29th, 2026
Description: This is the main file for Pearl Panic, an underwater arcade survival game where players dodge marine hazards and manage a depleting oxygen tank to retrieve lost pearls across evolving ocean depths.
"""

import pygame
import sys
from data import DataHandler
import levels

class Main:

    SCREEN_WIDTH = 680
    SCREEN_HEIGHT = 480

    def __init__(self):
        """Boots up pygame, creates the window, and runs the main game loop until the player closes the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pearl Panic")
        self.clock = pygame.time.Clock()
        self.data_handler = DataHandler()

        # Keep cycling through the menu and game sessions until the player decides to quit
        while True:
            chosen_level = self.show_intro()
            self.data_handler.save_current_level(chosen_level)

            # If start_game returns False it means the window was closed, so we exit cleanly
            if not self.start_game():
                break

        pygame.quit()
        sys.exit()

    def create_button(self, text, y_position, locked=False):
        """Draws a menu button at the given vertical position and returns its rect for click detection. Locked buttons are greyed out."""
        button_width, button_height = 200, 50
        x_position = 268

        button_rect = pygame.Rect(x_position, y_position, button_width, button_height)

        # Use a darker, muted colour scheme for locked levels so the player knows they can't click them
        bg_color = (15, 15, 20) if locked else (0, 21, 35)
        text_color = (60, 70, 75) if locked else (0, 141, 187)

        pygame.draw.rect(self.screen, bg_color, button_rect, border_radius=8)

        font = pygame.font.Font("assets/fonts/paladins.ttf", 25)
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.screen.blit(text_surf, text_rect)

        return button_rect

    def show_intro(self):
        """Shows the main menu screen with level select buttons and waits for the player to pick a level."""
        intro_img = pygame.image.load("assets/images/intro.png").convert()
        intro_img = pygame.transform.scale(intro_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.load_music()

        waiting = True
        selected_level = 1
        max_unlocked = self.data_handler.get_max_unlocked()

        # Stay on the intro screen until the player clicks a valid level button
        while waiting:
            self.screen.blit(intro_img, (0, 0))

            blvl1 = self.create_button("Level 1", 200)
            blvl2 = self.create_button("Level 2", 270, locked=(max_unlocked < 2))
            blvl3 = self.create_button("Level 3", 340, locked=(max_unlocked < 3))

            # Process all events that happened since the last frame
            for event in pygame.event.get():
                # The player clicked the window's close button — exit immediately
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check if any level button was clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if blvl1.collidepoint(mouse_pos):
                        # Level 1 is always accessible
                        waiting = False
                        selected_level = 1

                    elif blvl2.collidepoint(mouse_pos) and max_unlocked >= 2:
                        # Level 2 only responds to clicks if the player has unlocked it
                        waiting = False
                        selected_level = 2

                    elif blvl3.collidepoint(mouse_pos) and max_unlocked >= 3:
                        # Level 3 only responds to clicks if the player has unlocked it
                        waiting = False
                        selected_level = 3

            pygame.display.flip()
            self.clock.tick(60)

        return selected_level

    def start_game(self):
        """Loads and runs the appropriate level, then handles what happens when the player wins, dies, or escapes to the menu."""
        current_lvl = self.data_handler.get_saved_level()

        # Pick which level class to instantiate based on the saved level number
        if current_lvl == 1:
            show_level = levels.level1(self.screen)
        elif current_lvl == 2:
            show_level = levels.level2(self.screen)
        else:
            show_level = levels.level3(self.screen)

        # Keep running the level until something ends it — a win, a death, or the player pressing Escape
        while True:
            dt = self.clock.tick(60) / 1000.0

            # Handle window and keyboard events each frame
            for event in pygame.event.get():
                # The player closed the window — tell the caller to shut down
                if event.type == pygame.QUIT:
                    return False
                # Escape sends the player back to the main menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return True

            show_level.update(dt)
            show_level.draw()

            # Check if the player has collected all 10 pearls — that's the win condition
            if show_level.player.pearls >= 10:
                # If this wasn't the last level, unlock the next one
                if current_lvl < 3:
                    next_level = current_lvl + 1
                    # Only update the max unlocked record if this is actually a new achievement
                    if next_level > self.data_handler.get_max_unlocked():
                        self.data_handler.save_max_unlocked(next_level)

                # Completing level 3 triggers the full end screen instead of the normal win screen
                if current_lvl == 3:
                    self.show_end_screen()
                else:
                    self.show_game_over(win=True)

                return True

            # If the player's oxygen hit zero, they lose — show the game over screen
            if show_level.player.oxygen <= 0:
                self.show_game_over(win=False)
                return True

            pygame.display.flip()

    def show_game_over(self, win):
        """Shows the win or lose screen with an appropriate message and waits for the player to return to the main menu."""
        waiting = True
        font = pygame.font.Font("assets/fonts/paladins.ttf", 40)
        sub_font = pygame.font.Font("assets/fonts/retroica.ttf", 20)

        # Set up different colours and messages depending on whether the player won or lost
        if win:
            bg_color = (0, 45, 35)
            title_text = "VICTORY ACHIEVED"
            title_color = (0, 255, 150)
        else:
            bg_color = (45, 5, 10)
            title_text = "OXYGEN AT ZERO"
            title_color = (255, 50, 50)

        # Stay on this screen until the player clicks the main menu button
        while waiting:
            self.screen.fill(bg_color)

            title_surf = font.render(title_text, True, title_color)
            title_rect = title_surf.get_rect(center=(self.SCREEN_WIDTH // 2, 180))
            self.screen.blit(title_surf, title_rect)
            btn_rect = self.create_button("MAIN MENU", 280)

            # Handle all events while we wait on this screen
            for event in pygame.event.get():
                # Window closed — exit the whole game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # The player clicked the main menu button — leave this screen
                    if btn_rect.collidepoint(mouse_pos):
                        waiting = False

            pygame.display.flip()
            self.clock.tick(60)

    def show_end_screen(self):
        """Shows the full game completion screen with a recap of all three levels after beating level 3."""
        waiting = True
        title_font = pygame.font.Font("assets/fonts/paladins.ttf", 38)
        heading_font = pygame.font.Font("assets/fonts/paladins.ttf", 22)
        body_font = pygame.font.Font("assets/fonts/retroica.ttf", 16)

        lines = [
            ("YOU COLLECTED ALL 10 PEARLS", heading_font, (255, 220, 80)),
            ("", body_font, (255, 255, 255)),
            ("Level 1 - The Beach", heading_font, (100, 220, 255)),
            ("You dodged sharks to gather pearls", body_font, (200, 240, 255)),
            ("and learned how to dash past danger.", body_font, (200, 240, 255)),
            ("", body_font, (255, 255, 255)),
            ("Level 2 - The Open Ocean", heading_font, (100, 220, 255)),
            ("Jellyfish slowed you down, but you", body_font, (200, 240, 255)),
            ("pushed through and kept diving deeper.", body_font, (200, 240, 255)),
            ("", body_font, (255, 255, 255)),
            ("Level 3 - The Deep Cave", heading_font, (100, 220, 255)),
            ("Ocean currents swept you aside, sharks", body_font, (200, 240, 255)),
            ("and jellyfish blocked your path — but", body_font, (200, 240, 255)),
            ("your bubble shield kept you safe.", body_font, (200, 240, 255)),
        ]

        # Stay on the end screen until the player clicks the main menu button
        while waiting:
            self.screen.fill((0, 10, 30))

            title_surf = title_font.render("GAME COMPLETE!", True, (0, 255, 180))
            title_rect = title_surf.get_rect(center=(self.SCREEN_WIDTH // 2, 40))
            self.screen.blit(title_surf, title_rect)

            y = 85

            # Render each line of the recap, skipping blank entries with a small gap instead
            for text, font, color in lines:
                if text == "":
                    # Empty string means we just want a bit of breathing room between sections
                    y += 6
                    continue

                surf = font.render(text, True, color)
                rect = surf.get_rect(center=(self.SCREEN_WIDTH // 2, y))
                self.screen.blit(surf, rect)
                y += surf.get_height() + 4

            btn_rect = self.create_button("MAIN MENU", 420)

            # Handle all events while on the end screen
            for event in pygame.event.get():
                # Window closed — exit the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # The player clicked the main menu button — we're done here
                    if btn_rect.collidepoint(pygame.mouse.get_pos()):
                        waiting = False

            pygame.display.flip()
            self.clock.tick(60)

    def load_music(self):
        """Tries to load and loop the background music — silently does nothing if the file isn't found."""
        try:
            pygame.mixer.music.load("assets/sound/music/coral_chorus.mp3")
            pygame.mixer.music.play(-1)
        except Exception:
            # Music is nice but not essential — don't crash if it's missing
            pass

Main()
