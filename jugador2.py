from jugadores import Jugador

class Jugador2(Jugador):
    def __init__(self, icono, grid_size,moves, time_left):
        # Llamar al constructor de la clase base
        super().__init__(icono, grid_size, moves, time_left)

        #Movimientos jugador2
    def move_up(self):
        # Verificar si el jugador puede moverse hacia arriba
        if self.pos[0] > 0:
            # Determinar la cantidad de celdas a moverse
            if self.moves % 2 != 1 and self.pos[0] >= 2 and (self.pos[0] - 2, self.pos[1]) not in [(1, 1), (3, 3)]:
                # Moverse dos celdas hacia arriba si se cumplen ciertas condiciones
                self.pos = (self.pos[0] - 2, self.pos[1])
            elif (self.pos[0] - 1, self.pos[1]) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia arriba si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0] - 1, self.pos[1])
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1

    def move_down(self):
        # Verificar si el jugador puede moverse hacia abajo
        if self.pos[0] < self.grid_size - 1:
            # Determinar la cantidad de celdas a moverse
            if self.moves % 2 != 1 and self.pos[0] <= 2 and (self.pos[0] + 2, self.pos[1]) not in [(1, 1), (3, 3)]:
                # Moverse dos celdas hacia abajo si se cumplen ciertas condiciones
                self.pos = (self.pos[0] + 2, self.pos[1])
            elif (self.pos[0] + 1, self.pos[1]) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia abajo si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0] + 1, self.pos[1])
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1

    def move_left(self):
        # Verificar si el jugador puede moverse hacia la izquierda
        if self.pos[1] > 0:
            # Determinar la cantidad de celdas a moverse
            if self.moves % 2 != 1 and self.pos[1] >= 2 and (self.pos[0], self.pos[1] - 2) not in [(1, 1), (3, 3)]:
                # Moverse dos celdas hacia la izquierda si se cumplen ciertas condiciones
                self.pos = (self.pos[0], self.pos[1] - 2)
            elif (self.pos[0], self.pos[1] - 1) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia la izquierda si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0], self.pos[1] - 1)
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1

    def move_right(self):
        # Verificar si el jugador puede moverse hacia la derecha
        if self.pos[1] < self.grid_size - 1:
            # Determinar la cantidad de celdas a moverse
            if self.moves % 2 != 1 and self.pos[1] <= 2 and (self.pos[0], self.pos[1] + 2) not in [(1, 1), (3, 3)]:
                # Moverse dos celdas hacia la derecha si se cumplen ciertas condiciones
                self.pos = (self.pos[0], self.pos[1] + 2)
            elif (self.pos[0], self.pos[1] + 1) not in [(1, 1), (3, 3)]:
                # Moverse una celda hacia la derecha si no se cumplen las condiciones anteriores
                self.pos = (self.pos[0], self.pos[1] + 1)
            self.has_moved = True
            self.frame_iteration += 1
            self.moves -= 1
