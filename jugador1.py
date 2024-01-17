from jugadores import Jugador
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