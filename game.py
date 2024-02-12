import pygame
from jugador1 import Jugador1
from jugador2 import Jugador2
from map import Map
import streamlit as st
# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width, screen_height = 300, 250
cell_size = 40  # Tamaño de cada celda
margin = 2  # Margen entre celdas
grid_size = 5  # Tamaño de la cuadrícula (5x5)

# Colores
WHITE = (245, 245, 220)

# Lógica para los contadores
move_timer = pygame.USEREVENT + 1
pygame.time.set_timer(move_timer, 1000)





#clase del juego principal que ejecuta la logica del juego
class Game:
    def __init__(self):
    # Crear la ventana, resetea y establece los contadores de ganadas por jugador
        self.display = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Escape Game")
        self.clock = pygame.time.Clock()
        self.reset()
        self.contador_J1 = 0
        self.contador_J2 = 0
        # Crear un contenedor vacío
        self.container = st.empty()
        self.container2 = st.empty()

    def reset(self):
    # Definir jugadores y sus representaciones usando las clases y resetea las variables de los jugadores
        self.jugador1 = Jugador1('😡', grid_size,10,3)
        self.jugador2 = Jugador2('😭', grid_size,10,3)
        self.jugador1.reset()
        self.jugador2.reset()
        self.turno = True
# Funcion que sirve para la logica del juego, recibe una tupla de acciones y devuelve las recompensas.
    def play_step(self, actions):
        # Actualizar tiempo y movimientos
        self.jugador2.update_time_and_movements()
        self.jugador1.update_time_and_movements()

        # Mover jugadores según el turno
        if self.turno:
            self.jugador2._move_j2(actions[0])
            self.turno = False
        else:
            self.jugador1._move_j1(actions[1])
            self.turno = True

        # Llamar a updateUI para reflejar los cambios en la interfaz
        self.updateUI()
        
        # Comprobar condiciones de finalización del juego
        reward_j1, reward_j2, game_over = self.check_game_over()

        
        return reward_j1, reward_j2, game_over

    def check_game_over(self):
        reward_j1, reward_j2, game_over = 0, 0, False
        if self.jugador1.moves <= 0 or self.jugador2.moves <= 0:
            game_over = True
            reward_j1 = -10
            reward_j2 = 10
            self.container2.write("El jugador 2 ha ganado." if self.jugador1.moves <= 0 else "El jugador 1 ha ganado.")
        elif self.jugador1.pos == self.jugador2.pos:
            game_over = True
            reward_j1 = 10
            reward_j2 = -10
            self.container2.write("El jugador 1 ha ganado.")
        return reward_j1, reward_j2, game_over


    def updateUI(self):
        # Crear el mapa
        game_map = Map(grid_size, cell_size, margin)

        # Obtener el contenido HTML de la cuadrícula y jugadores
        grid_and_players_content = game_map.draw_grid_and_players(self.jugador1, self.jugador2)
        # Insertar el contenido en el contenedor
        self.container.write(grid_and_players_content, unsafe_allow_html=True)
