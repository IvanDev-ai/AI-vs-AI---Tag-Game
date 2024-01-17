import torch
import random
import numpy as np
from game import Direction_j1,Game
from collections import deque
from model import Linear_QNet, QTrainer
from agent2 import Agent2

MAX_MEMORY = 100_000  # Tamaño máximo de la memoria de replay
BATCH_SIZE = 1000  # Tamaño del lote para el entrenamiento
LR = 0.001  # Tasa de aprendizaje

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # Factor de aleatoriedad
        self.gamma = 0.9  # Tasa de descuento
        self.memory = deque(maxlen=MAX_MEMORY)  # Memoria de replay (cola de tamaño limitado)
        self.model = Linear_QNet(12, 256, 8)  # Inicialización del modelo Q-network
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)  # Inicialización del entrenador Q


    def get_state(self,game):
        # Move direction
        dir_l = game.jugador1.direction == Direction_j1.LEFT
        dir_r = game.jugador1.direction == Direction_j1.RIGHT
        dir_u = game.jugador1.direction == Direction_j1.UP
        dir_d = game.jugador1.direction == Direction_j1.DOWN
        dir_ul = game.jugador1.direction == Direction_j1.UP_LEFT
        dir_ur = game.jugador1.direction == Direction_j1.UP_RIGHT
        dir_dl = game.jugador1.direction == Direction_j1.DOWN_LEFT
        dir_dr = game.jugador1.direction == Direction_j1.DOWN_RIGHT

        state = [
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            dir_ul,
            dir_ur,
            dir_dl,
            dir_dr,
            
            # J2 location 
            game.jugador2.get_current_cell()[1] < game.jugador1.get_current_cell()[1],  # J2 left
            game.jugador2.get_current_cell()[1] > game.jugador1.get_current_cell()[1],  # J2 right
            game.jugador2.get_current_cell()[0] < game.jugador1.get_current_cell()[0],  # J2 up
            game.jugador2.get_current_cell()[0] > game.jugador1.get_current_cell()[0]  # J2 down
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward_j1, next_state, done):
    # Almacena la experiencia en la memoria del agente
        self.memory.append((state, action, reward_j1, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            # Muestreo aleatorio de BATCH_SIZE experiencias de la memoria
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            # Si la memoria es menor que BATCH_SIZE, toma toda la memoria como muestra
            mini_sample = self.memory
        
        # Desempaqueta las muestras en listas separadas
        states, actions, reward_j1s, next_states, dones = zip(*mini_sample)
        
        # Entrena el modelo usando las muestras
        self.trainer.train_step(states, actions, reward_j1s, next_states, dones)

    def train_short_memory(self, state, action, reward_j1, next_state, done):
    # Entrena el modelo con una única experiencia
        self.trainer.train_step(state, action, reward_j1, next_state, done)

    def get_action(self, state):
        # Actualiza el valor de epsilon basado en el número de juegos jugados
        self.epsilon = 80 - self.n_games
        
        # Inicializa una lista para representar la acción final
        final_move = [0, 0, 0, 0, 0, 0, 0, 0]
        
        # Exploración: elige una acción al azar si el valor aleatorio es menor que epsilon
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 7)
            final_move[move] = 1
        else:
            # Explotación: elige la acción con la predicción más alta según el modelo
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        # Devuelve la acción final como lista one-hot
        return final_move


def load_agent_model(agent1,agent2, model_path1, model_path2):
    # Carga el modelo desde el archivo .pth
    modelo_guardado1 = torch.load(model_path1, map_location=torch.device('cpu'))  # Añade 'map_location=torch.device('cpu')' si es necesario

    # Crea una instancia del modelo (asegúrate de que la arquitectura coincida)
    agent1.model = Linear_QNet(12, 256, 8)  # Ajusta según la arquitectura de tu modelo
    agent1.model.load_state_dict(modelo_guardado1)

    # Configura el modelo en modo de evaluación (no entrenamiento)
    agent1.model.eval()

    # Carga el modelo desde el archivo .pth
    modelo_guardado2 = torch.load(model_path2, map_location=torch.device('cpu'))  # Añade 'map_location=torch.device('cpu')' si es necesario
    # Crea una instancia del modelo (asegúrate de que la arquitectura coincida)
    agent2.model = Linear_QNet(8, 256, 4)  # Ajusta según la arquitectura de tu modelo
    agent2.model.load_state_dict(modelo_guardado2)

    # Configura el modelo en modo de evaluación (no entrenamiento)
    agent2.model.eval()

# Importar las clases necesarias
def train():
    # Crear instancias de los agentes
    agent = Agent()
    agent2 = Agent2()

    # Cargar los modelos previamente entrenados para cada agente
    load_agent_model(agent, agent2, './model1/model1.pth', './model1/model2.pth')

    # Crear una instancia del juego
    game = Game()

    # Bucle principal del juego
    while True:
        # Obtener el estado actual del juego para cada agente
        state_old = agent.get_state(game)
        state_old2 = agent2.get_state(game)

        # Obtener la acción que cada agente toma en base al estado actual
        final_move = agent.get_action(state_old)
        final_move2 = agent2.get_action(state_old2)

        # Combinar las acciones de ambos agentes
        final_moves = [final_move2, final_move]

        # Realizar un paso en el juego y obtener las recompensas y el estado nuevo
        reward_j1, reward_j2, done = game.play_step(final_moves)
        state_new = agent.get_state(game)
        state_new2 = agent2.get_state(game)

        # Entrenar la memoria corta de cada agente con la información del paso actual
        agent.train_short_memory(state_old, final_move, reward_j1, state_new, done)
        agent2.train_short_memory(state_old2, final_move2, reward_j2, state_new2, done)

        # Recordar la información del paso actual en la memoria larga de cada agente
        agent.remember(state_old, final_move, reward_j1, state_new, done)
        agent2.remember(state_old2, final_move2, reward_j2, state_new2, done)

        # Verificar si el juego ha terminado
        if done:
            # Reiniciar el juego y contar el número de juegos jugados
            game.reset()
            agent.n_games += 1

            # Entrenar la memoria larga de cada agente al final de un juego
            agent.train_long_memory()
            agent2.train_long_memory()

            # Guardar modelos después de cierto número de juegos
            if agent.n_games == 1000:
                print("Ganadas J1:", game.contador_J1)
                print("Ganadas J2:", game.contador_J2)
                agent.model.save()
                agent2.model.save("model2.pth")

            # Imprimir el número del juego actual
            print("Game", agent.n_games)

            
            



if __name__ == "__main__":
    train()
