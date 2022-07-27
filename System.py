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

#--------------------------CLASS ASSIGNMENT-----------------------------------------------------

class Entity():
    def __init__(self,x,y,movex,movey):
        self.x = x
        self.y = y
        self.movex = movex
        self.movey = movey

player = Entity(20,650,0,0)
playerspeed = 5

#----player projectiles----
playerbullets = []
playermaxbullets = 3
playerbulletwidth = 10
playerbulletheight= 10
def playerbulletrender(bulletlist):
    for bullet in bulletlist:
        pygame.draw.rect(mainscreen,(255,255,255),(bullet[0]-playerbulletwidth/2,bullet[1],playerbulletwidth,playerbulletheight))
        bullet[1] -= 5
        if bullet[1] < 0:
            bulletlist.remove(bullet)

#-------------------INITIAL LOADING---------------------------------------
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

#------------------------BASIC INPUTS-----------------------------

        if event.type == pygame.KEYDOWN:    #records key presses            
            if event.key == pygame.K_q:
                player.movex -= 1
            if event.key == pygame.K_e:
                player.movex += 1
            if event.key == pygame.K_w:
                if len(playerbullets) < playermaxbullets:
                    playerbullets.append([player.x + player_width//2, player.y])

        if event.type == pygame.KEYUP:  #records key unpresses
            if event.key == pygame.K_q:
                player.movex += 1
            if event.key == pygame.K_e:
                player.movex -= 1

    #update player position
    player.x = player.x + (playerspeed*player.movex)
    player.y = player.y + (playerspeed*player.movey)

    #contain player to screen
    if player.x < 0:
        player.x = 0
    if player.x > 1000 - player_width:
        player.x = 1000 - player_width

    #---------------UPDATE SCREEN------------------------------------

    mainscreen.fill(blue)
    pygame.draw.rect(mainscreen,(0,0,0),(0,0,1000,700)) #main game window
    pygame.draw.rect(mainscreen,(10,10,10),(0,700,1000,200)) #systems bar
    pygame.draw.rect(mainscreen,(15,15,15),(1000,0,500,900)) #metadata bar
    mainscreen.blit(player_spaceship, (player.x,player.y))
    playerbulletrender(playerbullets)

    pygame.display.update()

pygame.quit()