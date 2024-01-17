import pygame
from jugador1 import Jugador1
from jugador2 import Jugador2
from map import Map
from enum import Enum
import numpy as np
# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width, screen_height = 300, 250
cell_size = 40  # Tamaño de cada celda
margin = 2  # Margen entre celdas
grid_size = 5  # Tamaño de la cuadrícula (5x5)

# Colores
WHITE = (255, 255, 255)

# Lógica para los contadores
move_timer = pygame.USEREVENT + 1
pygame.time.set_timer(move_timer, 1000)

class Direction_j1(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    UP_RIGHT = 5
    UP_LEFT = 5
    DOWN_RIGHT = 5
    DOWN_LEFT = 5

class Direction_j2(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Game:
    def __init__(self):
    # Crear la ventana
        self.display = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Escape Game")
        self.clock = pygame.time.Clock()
        self.reset()
        self.contador_J1 = 0
        self.contador_J2 = 0

    def reset(self):
    # Definir jugadores y sus representaciones usando las clases
        self.jugador1 = Jugador1('X', grid_size,10,3)
        self.jugador2 = Jugador2('O', grid_size,10,3)
        self.jugador1.reset()
        self.jugador2.reset()
        self.turno = True

    def play_step(self, actions):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == move_timer:
                self.jugador2.update_time_and_movements()
                self.jugador1.update_time_and_movements()

        if self.turno:
            self._move_j2(actions[0])
            self.turno = False
        elif not self.turno:
            self._move_j1(actions[1])
            self.turno = True
        
        self.updateUI()
        self.clock.tick(30)

        reward_j1 = 0
        reward_j2 = 0
        game_over = False
        if self.jugador1.moves <= 0 or self.jugador2.moves <= 0:
            game_over = True
            reward_j1 = -10
            reward_j2 = 10
            self.contador_J2 += 1
            print(f"El jugador 2 ha ganado")
        elif self.jugador1.pos == self.jugador2.pos:
            game_over = True
            reward_j1 = 10
            reward_j2 = -10
            self.contador_J1 += 1
            print("Ha ganado el jugador 1")
        
        return reward_j1,reward_j2,game_over

    def updateUI(self):
        self.display.fill(WHITE)  # Fondo blanco
        # Crear el mapa
        game_map = Map(self.display, grid_size, cell_size, margin)
        # Dibujar la cuadrícula y jugadores
        game_map.draw_grid()
        game_map.draw_players(self.jugador1,self.jugador2)

        # Dibujar un círculo que cambia de color
        game_map.draw_circle(self.jugador2)

        # Dibujar contadores
        game_map.draw_counters(self.jugador2)

        # Actualizar la pantalla
        pygame.display.flip()

    def _move_j1(self,action):
            directions = {0: Direction_j1.RIGHT, 1: Direction_j1.LEFT, 2: Direction_j1.UP,
                3: Direction_j1.DOWN, 4: Direction_j1.UP_RIGHT, 5: Direction_j1.UP_LEFT,
                6: Direction_j1.DOWN_RIGHT, 7: Direction_j1.DOWN_LEFT}

            new_dir = directions[np.argmax(action)]  # Esto te dará la dirección correspondiente a la acción
            self.jugador1.direction = new_dir
            if self.jugador1.direction == Direction_j1.RIGHT:
                self.jugador1.move_right()
            elif self.jugador1.direction == Direction_j1.LEFT:
                self.jugador1.move_left()
            elif self.jugador1.direction == Direction_j1.UP:
                self.jugador1.move_up()
            elif self.jugador1.direction == Direction_j1.DOWN:
                self.jugador1.move_down()
            elif self.jugador1.direction == Direction_j1.UP_RIGHT:
                self.jugador1.move_up_right()
            elif self.jugador1.direction == Direction_j1.UP_LEFT:
                self.jugador1.move_up_left()
            elif self.jugador1.direction == Direction_j1.DOWN_RIGHT:
                self.jugador1.move_down_right()
            elif self.jugador1.direction == Direction_j1.DOWN_LEFT:
                self.jugador1.move_down_left()


    def _move_j2(self,action):
            directions = {0: Direction_j2.RIGHT, 1: Direction_j2.LEFT, 2: Direction_j2.UP,
                3: Direction_j2.DOWN}
            new_dir = directions[np.argmax(action)]  # Esto te dará la dirección correspondiente a la acción
            self.jugador2.direction = new_dir
            if self.jugador2.direction == Direction_j2.RIGHT:
                self.jugador2.move_right()
            elif self.jugador2.direction == Direction_j2.LEFT:
                self.jugador2.move_left()
            elif self.jugador2.direction == Direction_j2.UP:
                self.jugador2.move_up()
            elif self.jugador2.direction == Direction_j2.DOWN:
                self.jugador2.move_down()
