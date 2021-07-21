import pygame
import pygame.display
import random
import math

from pygame import mixer #handles music

pygame.init()  # initialise

# variables for display and location on screen
width = 1200
height = 800
screen = pygame.display.set_mode((width, height))  # create screen with x and y length

#score
score_value = 0
gamefont = pygame.font.SysFont('arial',42) # f
font = pygame.font.SysFont('arial',32) # first param is str of a font downloaded on your computer, size 32
textX = 10 # location
textY = 10

# background
background = pygame.image.load('bg.PNG').convert()  # converts pixel colours NECASSARY
backgroundnew = pygame.transform.scale(background, (width, height), )
#sound
mixer.music.load('theme.mp3')
mixer.music.play(-1) #value gives looped audio

# title and icon
pygame.display.set_caption("Personal Space Invaders")
icon = pygame.image.load('icon.png').convert()  # loads it to compiler
pygame.display.set_icon(icon)

# size of icons from image library
from PIL import Image

im = Image.open("player.png")
playerwidth, playerheight = im.size

im = Image.open("enemy.png")
enemywidth, enemyheight = im.size
# print(playerwidth, playerheight)

# creates images and gives properties

playerImg1 = pygame.image.load('player.png').convert_alpha() # use alpha if normal convert gives rects
#playerImg = pygame.transform.scale(playerImg1, (20, 20), )
playerX = width / 2 - playerwidth / 2  # centres image
playerY = height * 0.8
playerX_Vel = 0
playerY_Vel = 0

# Bullet image
bulletImg = pygame.image.load('bullet.png').convert_alpha()
bulletX = 0
bulletY = playerY
bulletY_Vel = 4
bullet_state = "ready"

# enemy image - makes empty list
enemyImg = []
enemyX = []
enemyY = []
enemyX_Vel = []
enemyY_Vel = []
number_enemies = 4

# fills the lists with type enemies
for i in range(number_enemies):
    enemyImg.append(pygame.image.load('enemy.png').convert_alpha())
    enemyX.append(random.randint(0, width - enemywidth))  # random spawn within range
    enemyY.append(100)
    enemyX_Vel.append(0.5)
    enemyY_Vel.append(50)


# single enemy
# enemyImg = pygame.image.load('enemy.png').convert_alpha()
# enemyX = random.randint(0, width - enemywidth)  # random spawn within range
# enemyY = random.randint(0, height / 2)
# enemyX_Vel = 0.3
# enemyY_Vel = 20

# function for drawing to screen

def show_score(x,y):
    score = font.render("SCORE : " + str(score_value),True, (255,255,255)) # RENDER FIRST :typecast the actual value into str, ?, RGB
    screen.blit(score,(x,y)) #draw it normally using imputs from function for loc

def game_over():
    overtxt = gamefont.render("GAME OVER",True, (255,0,0))
    screen.blit(overtxt,(width/2-50, height/2-50)) #centre screen
    print('game over')

def player(x, y):
    screen.blit(playerImg, (x, y))  # drawing plural bits, overwrites old image


def fire_bullet(x, y):
    global bullet_state  # can be accessed inside the fn
    bullet_state = "fire"
    screen.blit(bulletImg, (x + playerwidth / 2, y - playerheight / 2))  # offsets layer so appears off the player


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))))
    if dist < enemyheight * 0.8:
        return True
    else:
        return False

def scorecheck():
    global score_value
    if bullet_state == "fire":
        score_value += 1

# this is the screen loop - everything must happen inside here
# different events eg. key press must be defined in similar ways
running = True
playsound = True #condition so end sound only plays once
while running:

    #screen.fill((0, 200, 0))  # RGB 0-255
    screen.blit(backgroundnew, (0, 0))  # draws bg on the screen

    for event in pygame.event.get():  # checks all events in loop
        if event.type == pygame.QUIT:  # clicking close is a quit event
            running = False  # exits the infinite loop

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Vel = -2
            if event.key == pygame.K_RIGHT:
                playerX_Vel = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # only fires if bullet is ready ie back at ship
                    bullet_sound = mixer.Sound('pew2.mp3') #loads sounds triggered on event
                    bullet_sound.play() #just plays once
                    bulletX = playerX  # x pos at that moment
                    fire_bullet(bulletX, bulletY)  # triggers bullet fn

        # set velocity back to zero after each key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_Vel = 0

    playerX += playerX_Vel  # updates player position

    # Sets boundaries for player movement - resets position at boundary limit
    if playerX <= 0:
        playerX = 0
    elif playerX >= (width - playerwidth):  # considering image size
        playerX = (width - playerwidth)

    # bullet movement - not called until space bar pressed
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Vel
    if bulletY <= -30:
        bulletY = playerY
        bullet_state = "ready"

    # Enemy movement
    for i in range(number_enemies):
        enemyX[i] += enemyX_Vel[i]  # updates position

        #GAME OVER
        if enemyY[i] > (playerY - playerheight): #only one enemy needs to meet condition
            if playsound:
                scream = mixer.Sound('scream.mp3')  # collision soundclip
                scream.play()
                playsound = False
            for j in range(number_enemies): #all enemies
                enemyY[j] = 2000 #disappear
                enemyY_Vel[j] = 0
                enemyX_Vel[j] = 0
                game_over() #blitz game over message on screen on repeat
                # calls text fn
            #break

        if enemyX[i] <= 0:
            enemyX_Vel[i] = enemyX_Vel[i] * -1  # reverses the direction
            enemyY[i] += enemyY_Vel[i]  # drops vertically
        elif enemyX[i] >= (width - enemywidth):
            enemyX_Vel[i] = enemyX_Vel[i] * -1
            enemyY[i] += enemyY_Vel[i]

        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            scorecheck() # checks if the collision results in a score
            bulletY = playerY  # resets bullet to starting pos and state
            bullet_state = "ready"
            enemyX_Vel[i] = enemyX_Vel[i] * 1.2 #increases drop speed
            enemyX[i] = random.randint(0, width - enemywidth)  # resets enemy to random spawn within range
            enemyY[i] = random.randint(0, 100)

        enemy(enemyX[i], enemyY[i], i)  # draws list of enemies
        player(playerX, playerY)  # draws player - has to be after screen fill
        show_score(textX,textY)

    pygame.display.flip()  # updates screen - do this LAST
