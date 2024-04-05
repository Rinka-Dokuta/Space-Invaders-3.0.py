import pygame #bring in moduel to handle graphics, input, etc
import random
import time
pygame.init()#Set up game
pygame.display.set_caption("Space invaders!") #Sets window title
Window = pygame.display.set_mode((800, 800)) #Creates game screen
Time = pygame.time.Clock() #Set up clock
gameover = False #Variable to run our game loop
xpos = 400
ypos = 750
moveleft = False
moveright = False
timer = 0;
shoot = 0;
numhits = 0;
lives = 3;
my_font = pygame.font.SysFont('Comic Sans MS', 30)
text_surface = my_font.render('LIVES:', False, (255, 0, 0))
text_surface2 = my_font.render(str(lives), False, (255, 0, 0))
class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1
    def draw(self):
        if self.isAlive == True:
            
            pygame.draw.rect(Window, (250, 250, 250), (self.xpos, self.ypos, 40, 40))
    def move(self, time):
        #reset what direction you're moving every 8 moves
        if timer % 800== 0:
            self.ypos += 100 #moves down
            self.direction *=-1 #flip direction
            return 0 #reset timer to 0
        
        #move every time the timer increases by 100:
        if time % 100 == 0:
            self.xpos+=50*self.direction #move right
            
        return time #doesn't reset if first if statement hasn't executed
    
    def collide(self, BulletX, BulletY):
        if self.isAlive: #Only hit live aliens
            if BulletX > self.xpos: #check if bullet is right of the left side of the alien
                if BulletX < self.xpos + 40: #check if the bullet is left of the right side
                    if BulletY < self.ypos + 40: #check if the bullet is above the alien's botto,
                        if BulletY > self.ypos: #check if the bullet is bellow the top of the alien
                            print("hit!")#for testing
                            self.isAlive = False #set alien to dead
                            return False #set the BULLET to dead
        
        return True #Otherwise keep bullet alive
                    
    
    
class Bullet:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False
        
    def move(self, xpos, ypos):
        if self.isAlive == True: #Only shoot live bullets
            self.ypos-=5 #move up when shot
        if self.ypos < 0: #Check if you've hit the top of the screen
            self.isAlive = False #set to dead
            self.xpos = xpos #reset player position
            self.ypos = ypos
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 255), (self.xpos, self.ypos, 3, 20))
        

class Wall:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.numhits = 0
    def draw(self):
       if self.numhits ==0:
           pygame.draw.rect(Window, (250, 250, 20), (self.xpos, self.ypos, 30, 30))
       if self.numhits ==1:
            pygame.draw.rect(Window, (150, 150, 10), (self.xpos, self.ypos, 30, 30))
       if self.numhits ==2:
            pygame.draw.rect(Window, (50, 50, 0), (self.xpos, self.ypos, 30, 30))
            
            
    def collide(self, BulletX, BulletY):
        if numhits < 3: 
            if BulletX > self.xpos: #check if bullet is right of the left side of the wall
                if BulletX < self.xpos + 40: #check if the bullet is left of the right side
                    if BulletY < self.ypos + 40: #check if the bullet is above the wall botto,
                        if BulletY > self.ypos: #check if the bullet is bellow the top of the wall
                            print("hit!")#for testing
                            self.numhits += 1  
                            return False #set the BULLET to dead
        return True
        
#Instantiate bullet object
bullet = Bullet(xpos+28, ypos) #create bullet object and pass player position
        

armada = [] #create empty list
for i in range (4): #handles rows
    for j in range (9): #handle columns
        armada.append(Alien(j*80+50, i*80+50)) #push aliens into list
        
walls = []
for k in range (4):
    for i in range (2):
        for j in range (3):
            walls.append(Wall(j*30+200*k+50, i*30+600))
            
            
            
class Missile:
    def __init__(self):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False
    
    def move(self):
        if self.isAlive == True: #Only shoot live bullets
            self.ypos+=5 #move down when shot
        if self.ypos > 800: #Check if you've hit the bottom of the screen
            self.isAlive = False #set to dead
            self.xpos = -10 #reset player position
            self.ypos = -10
            
            
    def draw(self, screen):
        if self.isAlive == True:
            pygame.draw.rect(screen, (255, 0, 0), (self.xpos, self.ypos, 3, 20))
    
Missiles = []
for i in range (10):
    Missiles.append(Missile())

while not gameover: #GAME LOOP-----------------------------------
    Time.tick(60) #FPS
    timer += 1
    
    #Input section-----------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True #quit game if x is pressed in top corner
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveleft = True
            if event.key == pygame.K_RIGHT:
                moveright = True
            if event.key == pygame.K_SPACE:
                shoot = True
                
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveleft = False
            if event.key == pygame.K_RIGHT:
                moveright = False
            if event.key == pygame.K_SPACE:
                shoot = False
                
                
        
    
    
    
    #Physics section
    if moveleft == True:
        vx =- 3
    elif moveright == True:
        vx = 3
    else:
        vx = 0
    
    for i in range (len(armada)):
       timer = armada[i].move(timer)
    for i in range (len(Missiles)):
        Missiles[i].move()      
    #shoot bullet
    if shoot == True: #Check keyboard input
        bullet.isAlive = True
        
    if bullet.isAlive == True:
        bullet.move(xpos+28, ypos) #Shoot from player position
        if bullet.isAlive == True:
        #check for collision between bullet and enemy
            for i in range (len(armada)): #check bullet with entire armada's positions
                bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos) #if we hit, set bullet to false
                if bullet.isAlive == False:
                    break
       
       #shoot walls
       
        if bullet.isAlive == True:
        #check for collision between bullet and enemy   
            for i in range (len(walls)): #check bullet with entire list of wall positions
                bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos) #if we hit, set bullet to false
                if bullet.isAlive == False:
                    break
            
    else: #Make bullet follow player when not moving up
        bullet.xpos = xpos + 28
        bullet.ypos = ypos
    
   
    #Check for wall/missile collision
        for i in range(len(walls)): #Check each wall box
            for j in range(len(Missiles)): #against each missle
                if Missiles[j].isAlive == True: #Check if missle is true
                    if walls[i].collide(Missiles[j].xpos, Missiles[j].ypos) == False: #call wall collision for each combo
                        Missiles[j].isAlive = False #kill missile
                        break #stop killing walls if you're dead
   
   
   #2% chance every game loop that a missile will drop from a random alien
    chance = random.randrange(100)
    if chance < 2:
        #print("missle drop!") #for testing
        pick = random.randrange(len(armada))#pick a random alien from the armada
        if armada[pick].isAlive == True:
            for i in range(len(Missiles)): #find the first live missile to move
                if Missiles[i].isAlive == False: #only fire missile to move
                    Missiles[i].isAlive = True #set it to alive
                    Missiles[i].xpos = armada[pick].xpos+5 #set the missle's position to the alien's position
                    Missiles[i].ypos = armada[pick].ypos
                    break
    
    #player/missile collision
    for i in range (len(Missiles)): #check for collision with each missile in list
        if Missiles[i].isAlive: #only get hit by live missiles
            if Missiles[i].xpos > xpos: #check if missile is right of the left side of the player
                if Missiles[i].xpos < xpos + 40: #check if the missile is left of the right side of the player
                    if Missiles[i].ypos < ypos + 40: #check if the missile is above the player's bottom
                        if Missiles[i].ypos > ypos: #check if the missile is below the top of the player
                            lives -= 1
                            time.sleep(1)
                            xpos = 400
                            print("Player hit!") #for testing
    
    
    
    
    
    
    #update player position
    xpos += vx
    
    
    if lives <= 0:
        print("GAME OVER")
        gameover = True
    
    #Render section----------------------------------------------
    
    Window.fill((0, 0, 0))#Wipe screen so it doesn't smear
    
    pygame.draw.rect(Window, (0, 250, 0), (xpos, ypos, 60, 20)) #Draw player
    pygame.draw.rect(Window, (0, 250, 0), (xpos, ypos+10, 70, 20)) #Right Wing
    pygame.draw.rect(Window, (0, 250, 0), (xpos+10, ypos+10, 70, 20)) #Left Wing
    pygame.draw.rect(Window, (0, 250, 0), (xpos+19, ypos-10, 20, 15)) #Blaster
    pygame.draw.rect(Window, (0, 250, 0), (xpos+24, ypos-20, 10, 15)) #Tiny blaster thing
    
    
    
    #draw all aliens in list
    for i in range (len(armada)):
        armada[i].draw()
        
    for i in range (len(walls)):
        walls[i].draw()
    
    for i in range (len(Missiles)):
        Missiles[i].draw(Window)   

    if bullet.isAlive == True:
        bullet.draw(Window)
        
    Window.blit(text_surface, (0,0))
    Window.blit(text_surface2, (100,0))    
    
        
    pygame.display.flip() #This flips the buffer (memory) where stuff has been "drawn" to the actual screen
    
#End game loop---------------------------------------------------
    
pygame.quit() 
