import torch
import random
import numpy as np
from game import Direction_j1,Game
from collections import deque
from model import Linear_QNet, QTrainer
from agent2 import Agent2

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount rate
        self.memmory = deque(maxlen = MAX_MEMORY) #popleft()
        self.model = Linear_QNet(12,256,8)
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)
        #TODO: model,trainer


    def get_state(self,game):
        
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

    def remember(self,state,action,reward_j1,next_state,done):
        self.memmory.append((state,action,reward_j1,next_state,done)) 

    def train_long_memory(self):
        if len(self.memmory) > BATCH_SIZE:
            mini_sample = random.sample(self.memmory,BATCH_SIZE)
        else:
            mini_sample = self.memmory
        
        states , actions , reward_j1s , next_states , dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,reward_j1s,next_states,dones)

    def train_short_memory(self,state,action,reward_j1,next_state,done):
        self.trainer.train_step(state,action,reward_j1,next_state,done)

    def get_action(self,state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0,0,0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,7)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state,dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

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

def train():
    agent = Agent()
    agent2 = Agent2()

    load_agent_model(agent,agent2, './model1/model1.pth','./model1/model2.pth')

    game = Game()
    while True:
        state_old = agent.get_state(game)
        state_old2 = agent2.get_state(game)

        final_move = agent.get_action(state_old)
        final_move2 = agent2.get_action(state_old2)

        final_moves = [final_move2,final_move]

        reward_j1,reward_j2,done = game.play_step(final_moves)
        state_new = agent.get_state(game)
        state_new2 = agent2.get_state(game)

        agent.train_short_memory(state_old,final_move,reward_j1,state_new,done)
        agent2.train_short_memory(state_old2,final_move2,reward_j2,state_new2,done)

        agent.remember(state_old,final_move,reward_j1,state_new,done)
        agent2.remember(state_old2,final_move2,reward_j2,state_new2,done)

        if done:
            #train long memory
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            agent2.train_long_memory()

            if agent.n_games == 1000:
                print("Ganadas J1:",game.contador_J1)
                print("Ganadas J2:",game.contador_J2)
                agent.model.save()
                agent2.model.save("model2.pth")
            
            print("Game",agent.n_games)
            
            



if __name__ == "__main__":
    train()
