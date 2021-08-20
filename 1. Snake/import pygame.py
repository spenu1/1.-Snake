import pygame  
import sys
import random

class Snake(object):
    

    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)
        self.score = 0


    def getHeadPos(self):
        return self.positions[0]

    def turn(self, point):
        self.direction = point

    def move(self):
        cur = self.getHeadPos()
        x, y = self.direction
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)

        if new[0] == 0 or new[0] == (SCREEN_WIDTH - 20) or new[1] == 0 or new[1] == (SCREEN_HEIGHT - 20):
            self.reset()
        elif len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.score = 0
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def handleInput(self):
        for event in pygame.event.get():#will make sure the entire game closes upon hitting the close button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:#if a key is recognised as pressed
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


class Food(object):

    def __init__(self):#initialising values for the Food object
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.create()

    def create(self):#will create a fruit at a random position within the grid
        self.position = (random.randint(1, GRID_WIDTH-2) * GRIDSIZE, random.randint(1, GRID_HEIGHT-2) * GRIDSIZE)

    def draw(self, surface):#draws the fruit onscreen
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
    pygame.init()#pygame setup

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
    while (True):
        clock.tick(10)
        snake.handleInput()
        drawGrid(surface)
        snake.move()
        if snake.getHeadPos() == food.position:
            snake.length += 1
            snake.score += 1
            food.create()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()


main()