import pygame
import math
from collections import deque

class SimulationState:
    def __init__(self, name, state_machine):
        self.name = name
        self.state_machine = state_machine
        
        self.a = 0.2
        self.b = 0.2
        self.c = 5.7
        
        self.x, self.y, self.z = 0.1, 0.0, 0.0
        
        self.dt = 0.035  
        
        self.max_trail = 2500
        self.points_3d = deque(maxlen=self.max_trail)
        
        self.scale = 18
        self.angle_x = 0.6  # Initial tilt
        self.angle_y = 0.0  # Initial rotation
        
        # UI Font
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)

    def enter(self):
        # Reset the simulation variables when entering 
        self.x, self.y, self.z = 0.1, 0.0, 0.0
        self.points_3d.clear()

    def leave(self):
        pass

    def update(self, events):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_e]: self.a += 0.002
        if keys[pygame.K_q]: self.a -= 0.002
        
        if keys[pygame.K_d]: self.b += 0.002
        if keys[pygame.K_a]: self.b -= 0.002
        
        if keys[pygame.K_c]: self.c += 0.02
        if keys[pygame.K_z]: self.c -= 0.02
        
        if keys[pygame.K_LEFT]: self.angle_y -= 0.03
        if keys[pygame.K_RIGHT]: self.angle_y += 0.03
        if keys[pygame.K_UP]: self.angle_x -= 0.03
        if keys[pygame.K_DOWN]: self.angle_x += 0.03

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Transition back to the Main Menu 
                self.state_machine.transition('menu')

        for _ in range(8):
            dx = -self.y - self.z
            dy = self.x + self.a * self.y
            dz = self.b + self.z * (self.x - self.c)

            # Apply Euler's method for numerical integration
            self.x += dx * self.dt
            self.y += dy * self.dt
            self.z += dz * self.dt
            
            if math.isnan(self.x) or math.isinf(self.x) or abs(self.x) > 10000:
                self.x, self.y, self.z = 0.1, 0.0, 0.0
                self.points_3d.clear()
                break

            self.points_3d.append((self.x, self.y, self.z))

    def draw(self, surface):
        surface.fill((15, 15, 20))
        
        width, height = surface.get_size()
        cx, cy = width // 2, height // 2

        projected_points = []
        for px, py, pz in self.points_3d:

            x1 = px * math.cos(self.angle_y) - pz * math.sin(self.angle_y)
            z1 = px * math.sin(self.angle_y) + pz * math.cos(self.angle_y)
            
            
            y2 = py * math.cos(self.angle_x) - z1 * math.sin(self.angle_x)
            
            # Map to 2D screen coordinates
            screen_x = cx + int(x1 * self.scale)
            screen_y = cy + int(y2 * self.scale)
            
            projected_points.append((screen_x, screen_y))


        if len(projected_points) > 1:
            pygame.draw.lines(surface, (100, 200, 255), False, projected_points, 1)


        ui_elements = [
            "Rössler Attractor",
            "-------------------",
            f"Constant a: {self.a:.3f}   [Q/E to adjust]",
            f"Constant b: {self.b:.3f}   [A/D to adjust]",
            f"Constant c: {self.c:.3f}   [Z/C to adjust]",
            "",
            "Camera: Arrow Keys to Rotate",
            "Warning: Certain values paired with",
            "others may cause instability",
            "Back: ESC"
        ]
        
        for i, text in enumerate(ui_elements):
            rendered_text = self.font.render(text, True, (220, 220, 220))
            surface.blit(rendered_text, (20, 20 + i * 25))