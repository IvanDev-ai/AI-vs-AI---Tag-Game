import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # Definición de capa lineal 1 con input_size nodos de entrada y hidden_size nodos de salida
        self.linear1 = nn.Linear(input_size, hidden_size)
        # Definición de capa lineal 2 con hidden_size nodos de entrada y output_size nodos de salida
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Aplicar la función de activación ReLU a la salida de la capa lineal 1
        x = F.relu(self.linear1(x))
        # Capa lineal 2 sin función de activación adicional
        x = self.linear2(x)
        return x
    
    def save(self, file_name="model1.pth"):
        # Crear una carpeta para almacenar el modelo si no existe
        model_folder_path = "./model1"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        # Combinar la carpeta del modelo con el nombre de archivo para obtener la ruta completa
        file_name = os.path.join(model_folder_path, file_name)
        # Guardar los pesos del modelo en el archivo especificado
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        # Initialize the QTrainer with a model, learning rate (lr), and discount factor (gamma)
        self.lr = lr
        self.gamma = gamma
        self.model = model
        # Initialize the Adam optimizer with the model's parameters and the specified learning rate
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        # Define Mean Squared Error Loss as the criterion for training
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward_j1, next_state, done):
        # Convert inputs to PyTorch tensors with the appropriate data types
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward_j1, dtype=torch.float)

        # If the state is 1-dimensional, add a batch dimension
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: Predicted Q values with the current state
        pred = self.model(state)

        # Create a copy of predicted values to compute the target Q values
        target = pred.clone()
        for idx in range(len(done)):
            # Compute the new Q value based on whether the episode is done or not
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            # Update the target Q values with the new Q value for the chosen action
            target[idx][torch.argmax(action).item()] = Q_new

        # 2: Compute the loss using Mean Squared Error between predicted and target Q values
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        # Perform a gradient descent step to update the model's parameters
        self.optimizer.step()
