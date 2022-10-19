import pygame
pygame.font.init()
import os
from random import randint
black = (0,0,0)
WIDTH = 1500
HEIGHT = 900
mainscreen = pygame.display.set_mode((WIDTH,HEIGHT))
title_text = pygame.font.SysFont("systemtextfont", 100)
main_text = pygame.font.SysFont("systemtextfont", 20)
#sets the width and height of the game

pygame.display.set_caption("SYSTEM")
#sets the name of the window
#set_caption can also be set_icon

clock = pygame.time.Clock()
#so the game can run smoothly

#----text generation----
text_counter = 0
text = ""
def printtext():
    global text_counter
    global text
    global score
    if text_counter < 100:
        text_counter += 1
    pygame.draw.rect(mainscreen,(15,15,15),(1000,100,400,900))
    mainscreen.blit(main_text.render(text[0:text_counter//5], False, (255, 255, 255)),(1000,150))
    mainscreen.blit(main_text.render(("your score is "+str(score))[0:text_counter//5], False, (255, 255, 255)),(1000,175))
    pygame.display.update(1000,100,500,900)

prompt_counter = 0
def textprompt():
    global prompt_counter
    global text
    global text_counter
    if prompt_counter == 0:
        prompt_counter += 1
        text = "welcome to system"
    elif prompt_counter == 2:
        prompt_counter += 1
        text = "game over"
        text_counter = 0
    elif prompt_counter == 4:
        prompt_counter += 1
        text = "you win"
        text_counter = 0

#--------------------------CLASS ASSIGNMENT-----------------------------------------------------

#----enemy class for loading images----
class Entity():
    def __init__(self,image,width,height,damage):
        self.image = pygame.image.load(os.path.join("Assets",image))
        self.width = width
        self.height = height
        self.sprite = pygame.transform.scale(self.image,(self.width,self.height))
        self.damage = damage

scout = Entity("enemy_spaceship_1.png",34,40,1)
carrier = Entity("enemy_spaceship_2.png",40,40,2)
attacker = Entity("enemy_spaceship_3.png",46,40,3)

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
playerbulletwidth = 10
playerbulletheight = 10
playermaxbullets = 3
powerup = 0
score = 0

enemybullets = []
enemybulletwidth = 5
enemybulletheight = 5

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

#----------level renderer, repeat once level has been loaded----------------
def meta_update():
    pygame.draw.rect(mainscreen,(10,10,10),(0,700,1000,200)) #health/shields bar
    pygame.draw.rect(mainscreen,(255,50,0),(50,750,playerhealth*9,100)) #health
    pygame.draw.rect(mainscreen,(0,205,255),(0,700,1000-((1000//playermaxbullets)*len(playerbullets)),50)) #bullet "charge"
    pygame.display.update(0,700,1000,200)

def levelrender():
    global level
    global current_level
    global playerbullets
    global enemybullets
    global playerhealth
    global prompt_counter
    global score
    global playermaxbullets
    if current_level == []: #checks if the level is complete and loads the next level if so
        playerhealth += 25
        if playerhealth > 100:
            playerhealth = 100
            meta_update()
        level += 1
        if level == 2:
            level += 1
            current_level = loadlevel([[1,1],[2,1],[1,1],[3,1],[2,1],[1,1],[1,1],[1,1],[2,1],[3,1],[2,1],[1,1],[1,1],[1,1],[2,1],[3,1],[1,1],[2,1],[1,1]])
            playermaxbullets += 1
        if level == 4:
            level += 1
            current_level = loadlevel([[1,1],[2,1],[1,1],[3,1],[2,1],[1,1],[1,1],[1,1],[2,1],[3,1],[2,1],[1,1],[1,1],[1,1],[2,1],[3,1],[1,1],[2,1],[1,1],[1,1],[2,1],[1,1],[1,1],[1,1],[1,1],
            [1,1],[1,1],[1,1],[3,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[2,1],[1,1]])
        if level == 6:
            prompt_counter = 4

    #-----enemy rendering and firing bullets-----
    for enemy in current_level:
        if (enemy[0])[0] == 1:
            sprite = scout
        elif (enemy[0])[0] == 2:
            sprite = carrier
        elif (enemy[0])[0] == 3:
            sprite = attacker

        spriterect = [(enemy[1])[0] - sprite.width/2 ,(enemy[1])[1]]

        mainscreen.blit(sprite.image, spriterect)
        if randint(0,200) < (enemy[0])[0]:
            enemybullets.append([(enemy[1])[0],(enemy[1])[1]+sprite.height,(enemy[0])[0]])
            if (enemy[0])[0] == 3:
                for i in range(0,3):
                    enemybullets.append([(enemy[1])[0],(enemy[1])[1]+sprite.height,(enemy[0])[0]])

        #----enemy slowly move toward player, then close into the middle of the screen----
        if randint(0,len(current_level)^2) < (enemy[0])[0]:
            if (enemy[1])[1] < 500:
                (enemy[1])[1] += 6 - (enemy[0])[0]
            else:
                if (enemy[1])[0] < 500:
                    (enemy[1])[0] += 4 - (enemy[0])[0]
                else:
                    (enemy[1])[0] -= 4 - (enemy[0])[0]

        #----enemy upgrades----
        if randint(0,500*len(current_level)^2) < (enemy[0])[0]:
            (enemy[0])[0] += 1
            if (enemy[0])[0] > 3:
                (enemy[0])[0] = 3

    #-----------player bullet collision and rendering ----------
        for bullet in playerbullets:
            if bullet[0] > spriterect[0]:
                if bullet[0] < spriterect[0] + sprite.width:
                    if bullet[1] < spriterect[1] + sprite.height:
                        if bullet[1] > spriterect[1]:
                            (enemy[0])[1] -= 1
                            if (enemy[0])[1] == 0:
                                current_level.remove(enemy)
                                score += 100*(enemy[0])[0]
                            playerbullets.remove(bullet)
                            meta_update()

    for bullet in playerbullets:
        pygame.draw.rect(mainscreen,(255,255,255),(bullet[0]-playerbulletwidth/2,bullet[1],playerbulletwidth,playerbulletheight))
        bullet[1] -= 5
        if bullet[1] < 0 - playerbulletheight:
            playerbullets.remove(bullet)
            meta_update()
    
#-----enemy bullet rendering-----

    for bullet in enemybullets:
        if bullet[2] == 1:
            bulletcolour = (255,255,0)
        elif bullet[2] == 2:
            bulletcolour = (255,120,0)
        elif bullet[2] == 3:
            bulletcolour = (255,0,0)

        pygame.draw.rect(mainscreen,bulletcolour,(bullet[0]-enemybulletwidth/2,bullet[1],enemybulletwidth,enemybulletheight))
        bullet[1] += 3
        if bullet[2] == 2:
            if bullet[0] < player.x + player.width // 2:
                bullet[0] += 1
            elif bullet[0] > player.x + player.width // 2:
                bullet[0] -= 1
        elif bullet[2] == 3:
            bullet[0] += randint(-4,3)
        if bullet[1] > 695:
            enemybullets.remove(bullet)
        
        for bullet in enemybullets:
            if bullet[0] > player.x:
                if bullet[0] < player.x + player.width:
                    if bullet[1] < player.y + player.height:
                        if bullet[1] > player.y:
                            meta_update()
                            playerhealth -= bullet[2]
                            enemybullets.remove(bullet)

#-------------------INITIAL LOADING AND GAME RESET LOADING---------------------------------------

#this will probably change to some other load screen

#variable resets
def firstload():
    global current_level
    global level
    global playerhealth
    global playerbullets
    global enemybullets
    global playermaxbullets
    level = 1
    playerhealth = 100
    enemybullets = []
    playermaxbullets = 3
    playerbullets = []
    mainscreen.fill(black)
    mainscreen.blit(player.image, (player.x,player.y))
    pygame.draw.rect(mainscreen,(0,0,0),(0,0,1000,700)) #main game window
    pygame.draw.rect(mainscreen,(10,10,10),(0,700,1000,200)) #health/shields bar
    pygame.draw.rect(mainscreen,(255,50,0),(50,750,playerhealth*9,100))
    pygame.draw.rect(mainscreen,(15,15,15),(1000,0,500,900)) #metadata bar
    mainscreen.blit(title_text.render('SYSTEM', False, (255, 255, 255)),(1010,10)) # title text
    mainscreen.blit(main_text.render('Press space to start', False, (255, 255, 255)),(400,350))


    pygame.display.update()
    current_level = loadlevel([
        [1,1],[2,1],[1,1],[1,1],[1,1],[1,1],
        [1,1],[1,1],[1,1],[3,1],[1,1],[1,1],
        [1,1],[1,1],[1,1],[1,1],[1,1],[2,1],
        [1,1]
    ])
firstload()

#---------------------LIVE INPUT, will probably be run at the end of the code-----------------------

def main():
    global prompt_counter
    global score
    live = True
    meta_update()
    while live:
        clock.tick(60)
        textprompt()
        printtext()
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                live = False   

    #------------------------BASIC INPUTS-----------------------------

            if event.type == pygame.KEYDOWN:    #records key presses  
                    
                if event.key == pygame.K_ESCAPE:
                    live = False

                if event.key == pygame.K_q:
                    player.movex -= 1
                if event.key == pygame.K_e:
                    player.movex += 1
                if event.key == pygame.K_w:
                    if len(playerbullets) < playermaxbullets:
                        playerbullets.append([player.x + player.width//2, player.y,powerup])
                        meta_update()

            if event.type == pygame.KEYUP:  #records key unpresses
                if event.key == pygame.K_q:
                    player.movex += 1
                if event.key == pygame.K_e:
                    player.movex -= 1

        #update player position
        player.x = player.x + (playerspeed*player.movex)

        #contain player to main screen
        if player.x < 0:
            player.x = 0
        if player.x > 1000 - player.width:
            player.x = 1000 - player.width

        #---------------UPDATE SCREEN------------------------------------

        pygame.draw.rect(mainscreen,(0,0,0),(0,0,1000,700))
        mainscreen.blit(player.image, (player.x,player.y))
        levelrender()
        if playerhealth <= 0:
            live = False
        pygame.display.update(0,0,1000,700)
    prompt_counter = 2
    firstload()
    while live == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if  event.key == pygame.K_SPACE:
                    prompt_counter = 0
                    score = 0
                    main()
                elif event.key == pygame.K_ESCAPE:
                    return
        textprompt()
        player.movex = 0
        printtext()
        pygame.display.update(100,0,500,700)

live = True
while live:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                live = False
            if event.key == pygame.K_SPACE:
                live = False
                main()
pygame.quit