#####################################################################
# author:   Alex Hebert
# date:    01/11/2023 
# description: Player class for Game Template
#####################################################################
import pygame
from random import randint, choice
from Item import *
from Constants import *

#Person Class
class Person(pygame.sprite.Sprite, Item):
    def __init__(self, color= [0x00,0x2F,0x8B]):
        pygame.sprite.Sprite.__init__(self)
        Item.__init__(self)
        self.color = color
        self.setSize()
        self.rect = self.surf.get_rect()
        self.setColor()
        self.setRandomPosition()
        
    #Chooses a random color from COLORS and sets that to the sprite color
    def setColor(self):
        colors =  ['Blue', "Red", "Grey", "White", "Black"]
        color = choice(COLORS)
        self.surf.fill((color))
        self.color = colors[COLORS.index(color)]
    
    #Chooses a random value from 10 to 100 and scales the sprite accoringly
    def setSize(self):
        self.size = randint(10,100)
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        
    #Preforms actions based on the keys pressed    
    def update(self, pressed):
        if pressed[K_UP]:
            self.goUp()
        if pressed[K_DOWN]:
            self.goDown()
        if pressed[K_LEFT]:
            self.goLeft()
        if pressed[K_RIGHT]:
            self.goRight()
        if pressed[K_SPACE]:
            self.setColor()
            self.setSize()
        self.rect.move(self.x, self.y)
    
        #ensure sprite stays on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    #Sets sprite at a random location on screen
    def setRandomPosition(self):
        self.rect.move(randint(0,WIDTH), randint(0,HEIGHT))
        
    #returns a tuple of the sprite's x and y coodinates
    def getPosition(self):
        return(self.x,self.y)
    
    #Overloaded string function that reports color, size, position, and name
    def __str__(self):
        return Item.__str__(self)+" "+ self.color
    
########################### main game################################
# DO NOT CHANGE ANYTHING BELOW THIS LINE
#####################################################################

# Initialize pygame library and display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a person object
p = Person()
RUNNING = True  # A variable to determine whether to get out of the
                # infinite game loop

while (RUNNING):
    # Look through all the events that happened in the last frame to see
    # if the user tried to exit.
    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE):
            RUNNING = False
        elif (event.type == QUIT):
            RUNNING = False
        elif (event.type == KEYDOWN and event.key == K_SPACE):
            print(p)

    # Otherwise, collect the list/dictionary of all the keys that were
    # pressed
    pressedKeys = pygame.key.get_pressed()
    
    # and then send that dictionary to the Person object for them to
    # update themselves accordingly.
    p.update(pressedKeys)

    # fill the screen with a color
    screen.fill(WHITE)
    # then transfer the person to the screen
    screen.blit(p.surf, p.getPosition())
    pygame.display.flip()

