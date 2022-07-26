import pygame
import os
blue = (0,255,230)
WIDTH = 1500
HEIGHT = 900
mainscreen = pygame.display.set_mode((WIDTH,HEIGHT))
#sets the width and height of the game

pygame.display.set_caption("System")
#sets the name of the window
#set_caption can also be set_icon

clock = pygame.time.Clock()
#so the game can run smoothly

#--------------------IMAGE LOAD SECTION-------------------------------
player_spaceship_image = pygame.image.load(os.path.join("Assets","player_spaceship.png"))
player_width,player_height = 50,40
player_spaceship = pygame.transform.scale(player_spaceship_image,(player_width,player_height))



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
mainscreen.blit(player_spaceship, (player.x,player.y))
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

    player.x = player.x + (10*player.movex)
    player.y = player.y + (10*player.movey)

    #-------------CONTAIN PLAYER TO SCREEN----------------------------

    if player.y < 0:
        player.y = 0
    if player.y > HEIGHT - player_height:
        player.y = HEIGHT - player_height
    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player_width:
        player.x = WIDTH - player_width

    #---------------UPDATE SCREEN------------------------------------

    mainscreen.fill(blue)
    mainscreen.blit(player_spaceship, (player.x,player.y))

    pygame.display.update()

pygame.quit()