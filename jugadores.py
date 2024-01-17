import random

class Jugador:
    def __init__(self, icono, grid_size,moves, time_left):
        self.icono = icono
        self.grid_size = grid_size
        self.pos = self.generate_position()
        self.cell = self.get_current_cell()
        self.moves = moves
        self.time_left = time_left
        self.init_time = time_left
        self.has_moved = False
        self.frame_iteration = 0
        self.direction = None

    #Funcion para obtener la celda actual donde se encuentra el jugador
    def get_current_cell(self):
        row = self.pos[0]
        col = self.pos[1]
        return (row,col)

    def update_time_and_movements(self):
        #comprobar si se ha movido
        if self.time_left > 0 and self.has_moved:
            self.time_left = self.init_time + 1

        # Descender el tiempo
        if self.time_left > 0:
            self.time_left -= 1

        # Restar un movimiento si el jugador no se ha movido
        if self.time_left <= 0 and not self.has_moved:
            self.time_left = self.init_time
            self.moves -= 1

        # Resetear la variable de movimiento
        self.has_moved = False

    #Funcion para generar una posicion inicial aleatoria dentro del tablero
    def generate_position(self):
        while True:
            pos = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if pos != (1, 1) and pos != (3, 3):  # Evitar las celdas negras
                return pos
    #Funcion que resetea las variables de cada jugador
    def reset(self):
        self.moves = 10
        self.time_left = 3
        self.init_time = self.time_left
        self.has_moved = False
        self.frame_iteration = 0
