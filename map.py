import pygame
# Colores
RED = (168, 38, 38)
GREEN = (35, 148, 40)
DARKGREEN = (36, 75, 46)

class Map:
    def __init__(self, screen, grid_size, cell_size, margin):
        self.screen = screen
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.margin = margin

    def draw_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = pygame.Rect(col * (self.cell_size + self.margin), row * (self.cell_size + self.margin), self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                
                # Dibujar cuadrículas negras en (1, 1) y (3, 3)
                if (row, col) in [(1, 1), (3, 3)]:
                    pygame.draw.rect(self.screen, DARKGREEN, rect)


    def draw_players(self, jugador1, jugador2):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) == jugador1.pos:  # Dibujar al jugador 1
                    font = pygame.font.Font(None, 36)
                    text_surface = font.render(jugador1.icono, True, RED)
                    self.screen.blit(text_surface, (col * (self.cell_size + self.margin) + 10, row * (self.cell_size + self.margin) + 5))
                elif (row, col) == jugador2.pos:  # Dibujar al jugador 2
                    font = pygame.font.Font(None, 36)
                    text_surface = font.render(jugador2.icono, True, GREEN)
                    self.screen.blit(text_surface, (col * (self.cell_size + self.margin) + 10, row * (self.cell_size + self.margin) + 5))

    def draw_counters(self, player2):
        font = pygame.font.Font(None, 24)
        moves_text = font.render(f"Movimientos: {player2.moves}", True, (0, 0, 0))
        time_text = font.render(f"Tiempo: 0:{'0' + str(player2.time_left) if player2.time_left < 10 else player2.time_left}", True, (0, 0, 0))
        self.screen.blit(moves_text, (10, self.screen.get_height() - 40))
        self.screen.blit(time_text, (10, self.screen.get_height() - 20))
    
    def draw_circle(self, jugador2):
        circle_color = RED if jugador2.moves % 2 == 1 else GREEN
        pygame.draw.circle(self.screen, circle_color, (self.screen.get_width() - 40, 30), 12)
