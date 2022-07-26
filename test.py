import pygame
#lets you actualy code the game

blue = (0,255,230)
WIDTH = 900
HEIGHT = 500
mainscreen = pygame.display.set_mode((WIDTH,HEIGHT))
#sets the width and height of the game

pygame.display.set_caption("Beep Blaster")
#sets the name of the window
#set_caption can also be set_icon

clock = pygame.time.Clock()
#so the game can run smoothly

#class example (self value is very important)
class Entity():
    def __init__(self,x,y,movex,movey):
        self.x = x
        self.y = y
        self.movex = movex
        self.movey = movey

player = Entity(20,20,0,0)

#first loading of screen (will want to upate)
mainscreen.fill(blue)
pygame.draw.rect(mainscreen,(255,255,255),(player.x,player.y,20,20))
pygame.display.update()

#LIVE INPUT, will probably be run at the end of the code
live = True
while live:
    clock.tick(60)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            live = False   

        #----------BASIC MOVEMENT-----------------------------

        if event.type == pygame.KEYDOWN:    #records key presses
            if event.key == pygame.K_w:
                player.movey -= 1
            if event.key == pygame.K_s:
                player.movey += 1
            
            if event.key == pygame.K_a:
                player.movex -= 1
            if event.key == pygame.K_d:
                player.movex += 1

        if event.type == pygame.KEYUP:  #records key unpresses
            if event.key == pygame.K_w:
                player.movey += 1
            if event.key == pygame.K_s:
                player.movey -= 1

            if event.key == pygame.K_a:
                player.movex += 1
            if event.key == pygame.K_d:
                player.movex -= 1

    #---------------UPDATE PLAYER POSITION----------------------------    

    player.x = player.x + (5*player.movex)
    player.y = player.y + (5*player.movey)

    #-------------CONTAIN PLAYER TO SCREEN----------------------------

    if player.y < 0:
        player.y = 0
    if player.y > 480:
        player.y = 480
    if player.x < 0:
        player.x = 0
    if player.x > 880:
        player.x = 880

    #---------------UPDATE SCREEN------------------------------------

    mainscreen.fill(blue)

    pygame.draw.rect(mainscreen,(255,255,255),(player.x,player.y,20,20))

    pygame.display.update()

pygame.quit()