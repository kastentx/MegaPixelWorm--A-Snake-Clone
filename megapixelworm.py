# Nick Kasten
# megapixelworm.py
# Mega Pixel Worm: A Snake Clone
# 1/7/2015

# dataFile = shelve.open('score.txt') # here you will save the score variable   
# d['score'] = score           # thats all, now it is saved on disk.
# d.close()

import pygame, random, sys, shelve
from pygame.locals import *

# initialize pygame and retrieve high scores
pygame.init()
dataFile = shelve.open('score.txt') 

# directions of movement
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)

# basic colors
#          R    G    B
RED   = ( 255,   0,   0 )
GREEN = (   0, 255,   0 )
BLUE  = (   0,   0, 255 )
WHITE = ( 255, 255, 255 )
BLACK = (   0,   0,   0 )

# window dimensions
width       = 640
height      = 430
titleHeight = 50
pygame.display.set_caption("Hungry Snake Challenge")

# set up the blank black screen
screen     = pygame.display.set_mode((width, (height+titleHeight)))
screenRect = screen.get_rect()
screen.fill((BLACK))

# set the clock and infinite loop
FPS      = 240
fpsClock = pygame.time.Clock()
running  = True

# Content and Position of Title text
titleText       = pygame.font.Font( "freesansbold.ttf", 48 )
titleSurfaceObj = titleText.render( "Megal Pixel Worm", True, GREEN, BLUE )
titleRectObj    = titleSurfaceObj.get_rect( center = ( screenRect.centerx, screenRect.centery - 100 ) )

# Content and Position of Game Over text
gameOverText       = pygame.font.Font( "freesansbold.ttf", 48 )
gameOverSurfaceObj = gameOverText.render( "GAME OVER", True, WHITE )
gameOverRectObj    = gameOverSurfaceObj.get_rect( center = ( screenRect.centerx, screenRect.centery - 100 ) )

# Content and Position of Press a Key text
pressKeyText       = pygame.font.Font( "freesansbold.ttf", 18 )
pressKeySurfaceObj = pressKeyText.render( "Press any key...", True, WHITE )
pressKeyRectObj    = pressKeySurfaceObj.get_rect( center = ( screenRect.centerx, screenRect.centery + 100 ) )

###### CLASS AND FUNCTION DEFINITIONS ######
class TitleBar:
    """ Text and Title bar at the bottom of screen """
    
    def __init__(self, surface):
        self.surface = surface
        self.font    = pygame.font.SysFont(None, 36)
        self.score   = 0
        
        self.drawTitle()
        self.drawTitleBox()
        self.drawScore()

    def drawTitleBox(self):
        pygame.draw.rect(self.surface, WHITE, (0, height, width, titleHeight), 2)

    def drawTitle(self):
        title = self.font.render("Megal Pixel Worm", True, WHITE)
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

def keyPressed():
    """ Removes KEYDOWN events from the event queue
        and returns KEYUP events """
    checkForQuit()
    for event in pygame.event.get( [ KEYDOWN, KEYUP ] ):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None
    

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def terminate():
    pygame.quit()
    sys.exit()

def showTitle():
    screen.blit( titleSurfaceObj, titleRectObj ) # display title text
    screen.blit( pressKeySurfaceObj, pressKeyRectObj ) # display press any key text
    while keyPressed() == None:
        pygame.display.update()
        fpsClock.tick( FPS )

    screen.fill(BLACK)

def showGameOver(titleBar):
    # Content and Position of Final Score Text
    finalScoreText       = pygame.font.Font( "freesansbold.ttf", 18 )
    finalScoreSurfaceObj = finalScoreText.render( "You scored %d points!" % titleBar.score, True, WHITE )
    finalScoreRectObj    = finalScoreSurfaceObj.get_rect( center = ( screenRect.centerx, screenRect.centery + 50 ) )

    # Content and Position of High Score Text
    highScoreText       = pygame.font.Font( "freesansbold.ttf", 18 )
    highScoreSurfaceObj = highScoreText.render( "Current High Score: %d points!" % dataFile['highscore'], True, WHITE )
    highScoreRectObj    = highScoreSurfaceObj.get_rect( center = ( screenRect.centerx, screenRect.centery + 25 ) )    

    screen.fill(BLACK)

    screen.blit( gameOverSurfaceObj, gameOverRectObj ) # display game over text
    screen.blit( pressKeySurfaceObj, pressKeyRectObj ) # display press any key text
    screen.blit( highScoreSurfaceObj, highScoreRectObj ) # display high score text
    screen.blit( finalScoreSurfaceObj, finalScoreRectObj ) # display final score text

    while keyPressed() == None:
        pygame.display.update()
        fpsClock.tick( FPS )

    screen.fill(BLACK)   
###### END OF DEFINITIONS ######

# main game loop
showTitle()

# create our Worm, food, and title objects
worm = Worm(screen, int(round(width / 2)), int(round(height / 2)), 200)
food = Food(screen)
titleBar = TitleBar(screen)
dataFile['highScore'] = titleBar.score

while running:

    worm.draw()
    worm.move()
    
    if worm.crashed or worm.x <= 0 or worm.x >= width-1 or worm.y <= 0 or worm.y >= height-1:
        print("You Crashed!")
        if titleBar.score > dataFile['highscore']:
            dataFile['highscore'] = titleBar.score 
        showGameOver(titleBar)        
        dataFile.close()
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
    fpsClock.tick(FPS)
pygame.quit()
