import pygame
import time
#Color definition
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
#Rectangle class
class ShapeRect:
    color = WHITE
    x = 0
    y = 0
    height = 0
    width = 0
    def __init__(self,x,y,width,height,color,origin):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.origin = origin
    def draw(self):
        if(self.origin):
            pygame.draw.rect(window,self.color,(self.x - self.width / 2,self.y - self.height / 2,self.width,self.height))
        else:
            pygame.draw.rect(window,self.color,(self.x ,self.y ,self.width,self.height))
#Circle class
class ShapeCircle:
    color = WHITE
    x = 0
    y = 0
    radius = 0
    velocityX = 0
    velocityY = 0
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        
    def draw(self):
        pygame.draw.circle(window,self.color,(self.x,self.y),self.radius)

#Create objects
p = ShapeRect(150,150,50,50,GREEN,True)
enemy = ShapeRect(150,150,50,50,RED,True)
ball = ShapeCircle(400,400,20,BLUE)
line = ShapeRect(0,400,800,5,WHITE,False)
eBase = ShapeRect(400,0,300,5,WHITE,True)
pBase = ShapeRect(400,800,300,5,WHITE,True)
#Initialize temp position of enemy and player
tempP = [p.x,p.y]
tempE = [enemy.x,enemy.y]
enemyVelocity = [0,0]
#Initialize screen size width height
screenSize = (800,800)
#Initialize score count
enemyScore = 0
playerScore = 0

def sgn(a):
    if(a < 0):
        return -1
    else:
        return 1

def movEnemy():
    enemyVelocity[0] = sgn(ball.x - enemy.x) * 5
    enemyVelocity[1] = sgn(ball.y - enemy.y) * 8

    enemy.x += enemyVelocity[0]
    enemy.y += enemyVelocity[1]
    if(line.y - enemy.y < enemy.height / 2 + line.height):
        enemy.y = line.y + line.height - enemy.height / 2 - 10

def score():
    flag = 0
    global playerScore,enemyScore
    if(ball.y - eBase.y <= ball.radius + eBase.height / 2 and abs(ball.x - eBase.x) <= ball.radius + eBase.width / 2):
        playerScore += 1
        flag = 1
    elif(pBase.y - ball.y <= ball.radius + pBase.height / 2 and abs(ball.x - pBase.x) <= ball.radius + pBase.width / 2):
        enemyScore += 1
        flag = 1
    #Init game when scored
    if(flag == 1):
        enemy.x = 350
        enemy.y = 100
        ball.x = 400
        ball.y = 400
        ball.velocityX = 0
        ball.velocityY = 0
        
def hitBall():
    #If ball hits base , increase score count
    score()
    #Ball hit player and enemy
    if(abs(ball.y - p.y )  <= p.height / 2 + ball.radius and abs(ball.x - p.x )  <= p.width / 2 + ball.radius):
        ball.velocityY = int((ball.y - p.y) * (abs(p.y - tempP[1]) + 1) / 30)
        ball.velocityX = int((ball.x - p.x) * (abs(p.x - tempP[0]) + 1) / 30)
    elif(abs(ball.y - enemy.y ) <= enemy.height / 2 + ball.radius and abs(ball.x - enemy.x ) <= enemy.width / 2 + ball.radius):
        ball.velocityY = sgn(ball.y - enemy.y) * 5 + 10
        ball.velocityX = sgn(ball.x - enemy.x) * 5 + 10
    #Ball hits the wall
    if(ball.y + ball.radius >= screenSize[1] or ball.y - ball.radius <= 0 ):
        ball.velocityY = - ball.velocityY
    if(ball.x + ball.radius >= screenSize[0] or ball.x - ball.radius <= 0):
        ball.velocityX = - ball.velocityX
    #Move the ball
    ball.y += ball.velocityY
    ball.x += ball.velocityX

def collusionDetection():
    if(p.y - line.y <= p.height / 2 + line.height):
        p.y = line.y + line.height + p.height / 2
def screenUpdate():
    window.fill((0,0,0))
    #Position of player before change
    tempP[0] = p.x
    tempP[1] = p.y
    #move player and enemy
    p.x,p.y = pygame.mouse.get_pos()
    movEnemy()
    #Collusion detection
    collusionDetection()
    hitBall()
    #Draw objects
    enemyScoreRenderer = font.render(str(enemyScore),1,(255,255,0))
    playerScoreRenderer = font.render(str(playerScore),1,(255,255,0))
    window.blit(enemyScoreRenderer,(350,100))
    window.blit(playerScoreRenderer,(350,600))
    pygame.draw.circle(window,WHITE,(400,400),80,1)
    pBase.draw()
    eBase.draw()
    line.draw()
    ball.draw()
    enemy.draw()
    p.draw()
    #Update the display
    pygame.display.update()

#           *******Main********
pygame.init()

pygame.mouse.set_visible(0)

font = pygame.font.SysFont("monospace",100)

enemyScoreRenderer = font.render(str(enemyScore),1,(255,255,0))
playerScoreRenderer = font.render(str(playerScore),1,(255,255,0))

window = pygame.display.set_mode(screenSize)
pygame.display.set_caption("RectHockey")

run = True
while run:
    time.sleep(1/60)
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run = False
            break
    screenUpdate()
    
pygame.quit()