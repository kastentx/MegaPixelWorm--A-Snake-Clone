# Nick Kasten
# megapixelworm.py
# worm with improved collision detection
# 1/7/2015

import pygame
import random

# directions of movement
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# color values
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class TitleBar:
    """ Text and Title bar at the bottom of screen """
    
    def __init__(self, surface):
        pygame.font.init()
        self.surface = surface
        self.font = pygame.font.SysFont(None, 36)
        self.score = 0
        self.drawTitle()
        self.drawTitleBox()
        self.drawScore()

    def drawTitleBox(self):
        pygame.draw.rect(self.surface, WHITE, (0, height, width, titleHeight), 2)

    def drawTitle(self):
        title = self.font.render("Hungry Snake Challenge", True, WHITE)
        self.surface.blit(title, (5, (height+10)))

    def updateScore(self, score):
        self.score = score

    def drawScore(self):
        scoreText = self.font.render("Score: %d" % (self.score), True, WHITE)
        self.surface.blit(scoreText, ((width/2), (height+10)))

    def eraseScore(self):
        pygame.draw.rect(self.surface, BLACK, (0, height, width, titleHeight), 0)

    def showScore(self):
        self.eraseScore()
        self.drawTitle()
        self.drawTitleBox()
        self.drawScore()
        
        

class Food:
    """ a piece of food """

    def __init__(self, surface):
        """ creates the food """
        self.surface = surface
        self.x = random.randint(0, width-1)
        self.y = random.randint(0, height-1)
        
        pygame.draw.circle(self.surface, (GREEN), (self.x, self.y), 5, 0)

    def erase(self):
        pygame.draw.circle(self.surface, (BLACK), (self.x, self.y), 5, 0)
        
        
class Worm:
    """ a worm """

    def __init__(self, surface, x, y, length):
        """ creates a worm """
        self.surface = surface
        self.x = x
        self.y = y
        self.length = length
        self.dirX = 0
        self.dirY = -1
        self.body = []
        self.last = (0, 0)
        self.crashed = False
        self.eating = False
        self.numEaten = 0
        self.numTotalEaten = 0

    def keyEvent(self, event):
        """ Handle key events that affect the worm """
        if event.key == pygame.K_UP:
            if self.dirY == (1):
                return
            self.direction(UP)
        elif event.key == pygame.K_DOWN:
            if self.dirY == (-1):
                return            
            self.direction(DOWN)
        elif event.key == pygame.K_LEFT:
            if self.dirX == (1):
                return            
            self.direction(LEFT)
        elif event.key == pygame.K_RIGHT:
            if self.dirX == (-1):
                return            
            self.direction(RIGHT)

    def direction(self, pixelDir):
        self.dirX, self.dirY = pixelDir

    def move(self):
        """ move the worm """
        self.body.insert(0, (self.x, self.y))
        self.x += self.dirX
        self.y += self.dirY

        # this checks for the color of the worm to detect collision
        r, g, b, a = self.surface.get_at((self.x, self.y))
        if (r, g, b) == (GREEN):
            self.eatFood()
        elif (r, g, b) == (WHITE):
            self.crashed = True
            
        if len(self.body) >= self.length:
            self.last = self.body.pop()
        else:
            self.last = self.body[-1]

    def draw(self, hasEaten=False):
        """ draw the worm """
        if hasEaten:
            for x, y in self.body:
                self.surface.set_at((x, y), (WHITE))
        else:
            self.surface.set_at((self.x, self.y), (WHITE))
            self.surface.set_at((self.last), (BLACK))

    def eatFood(self):
        """turn the eaten food to black"""
        upR, upG, upB, upA = self.surface.get_at((self.x, self.y-5))
        downR, downG, downB, downA = self.surface.get_at((self.x, self.y+5))
        leftR, leftG, leftB, leftA = self.surface.get_at((self.x-5, self.y))
        rightR, rightG, rightB, rightA = self.surface.get_at((self.x+5, self.y))
        if (upG) == (255) or (downG) == (255) or (leftG) == (255) or (rightG) == (255):
            self.numEaten += 1
            if self.numEaten >= 5:    
                self.eating = True
                self.numTotalEaten += 1
                self.numEaten = 0
                self.length += 80

                print("Yummmo!")
                print(self.numTotalEaten)
                titleBar.updateScore(self.numTotalEaten)
                titleBar.showScore()
        

# window dimensions
width = 640
height = 400
titleHeight = 50

# set up the blank black screen
screen = pygame.display.set_mode((width, (height+titleHeight)))
screen.fill((BLACK))

# set the clock and infinite loop
clock = pygame.time.Clock()
running = True

# create our Worm, food, and title objects
worm = Worm(screen, int(round(width / 2)), int(round(height / 2)), 200)
food = Food(screen)
titleBar = TitleBar(screen)

while running:

    worm.draw()
    worm.move()
    
    if worm.crashed or worm.x <= 0 or worm.x >= width-1 or worm.y <= 0 or worm.y >= height-1:
        print("You Crashed!")
        running = False
    elif worm.eating:
        food.erase()
        worm.draw(True)
        food = Food(screen)
        worm.eating = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            worm.keyEvent(event)
        

    pygame.display.flip()
    clock.tick(240)
pygame.quit()
