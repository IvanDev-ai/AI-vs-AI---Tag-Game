# Definir constantes de colores
RED = (168, 38, 38)
GREEN = (35, 148, 40)
DARKGREEN = (36, 75, 46)

class Map:
    def __init__(self, grid_size, cell_size, margin):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.margin = margin

    def draw_grid_and_players(self, jugador1, jugador2):
        html_content = '<div style="display: grid; grid-template-columns: repeat(' + str(self.grid_size) + ', ' + str(self.cell_size) + 'px);">'
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) == jugador1.pos:
                    # Dibujar jugador1 con esquinas redondeadas y color de fondo carne
                    html_content += f'<div style="width:{self.cell_size}px;height:{self.cell_size}px;border: 1px solid black;background-color:#FFCC99;border-radius: 5px;">{jugador1.icono}</div>'
                elif (row, col) == jugador2.pos:
                    # Dibujar jugador2 con esquinas redondeadas y color de fondo azul oscuro
                    html_content += f'<div style="width:{self.cell_size}px;height:{self.cell_size}px;border: 1px solid black;background-color:#FFCC99;border-radius: 5px;">{jugador2.icono}</div>'
                else:
                    if (row, col) not in [(1, 1), (3, 3)]:
                        # Agregar una celda normal con esquinas redondeadas
                        html_content += f'<div style="width:{self.cell_size}px;height:{self.cell_size}px;border: 1px solid black;background-color:#FFCC99;border-radius: 5px;"></div>'
                    else:
                        # Agregar una celda especial con esquinas redondeadas y color de fondo azul oscuro
                        html_content += f'<div style="width:{self.cell_size}px;height:{self.cell_size}px;background-color:#2E4053;border-radius: 5px;"></div>'
        html_content += '</div>'
        return html_content


    def draw_counters(self, player2):
        # Dibujar contadores de jugador 2
        html_content = ""
        html_content += f"Movimientos: {player2.moves}\n"
        html_content += f"Tiempo: 0:{'0' + str(player2.time_left) if player2.time_left < 10 else player2.time_left}"
        return html_content

    def draw_circle(self, jugador2):
        # Dibujar el círculo que cambia de color
        circle_color = "red" if jugador2.moves % 2 == 1 else "green"
        html_content = f'<div style="display:inline-block;width:24px;height:24px;border-radius:50%;background-color:{circle_color};"></div>'
        return html_content
