from jugadores import Jugador
from enum import Enum
import numpy as np

#Clases para las guardar las direcciones de cada jugador.
class Direction_j1(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    UP_RIGHT = 5
    UP_LEFT = 5
    DOWN_RIGHT = 5
    DOWN_LEFT = 5

class Jugador1(Jugador):
    def __init__(self, icono, grid_size,moves, time_left):
        # Llamar al constructor de la clase base
        super().__init__(icono, grid_size, moves, time_left) 


    #Movimientos jugador1
    def move_up(self):
        # Verificar si el jugador puede moverse hacia arriba
        if self.pos[0] > 0:
            if (self.pos[0] - 1, self.pos[1]) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia arriba si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0] - 1, self.pos[1])
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1

    def move_down(self):
        # Verificar si el jugador puede moverse hacia abajo
        if self.pos[0] < self.grid_size - 1:
            if (self.pos[0] + 1, self.pos[1]) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia abajo si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0] + 1, self.pos[1])
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1

    def move_left(self):
        # Verificar si el jugador puede moverse hacia la izquierda
        if self.pos[1] > 0:
            if (self.pos[0], self.pos[1] - 1) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia la izquierda si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0], self.pos[1] - 1)
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1

    def move_right(self):
        # Verificar si el jugador puede moverse hacia la derecha
        if self.pos[1] < self.grid_size - 1:
            if (self.pos[0], self.pos[1] + 1) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia la derecha si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0], self.pos[1] + 1)
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1
    
    def move_up_right(self):
        # Verificar si el jugador puede moverse hacia la derecha y hacia arriba
        if self.pos[1] < self.grid_size - 1 and self.pos[0] > 0:
            if (self.pos[0] - 1, self.pos[1] + 1) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia la derecha si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0] - 1, self.pos[1] + 1)
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1

    def move_up_left(self):
        # Verificar si el jugador puede moverse hacia la izquierda y arriba
        if self.pos[1] > 0  and self.pos[0] > 0:
            if (self.pos[0] - 1, self.pos[1] - 1) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia la derecha si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0] - 1, self.pos[1] - 1)
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1

    def move_down_right(self):
        # Verificar si el jugador puede moverse hacia la derecha y abajo
        if self.pos[1] < self.grid_size - 1 and self.pos[0] < self.grid_size - 1:
            if (self.pos[0] + 1, self.pos[1] + 1) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia la derecha si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0] + 1, self.pos[1] + 1)
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1

    def move_down_left(self):
        # Verificar si el jugador puede moverse hacia la izquierda y abajo
        if self.pos[1] > 0 and self.pos[0] < self.grid_size - 1:
            if (self.pos[0] + 1, self.pos[1] - 1) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia la derecha si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0] + 1, self.pos[1] - 1)
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1

    def _move_j1(self,action):
            directions = {0: Direction_j1.RIGHT, 1: Direction_j1.LEFT, 2: Direction_j1.UP,
                3: Direction_j1.DOWN, 4: Direction_j1.UP_RIGHT, 5: Direction_j1.UP_LEFT,
                6: Direction_j1.DOWN_RIGHT, 7: Direction_j1.DOWN_LEFT}

            new_dir = directions[np.argmax(action)]  # Esto te dará la dirección correspondiente a la acción
            self.direction = new_dir
            if self.direction == Direction_j1.RIGHT:
                self.move_right()
            elif self.direction == Direction_j1.LEFT:
                self.move_left()
            elif self.direction == Direction_j1.UP:
                self.move_up()
            elif self.direction == Direction_j1.DOWN:
                self.move_down()
            elif self.direction == Direction_j1.UP_RIGHT:
                self.move_up_right()
            elif self.direction == Direction_j1.UP_LEFT:
                self.move_up_left()
            elif self.direction == Direction_j1.DOWN_RIGHT:
                self.move_down_right()
            elif self.direction == Direction_j1.DOWN_LEFT:
                self.move_down_left()