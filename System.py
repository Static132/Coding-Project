import pygame
import os
black = (0,0,0)
WIDTH = 1500
HEIGHT = 900
mainscreen = pygame.display.set_mode((WIDTH,HEIGHT))
#sets the width and height of the game

pygame.display.set_caption("SYSTEM")
#sets the name of the window
#set_caption can also be set_icon

clock = pygame.time.Clock()
#so the game can run smoothly

#--------------------------CLASS ASSIGNMENT-----------------------------------------------------

#----enemy class for loading images----
class Entity():
    def __init__(self,image,width,height):
        self.image = pygame.image.load(os.path.join("Assets",image))
        self.width = width
        self.height = height
        self.sprite = pygame.transform.scale(self.image,(self.width,self.height))

scout = Entity("enemy_spaceship_1.png",34,40)
carrier = Entity("enemy_spaceship_2.png",40,40)
attacker = Entity("enemy_spaceship_3.png",46,40)

class Player(Entity):
    def __init__(self,image,width,height,x,y,movex,movey):
        self.image = pygame.image.load(os.path.join("Assets",image))
        self.width = width
        self.height = height
        self.sprite = pygame.transform.scale(self.image,(self.width,self.height))
        self.x = x
        self.y = y
        self.movex = movex
        self.movey = movey

player = Player("player_spaceship.png",50,40,20,650,0,0)
playerspeed = 5

#-------------------------GAME FUNCTIONS--------------------------------------

#----player projectiles----
playerbullets = []
playermaxbullets = 3
playerbulletwidth = 10
playerbulletheight= 10


#----LEVEL LOADING----
def loadlevel(level_list):
    level = level_list
    spawnpoint = []
    for y_axis in range(50,200,50):
        for x_axis in range(50,1000,50):
            spawnpoint.append([x_axis,y_axis])

    for enemy in range(0,len(level)):
        spawnpoint[enemy] = [level[enemy],spawnpoint[enemy]]
    
    for empty in range(len(level),57):
            spawnpoint[empty] = "0"
    
    while len(spawnpoint) != len(level_list):
        for blank in spawnpoint:
            if blank == "0":
                spawnpoint.remove(blank)
    return spawnpoint

#example spawnpoint = [scout,1],[x,y]


level_1 = loadlevel([
    [1,1],[2,1],[1,1],[1,1],[1,1],[1,1],
    [1,1],[1,1],[1,1],[3,1],[1,1],[1,1],
    [1,1],[1,1],[1,1],[1,1],[1,1],[2,1],
    [1,1]
])

#level renderer, repeat once level has been loaded
def levelrender(spawnlist,bulletlist):
    for enemy in range(0,(len(spawnlist))):
        if ((spawnlist[enemy])[0])[0] == 1:
            mainscreen.blit(scout.image,((spawnlist[enemy][1])[0] - scout.width/2 ,(spawnlist[enemy][1])[1]))
        if ((spawnlist[enemy])[0])[0] == 2:
            mainscreen.blit(carrier.image,((spawnlist[enemy][1])[0] - carrier.width/2 ,(spawnlist[enemy][1])[1]))
        if ((spawnlist[enemy])[0])[0] == 3:
            mainscreen.blit(attacker.image,((spawnlist[enemy][1])[0] - attacker.width/2 ,(spawnlist[enemy][1])[1]))
    for bullet in bulletlist:
        pygame.draw.rect(mainscreen,(255,255,255),(bullet[0]-playerbulletwidth/2,bullet[1],playerbulletwidth,playerbulletheight))
        bullet[1] -= 5
        if bullet[1] < 0 - playerbulletheight:
            bulletlist.remove(bullet)

current_level = level_1

#-------------------INITIAL LOADING---------------------------------------

#this will probably change to some other load screen
mainscreen.fill(black)
mainscreen.blit(player.image, (player.x,player.y))
pygame.draw.rect(mainscreen,(0,0,0),(0,0,1000,700)) #main game window
pygame.draw.rect(mainscreen,(10,10,10),(0,700,1000,200)) #systems bar
pygame.draw.rect(mainscreen,(15,15,15),(1000,0,500,900)) #metadata bar
pygame.display.update()



#LIVE INPUT, will probably be run at the end of the code
def main():
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
                        playerbullets.append([player.x + player.width//2, player.y])

            if event.type == pygame.KEYUP:  #records key unpresses
                if event.key == pygame.K_q:
                    player.movex += 1
                if event.key == pygame.K_e:
                    player.movex -= 1

        #update player position
        player.x = player.x + (playerspeed*player.movex)
        player.y = player.y + (playerspeed*player.movey)

        #contain player to main screen
        if player.x < 0:
            player.x = 0
        if player.x > 1000 - player.width:
            player.x = 1000 - player.width

        #---------------UPDATE SCREEN------------------------------------

        pygame.draw.rect(mainscreen,(0,0,0),(0,0,1000,700))
        mainscreen.blit(player.image, (player.x,player.y))
        levelrender(current_level,playerbullets)
        pygame.display.update(0,0,1000,700)

main()
pygame.quit()