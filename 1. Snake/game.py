import os
import pygame  
import sys
import random
import numpy as np
from collections import namedtuple

Point = namedtuple('Point', 'x, y')

class Snake(object):
    
    
    
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = UP
        self.color = (17, 24, 47)
        self.score = 0
        self.generation = 1
        self.frameIteration = 0
        self.reward = 0
        self.gameOver = False
        self.clock = pygame.time.Clock() # initialises close
        self.Point = namedtuple('Point', 'x, y')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)#gives peramiters for screensize
        self.myfont = pygame.font.SysFont("monospace", 16)
        
        self.clockSpeed = 100

        self.foodPosition = (random.randint(1, GRID_WIDTH-2) * GRIDSIZE, random.randint(1, GRID_HEIGHT-2) * GRIDSIZE)

        

        surface = pygame.Surface(self.screen.get_size())
        surface = surface.convert()
        drawGrid(surface)#creates a grid using the peramiters from surface

       



    def getHeadPos(self):
        return self.positions[0]

    def turn(self, point):
        self.direction = point

    def move(self):
        reward = 0
        gameOver = False

        cur = self.getHeadPos()
        x, y = self.direction
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)

        if new[0] == 0 or new[0] == (SCREEN_WIDTH - 20) or new[1] == 0 or new[1] == (SCREEN_HEIGHT - 20):#hits wall
            reward = -10
            reward += (self.score * 10)
            gameOver = True
            return reward, gameOver, self.score
            #self.reset()
        elif len(self.positions) > 2 and new in self.positions[2:]:#hits self
            reward = -10
            reward += (self.score * 10)
            gameOver = True
            return reward, gameOver, self.score##<------------------------
            #self.reset()
        elif self.frameIteration > 100*(self.length):#lives too long
            reward = -10
            reward += (self.score * 10)
            gameOver = True
            return reward, gameOver, self.score
        else:#it is fine
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()#remove the last part of the tail, add a new part
            return reward, gameOver, self.score
        
        

    def collisionCheck(self, pt=None):
        if pt == None:
            cur = self.getHeadPos()
            x, y = self.direction
            new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)
            pt = new
        
        if pt[0] == 0 or pt[0] == (SCREEN_WIDTH - 20) or pt[1] == 0 or pt[1] == (SCREEN_HEIGHT - 20):
            return True
        elif pt in self.positions[2:]:
            return True
        else:
            return False


        

    def gameOverCheck(self):
        if self.gameOver == True:
            self.reset()

    def reset(self):
        self.score = 0
        self.length = 1
        self.generation += 1
        self.frameIteration = 0
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = RIGHT
        print(str(self.generation))
        self.foodPosition = (random.randint(1, GRID_WIDTH-2) * GRIDSIZE, random.randint(1, GRID_HEIGHT-2) * GRIDSIZE)

        
        #defines our objects to classes
        snake = Snake()
        food = Food()

    




    def draw(self, surface):
        
        #temp = self.getHeadPos##need to convert getHeadPos into actual coordinates to compare
        cur = self.getHeadPos()
        x, y = self.direction
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)
        for p in self.positions:
            if p == cur:
                r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, self.color, r)
                pygame.draw.rect(surface, (255, 255, 255), r, 1)
            else:
                r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))#############this doesnt work/ head and body aren't seperate colours ##why???##
                pygame.draw.rect(surface, self.color, r)
                pygame.draw.rect(surface, (0, 0, 0), r, 1)

    def handleInput(self, action):
        for event in pygame.event.get():#will make sure the entire game closes upon hitting the close button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clockWise = [1, 2, 3, 4]
        tempDirection = self.direction

        if tempDirection == UP:
            idx = 1
        elif tempDirection == RIGHT:
            idx = 2
        elif tempDirection == DOWN:
            idx = 3
        elif tempDirection == LEFT:
            idx = 4

        if np.array_equal(action, [1, 0, 0]):
            if idx == 5:
                idx = 1

            if idx == 1:
                tempDirection = UP
            elif idx == 2:
                tempDirection = RIGHT
            elif idx == 3:
                tempDirection = DOWN
            elif idx == 4:
                tempDirection = LEFT

            self.turn(tempDirection)

        elif np.array_equal(action, [0, 1, 0]):
            idx += 1

            if idx == 5:
                idx = 1

            if idx == 1:
                tempDirection = UP
            elif idx == 2:
                tempDirection = RIGHT
            elif idx == 3:
                tempDirection = DOWN
            elif idx == 4:
                tempDirection = LEFT

            self.turn(tempDirection)

        elif np.array_equal(action, [0, 0, 1]):
            idx -= 1

            if idx == 5:
                idx = 1

            if idx == 1:
                self.direction = UP
            elif idx == 2:
                self.direction = RIGHT
            elif idx == 3:
                self.direction = DOWN
            elif idx == 4:
                self.direction = LEFT

            self.turn(self.direction)
        #[up, down, left, right]

        ##


    def playStep(self, action):
        clock = pygame.time.Clock() # initialises close
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)#gives peramiters for screensize
        self.rewardAdd = 0
        surface = pygame.Surface(screen.get_size())
        surface = surface.convert()
        clock.tick(self.clockSpeed)
        self.frameIteration += 1
        self.handleInput(action)
        drawGrid(surface)
        rewardAdd0, gameOver0, score0 = self.move()
        headPos = self.getHeadPos()
        foodPos = self.foodPosition
        if headPos == foodPos:
            self.length += 1
            self.score += 1
            self.create()
            rewardAdd0 += 10
        self.draw(surface)
        self.drawFood(surface)
        self.drawFin(surface)



        return rewardAdd0, gameOver0, score0,  
        

    def drawFin(self, surface):
        self.screen.blit(surface, (0, 0))
        text = self.myfont.render("Score {0}".format(self.score), 1, (0, 0, 0))
        self.screen.blit(text, (5, 10))
        pygame.display.update()

    ##unused
    def locateDanger(self):
        cur = self.getHeadPos()
        x, y = self.direction
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), ((cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT))


        if new[0] == 0 or new[0] == (SCREEN_WIDTH - 20) or new[1] == 0 or new[1] == (SCREEN_HEIGHT - 20):
            reward = -10
            reward += (self.score * 10)
            gameOver = True
            return reward, gameOver, self.score
            #self.reset()
        elif len(self.positions) > 2 and new in self.positions[2:]:
            reward = -10
            reward += (self.score * 10)
            gameOver = True
            return reward, gameOver, self.score##<------------------------
            #self.reset().



    
        
        ####
        #fruit
        ####

    def create(self):#will create a fruit at a random position within the grid
        self.foodPosition = (random.randint(1, GRID_WIDTH-2) * GRIDSIZE, random.randint(1, GRID_HEIGHT-2) * GRIDSIZE)

    def drawFood(self, surface):#draws the fruit onscreen
        r = pygame.Rect((self.foodPosition[0], self.foodPosition[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def getFoodX(self):
        return self.foodPosition[0]

    def getFoodY(self):
        return self.foodPosition[1]
  
        



class Food(object):

    def __init__(self):#initialising values for the Food object
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.create()

    def create(self):#will create a fruit at a random position within the grid
        self.position = (random.randint(1, GRID_WIDTH-2) * GRIDSIZE, random.randint(1, GRID_HEIGHT-2) * GRIDSIZE)

    def getX(self):
        return self.position[0]

    def getY(self):
        return self.position[1]

    def drawFood(self, surface):#draws the fruit onscreen
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)


def drawGrid(surface):
    for y in range (0, int(GRID_HEIGHT)):
        for x in range (0, int(GRID_WIDTH)):
            if (x == 0 or x == GRID_WIDTH-1 or y == 0 or y == GRID_HEIGHT-1) :#if our current coordinate is anywhere along the outer edge of the grid
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (255, 0, 0), r)#draw red rectangles
            else:#everything within the grid
                if (x+y) % 2 == 0:#if we have an even number place the first colour
                    r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                    pygame.draw.rect(surface, (93, 216, 228), r)
                else:#if we have an odd number place the second colour
                    r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                    pygame.draw.rect(surface, (84, 194, 205), r)


#global vars


#set grid size, number within SQUARESIZE is the number of grid spaces within an axis (SQUARESIZE = 12 will make a 12*12 grid)
SQUARESIZE = 12
###########################
SQUARESIZE = SQUARESIZE * 20

SCREEN_WIDTH = SQUARESIZE
SCREEN_HEIGHT = SQUARESIZE


GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE#will divide our screen into squares each taking up 20 pixels

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():
    #pygame.init()#pygame setup

    clock = pygame.time.Clock() # initialises close
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)#gives peramiters for screensize

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)#creates a grid using the peramiters from surface

    #defines our objects to classes
    snake = Snake()
    food = Food()

    #sets the font for scoring
    myfont = pygame.font.SysFont("monospace", 16)


    score = 0#unused global score
    """ while (True):
        clock.tick(10)
        snake.playStep()
        if snake.getHeadPos() == food.position:
            snake.length += 1
            snake.score += 1
            food.create()
        drawGrid(surface)
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = self.myfont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update() """

    #while (True):
        #clock.tick(10)
        #snake.frameIteration += 1
        #snake.handleInput()
        #drawGrid(surface)
        #snake.move()
        #if snake.getHeadPos() == food.position:
            #snake.length += 1
            #snake.score += 1
            #food.create()
        #snake.draw(surface)
        #food.draw(surface)
       # screen.blit(surface, (0, 0))
       # text = myfont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
       # screen.blit(text, (5, 10))
       # pygame.display.update()
#main()