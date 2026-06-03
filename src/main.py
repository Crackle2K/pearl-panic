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
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pearl Panic")
        self.clock = pygame.time.Clock()
        self.data_handler = DataHandler()

        while True:
            chosen_level = self.show_intro()
            self.data_handler.save_current_level(chosen_level)
            if not self.start_game():
                break
        pygame.quit()
        sys.exit()
        
    def create_button(self, text, y_position):
        button_width, button_height = 200, 50
        x_position = 268
        
        button_rect = pygame.Rect(x_position, y_position, button_width, button_height)
        
        pygame.draw.rect(self.screen, (0, 21, 35), button_rect, border_radius=8)
        
        font = pygame.font.Font("assets/fonts/paladins.ttf", 25)
        text_surf = font.render(text, True, (0, 141, 187))
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.screen.blit(text_surf, text_rect)
        
        return button_rect

    def show_intro(self):
        intro_img = pygame.image.load("assets/images/intro.png").convert()
        intro_img = pygame.transform.scale(intro_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.load_music()

        waiting = True
        selected_level = 1

        while waiting:
            self.screen.blit(intro_img, (0, 0))
            
            blvl1 = self.create_button("Level 1", 200)
            blvl2 = self.create_button("Level 2", 270)
            blvl3 = self.create_button("Level 3", 340)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if blvl1.collidepoint(mouse_pos):
                        waiting = False
                        selected_level = 1
                        
                    elif blvl2.collidepoint(mouse_pos):
                        waiting = False
                        selected_level = 2

                    elif blvl3.collidepoint(mouse_pos):
                        waiting = False
                        selected_level = 3

            pygame.display.flip()
            self.clock.tick(60)
            
        return selected_level
    
    def start_game(self):
        current_lvl = self.data_handler.get_saved_level()
        if current_lvl == 1:
            show_level = levels.level1(self.screen)
        elif current_lvl == 2:
            show_level = levels.level2(self.screen)
        else:
            show_level = levels.level3(self.screen)

        while True:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return True

            show_level.update(dt)
            show_level.draw()
            pygame.display.flip()
        
    def load_music(self):
        try:
            pygame.mixer.music.load("assets/sound/music/coral_chorus.mp3")
            pygame.mixer.music.play(-1)
        except Exception:
            pass

Main()
