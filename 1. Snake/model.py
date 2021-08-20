import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
#https://www.youtube.com/watch?v=VGkcmBaeAGM

class LinearQNet(nn.Module):
    def __init__(self, inputSize, hiddenSize, outputSize):
        super().__init__()
        self.linear1 = nn.Linear(inputSize, hiddenSize)
        self.linear2 = nn.Linear(hiddenSize, outputSize)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, fileName='model.pth'):
        modelFolderPath = './model'
        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)

        fileName = os.path.join(modelFolderPath, fileName)
        torch.save(self.state_dict(), fileName)



class QTrainer:

    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model

        self.optimiser = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def trainStep(self, state, move, reward, nextState, gameOver):
        state = torch.tensor(state, dtype=torch.float)
        nextState = torch.tensor(nextState, dtype=torch.float)
        move = torch.tensor(move, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        #we dont need gameover as a tensor value

        if len(state.shape) == 1:
            #reshape
            state = torch.unsqueeze(state, 0)
            nextState = torch.unsqueeze(nextState, 0)
            move = torch.unsqueeze(move, 0)
            reward = torch.unsqueeze(reward, 0)
            gameOver = (gameOver, )


        #predicted Q with state
        pred = self.model(state)########################################################################

        target = pred.clone()#pred.clone()
        for idx in range(len(gameOver)):
            QNew = reward[idx]
            if not gameOver[idx]:
                QNew = reward[idx] + self.gamma * torch.max(self.model(nextState[idx])) #apply new Q formula r+y*max(nextpred Q)

            target[idx][torch.argmax(move).item()] = QNew#predictions[argmax(move)] = our new Q pred

        #apply new Q formula r+y*max(nextpred Q)
        #pred.clone()
        #predictions[argmax(move)] = our new Q pred

        self.optimiser.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimiser.step()
