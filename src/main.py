
import pygame
import sys
import os

class Main:
    SCREEN_WIDTH = 680
    SCREEN_HEIGHT = 480

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pearl Panic")
        self.clock = pygame.time.Clock()
        self.show_intro()
        
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
        intro_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "intro.png")
        intro_img = pygame.image.load(intro_path).convert()
        intro_img = pygame.transform.scale(intro_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        if not pygame.mixer.music.get_busy():
            self.load_music()

        waiting = True
        while waiting:
            self.screen.blit(intro_img, (0, 0))
            
            start_rect = self.create_button("Level 1", 200)
            options_rect = self.create_button("Level 2", 270)
            quit_rect = self.create_button("Level 3", 340)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if start_rect.collidepoint(mouse_pos):
                        #level 1 button logic
                        waiting = False
                        
                    elif options_rect.collidepoint(mouse_pos):
                        # level 2 button logic
                        waiting = False
                        
                    elif quit_rect.collidepoint(mouse_pos):
                        # level 3 button logic
                        waiting = False

            pygame.display.flip()
            self.clock.tick(60)
            
    def load_music(self):
        try:
            pygame.mixer.music.load("assets/sound/music/coral_chorus.mp3")
            pygame.mixer.music.play(-1)
        except Exception:
            pass

Main()
