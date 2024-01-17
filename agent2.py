import torch
import random
import numpy as np
from game import Direction_j2
from collections import deque
from model import Linear_QNet, QTrainer


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent2:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount rate
        self.memmory = deque(maxlen = MAX_MEMORY) #popleft()
        self.model = Linear_QNet(8,256,4)
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)


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

    def remember(self,state,action,reward_j2,next_state,done):
        self.memmory.append((state,action,reward_j2,next_state,done)) 

    def train_long_memory(self):
        if len(self.memmory) > BATCH_SIZE:
            mini_sample = random.sample(self.memmory,BATCH_SIZE)
        else:
            mini_sample = self.memmory
        
        states , actions , reward_j2s , next_states , dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,reward_j2s,next_states,dones)

    def train_short_memory(self,state,action,reward_j2,next_state,done):
        self.trainer.train_step(state,action,reward_j2,next_state,done)

    def get_action(self,state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state,dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
    

