import pygame
from settings import *
from button import Button

class MainMenuState:
    def __init__(self, name, state_machine):
        self.name = name
        self.state_machine = state_machine
        self.BASE_WIDTH = BASE_WIDTH
        self.BASE_HEIGHT = BASE_HEIGHT
        self.setup_ui()
        
    def setup_ui(self):
        surface = pygame.display.get_surface()
        if surface:
            self.screen_width, self.screen_height = surface.get_size()
        else:
            self.screen_width, self.screen_height = self.BASE_WIDTH, self.BASE_HEIGHT
            
        scale_x = self.screen_width / self.BASE_WIDTH
        scale_y = self.screen_height / self.BASE_HEIGHT
        
        scale = min(scale_x, scale_y)
        
        btn_width = int(200 * scale)
        btn_height = int(50 * scale)
        btn_spacing = int(70 * scale)
        font_size = max(int(36 * scale), 10)
        btn_font = pygame.font.SysFont(None, font_size)
        
        button_x = (self.screen_width // 2) - (btn_width // 2)
        button_y = (self.screen_height // 2) - int(100 * scale)
        self.start = Button(button_x, button_y, btn_width, btn_height, "Start", btn_font, BLACK, WHITE)
        self.quit = Button(button_x, button_y + btn_spacing * 3, btn_width, btn_height, "Quit", btn_font, RED, WHITE)
        
    def update(self, events):
        for event in events:
            if self.start.is_clicked(event):
                self.state_machine.transition('Simulation')
            elif self.quit.is_clicked(event):
                self.state_machine.quit()
            elif event.type == pygame.VIDEORESIZE:
                self.__init__(self.name, self.state_machine)  
                
    def draw(self, surface):
        surface.fill(DARK)
        title = pygame.font.Font(None, 74).render("Rössler Attractor Simulation", True, WHITE)
        surface.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        self.start.draw(surface)
        self.quit.draw(surface)
        
    def enter(self):
        self.__init__(self.name, self.state_machine)
        
                