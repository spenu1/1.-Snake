from typing import final
import torch
import random
import numpy as np
import pygame
from collections import deque
from game import Food, UP, DOWN, LEFT, RIGHT, Point, Snake, Food
from model import LinearQNet, QTrainer
from helper import plot
import os


#reference https://www.youtube.com/watch?v=6pJBPPrDO40&t=83s

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.gameNo = 0
        self.epsilon = 0 #devience from memory
        self.gamma = 0.8 # "discount rate"
        self.memory = deque(maxlen=MAX_MEMORY) #popleft() if we exceed maxlength, we will remove older values/ memories
        self.model = LinearQNet(12, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)



    def getState(self, game):

        head = game.getHeadPos()
        stateLeft = Point(head[0] - 20, head[1])
        stateRight = Point(head[0] + 20, head[1])
        stateUp = Point(head[0], head[1] - 20)
        stateDown = Point(head[0], head[1] + 20)

        if game.direction == None:
            game.direction == UP
        
        if game.direction == UP:
            dirUP = True
        else:
            dirUP = False

        if game.direction == DOWN:
            dirDOWN = True
        else:
            dirDOWN = False

        if game.direction == LEFT:
            dirLEFT = True
        else:
            dirLEFT = False

        if game.direction == RIGHT:
            dirRIGHT = True
        else:
            dirRIGHT = False
        #[up, down, left, right]

        foodX = game.getFoodX()
        foodY = game.getFoodY()

        state = [
            (game.collisionCheck(stateUp)),

            (game.collisionCheck(stateDown)),

            (game.collisionCheck(stateLeft)),

            (game.collisionCheck(stateRight)),

            dirUP,

            dirDOWN,

            dirLEFT,

            dirRIGHT,

            foodY < head[1],
            foodY > head[1],
            foodX < head[0],
            foodX > head[0]]
        
        

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, nextState, gameOver):
        self.memory.append((state, action, reward, nextState, gameOver))#popleft is memory is maxed. extra brackets for one tuple


    def trainLong(self):

        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)#defines a list of tuples (?)
        else:
            mini_sample = self.memory

        states, actions, rewards, nextStates, gameOvers = zip(*mini_sample)
        self.trainer.trainStep(states, actions, rewards, nextStates, gameOvers)
        #for state, action, reward, nextState, gameOver in mini_sample:
        #
        

    def trainShort(self, state, action, reward, nextState, gameOver):
        self.trainer.trainStep(state, action, reward, nextState, gameOver)

    def getAction(self, state):
        #random opening move reinforces deviation
        self.epsilon = 80 - self.gameNo
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)#uses our state to get float values 
            prediction = self.model(state0) # get our forward move, converts each movement option into a float number, higher the float the better the option
            move = torch.argmax(prediction).item()#get the highest float (best option)
            final_move[move] = 1#set our move (in the correct move array position) as true

        return final_move#return the move we will make


def train():
    plotScores = []
    plotMeanScore = []
    totalScore = 0
    recordScore = 0
    agent = Agent()
    game = Snake()
    
    while True:
        #get state
        
        oldState = agent.getState(game)
        #get input
        
        finalMove = agent.getAction(oldState)
        #carry out input
        
        reward, gameOver, score = game.playStep(finalMove)
        #get new state
        
        newState = agent.getState(game)
        #short memory train
        
        agent.trainShort(oldState, finalMove, reward, newState, gameOver)
        #remember store to memory
        
        agent.remember(oldState, finalMove, reward, newState, gameOver)
        
        if gameOver:
            #long memory train
            
            game.reset()
            agent.gameNo += 1
            
            agent.trainLong()

            if score > recordScore:
                recordScore = score
                
                agent.model.save()

            print('Game', agent.gameNo, 'score', score, 'record:', recordScore)
            
            
            totalScore += score
            meanScore = totalScore / agent.gameNo
            #if agent.gameNo > 80:
                ##del plotScores[0]
                #del plotMeanScore[0]


            plotScores.append(score)
            #print("appending mean score...")
            plotMeanScore.append(meanScore)
            #print("plotting plotscore, plotmeanscore")
            plot(plotScores, plotMeanScore)



if __name__ == '__main__':
    pygame.init()
    train()

