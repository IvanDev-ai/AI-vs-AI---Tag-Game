import torch
import random
import numpy as np
from jugador2 import Direction_j2
from collections import deque
from model import Linear_QNet, QTrainer


MAX_MEMORY = 100_000  # Tamaño máximo de la memoria de replay
BATCH_SIZE = 1000  # Tamaño del lote para el entrenamiento
LR = 0.001  # Tasa de aprendizaje

class Agent2:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # Factor de aleatoriedad
        self.gamma = 0.9  # Tasa de descuento
        self.memory = deque(maxlen=MAX_MEMORY)  # Memoria de replay (cola de tamaño limitado)
        self.model = Linear_QNet(8, 256, 4)  # Inicialización del modelo Q-network
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)  # Inicialización del entrenador Q


    def get_state(self,game):
        
        dir_l = game.jugador2.direction == Direction_j2.LEFT
        dir_r = game.jugador2.direction == Direction_j2.RIGHT
        dir_u = game.jugador2.direction == Direction_j2.UP
        dir_d = game.jugador2.direction == Direction_j2.DOWN

        state = [
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # J1 location 
            game.jugador1.get_current_cell()[1] < game.jugador2.get_current_cell()[1],  # J1 left
            game.jugador1.get_current_cell()[1] > game.jugador2.get_current_cell()[1],  # J1 right
            game.jugador1.get_current_cell()[0] < game.jugador2.get_current_cell()[0],  # J1 up
            game.jugador1.get_current_cell()[0] > game.jugador2.get_current_cell()[0]  # J1 down
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward_j2, next_state, done):
    # Almacena la experiencia en la memoria del agente
        self.memory.append((state, action, reward_j2, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            # Muestreo aleatorio de BATCH_SIZE experiencias de la memoria
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            # Si la memoria es menor que BATCH_SIZE, toma toda la memoria como muestra
            mini_sample = self.memory
        
        # Desempaqueta las muestras en listas separadas
        states, actions, reward_j2s, next_states, dones = zip(*mini_sample)
        
        # Entrena el modelo usando las muestras
        self.trainer.train_step(states, actions, reward_j2s, next_states, dones)

    def train_short_memory(self,state,action,reward_j2,next_state,done):
        # Entrena el modelo con una única experiencia
        self.trainer.train_step(state,action,reward_j2,next_state,done)

    def get_action(self, state):
        # Actualiza el valor de epsilon basado en el número de juegos jugados
        self.epsilon = 80 - self.n_games
        
        # Inicializa una lista para representar la acción final
        final_move = [0, 0, 0, 0]
        
        # Exploración: elige una acción al azar si el valor aleatorio es menor que epsilon
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            # Explotación: elige la acción con la predicción más alta según el modelo
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        # Devuelve la acción final como lista one-hot
        return final_move
    


