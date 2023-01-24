import pygame

from pygame.locals import(K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,KEYDOWN,QUIT)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.Surface((75,25))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)
            
        #Keep player on screen
        if self.rect.left<0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        
#initialize Pygame
pygame.init()

#Screen size consatants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#instatiate player
player = Player()

#variable to keep main loop running
running = True

#main loop
while running:
    #itterate through event queue
    for event in pygame.event.get():
        
        #If 'esc' pressed or window closed, stop main loop
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                
            elif event.type == QUIT:
                running = False

        #Get the set of pressed keys
        pressed_keys = pygame.key.get_pressed()

        player.update(pressed_keys)
    
        #fill screen white
        screen.fill((255,255,255))

        #draw player on screen
        screen.blit(player.surf,player.rect)
        
        #update display
        pygame.display.flip()
        