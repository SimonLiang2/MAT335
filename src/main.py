import pygame
from settings import *
import sys
from state_manager import StateManager
from Menu import MainMenuState
from SimulationState import SimulationState

def main():
    pygame.init()
    screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Onions May Cry")
    clock = pygame.time.Clock()
    state_manager = StateManager()
    
    state_manager.add_state('menu', MainMenuState('menu', state_manager))
    state_manager.add_state('Simulation', SimulationState('Simulation',state_manager))
    state_manager.transition('menu')
    
    while not state_manager.window_should_close:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                state_manager.quit()
        state_manager.update(events)
        state_manager.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()