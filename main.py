# Library imports
import pygame
import math
import random
from howToPlay import *
from game_contants import *


class Direction:
    LEFT = '👈'
    FRONT = '🐥'
    RIGHT = '👉'

class Emotion:
    SAD = '😞'
    WOW = '😲'
    HAPPY = '😊'

def play_audio(soundname):
    pygame.mixer.music.load("sounds/"+soundname)
    pygame.mixer.music.play(0)

# Initilize Variables
game_over = False
window = pygame.display.set_mode((WIDTH, HEIGHT))
clicked = False # mouse button down to starting to draw

class Point:
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y
    def set(self, x,y):
        self.x = x
        self.y = y
    def get(self):
        return [self.x, self.y]
    def get2(self):
        return (self.x, self.y)

class Eyes:
    left = Point()
    right = Point()
    def move(self, x):
        self.left.x +=x
        self.right.x +=x
    # winking eyes        
    wink = False # last wink status
    do_winking = 0 # eye winking when blocky is idle
    target = 20
    keep = 0
    def winking(self):
        self.do_winking +=1 
        if self.do_winking % self.target == 0:
            self.do_winking = 0
            self.wink = True
            self.keep = 30
    
        if self.wink:
            self.keep -=1


class Is_filled_pixel:
    def left(x,y):
        for i in range(CHARCTER):
            dot = window.get_at((x-MOVE,y+i))
            if dot[0] > 0:
                return True
            if dot[1] > 0:
                return True
            if dot[2] > 0:
                return True
        return False

    def right(x,y):        
        for i in range(CHARCTER):
            dot = window.get_at((x+MOVE + CHARCTER,y+i))
            if dot[0] > 0:
                return True
            if dot[1] > 0:
                return True
            if dot[2] > 0:
                return True
        return False

    def top(x,y):     
        for i in range(CHARCTER):
            dot = window.get_at((x+i,y-MOVE))
            if dot[0] > 0:
                return True
            if dot[1] > 0:
                return True
            if dot[2] > 0:
                return True
        return False

    def bottom(x,y):
        try:
            for i in range(CHARCTER):
                dot = window.get_at((x+i,y+CHARCTER+MOVE))
                if dot[0] > 0:
                    return True
                if dot[1] > 0:
                    return True
                if dot[2] > 0:
                    return True
        except:
            pass  

        return False

class BlockyBlock:
    title = "Blocky Block"
    eyes = Eyes()
    x= int(CHARCTER)*5
    y= CHARCTER
    jumping = False
    rising = False
    falling = False
    fall_played = True
    fall = 0
    rise= 0
    direction = Direction.FRONT

    # render charcter
    def render_character(self, emo = Emotion.HAPPY): # default face is happy :)
        x = self.x
        y = self.y
        pygame.draw.rect(window, COLOR, [ x ,y  , CHARCTER , CHARCTER ], 0 ) # [ ]
        self.eyes.left.x = x+int(CHARCTER/2)- int(CHARCTER / 5)
        self.eyes.left.y = y+int(CHARCTER/2)-int(CHARCTER / 5)

        self.eyes.right.x = x+int(CHARCTER/2)+int(CHARCTER / 5)
        self.eyes.right.y = y+int(CHARCTER/2)-int(CHARCTER / 5)

        if self.direction == Direction.RIGHT:
            self.eyes.move(int(CHARCTER / 10))
            self.eyes.left.y +=1

        elif self.direction == Direction.LEFT:
            self.eyes.move(-int(CHARCTER / 10))
            self.eyes.right.y +=1


        if  self.eyes.keep > 5:
            pygame.draw.circle(window, BLACK, self.eyes.left.get(), int(CHARCTER / 15),0) #[.]
            pygame.draw.circle(window, BLACK, self.eyes.right.get(),int(CHARCTER / 15),0) # [..]
            self.eyes.target = random.randrange(100,1000) # random period for winking
        else:       
            pygame.draw.circle(window, BLACK,self.eyes.left.get(),int(CHARCTER / 10),0) #[.]
            pygame.draw.circle(window, BLACK,self.eyes.right.get(),int(CHARCTER / 10),0) # [..]
        
    
        if emo == Emotion.SAD:
            pygame.draw.arc(window, BLACK,  (x+(x+int(CHARCTER / 10)),y+(x+int(CHARCTER / 2)) , CHARCTER-int(CHARCTER / 5), CHARCTER-int(CHARCTER / 5)), math.pi/4,3* math.pi / 4 , int(CHARCTER / 10)) # :(

        elif not self.falling:
            pygame.draw.arc(window, BLACK,  (x+int(CHARCTER / 10),y , CHARCTER-int(CHARCTER / 5), CHARCTER-int(CHARCTER / 5)), 5*math.pi/4,7* math.pi / 4 , int(CHARCTER / 10)) # :)
        else:
            pygame.draw.arc(window, BLACK,  (x+int(CHARCTER / 2.5),y+int(CHARCTER / 1.8) , int(CHARCTER / 3.5),  int(CHARCTER / 3.5)), 0,2* math.pi  , int(CHARCTER / 7)) # :O

    def clear_shadow(self):
        pygame.draw.rect(window, BLACK, [ self.x, self.y, CHARCTER , CHARCTER ], 0 )

    def shot(self):
        global dir
        global WIDTH
        self.render_character(Emotion.SAD)

        eyes2 = Eyes()
        eyes2.left = self.eyes.left
        eyes2.right = self.eyes.right
        
        # draw laser
        if self.direction == Direction.RIGHT or  self.direction == Direction.FRONT:
            pygame.draw.line(window, LASER, eyes2.left.get2(), (WIDTH,eyes2.left.y),int(CHARCTER/10))
            pygame.draw.line(window, LASER2, eyes2.right.get2(), (WIDTH,eyes2.left.y),int(CHARCTER/10))
        else:
            pygame.draw.line(window, LASER, eyes2.left.get2(), (0,eyes2.left.y),int(CHARCTER/10))
            pygame.draw.line(window, LASER2, eyes2.right.get2(), (0,eyes2.left.y),int(CHARCTER/10))

        play_audio("laser.wav")

        pygame.display.update()
        pygame.time.delay(50)
        self.render_character(Emotion.SAD)

        # clean laser
        if self.direction == Direction.RIGHT or  self.direction == Direction.FRONT:
            pygame.draw.line(window, BLACK, (eyes2.left.x +1,eyes2.left.y-int(CHARCTER/5)), (WIDTH,eyes2.left.y-int(CHARCTER/5)),int(CHARCTER/2))
        else:
            pygame.draw.line(window, BLACK, (eyes2.right.x+1,eyes2.right.y-int(CHARCTER/5)), (0,eyes2.right.y-int(CHARCTER/5)),int(CHARCTER/2))

        pygame.display.update()

def draw_object(pygame, window,WIDTH, HEIGHT):
    pygame.draw.rect(window, OBJECT4, [ WIDTH - WIDTH / 2 ,HEIGHT-70 , 170 , 70 ], 0 )
    pygame.draw.rect(window, OBJECT4, [ 5 ,5, WIDTH-5 , HEIGHT-5 ], 15 ) # GAME BOARD

# Initiate pygame
pygame.init()
pygame.display.set_caption(BlockyBlock.title)
pygame.display.update()

def print_current_color(): 
    pygame.draw.rect(window, OBJECT_COLOR, [0,0,30,10],0)

PrintHelpOnConsole()
blocky = BlockyBlock() # make a blocky character
# Main Game Loop
while not game_over:    
    draw_object(pygame, window, WIDTH, HEIGHT)
    print_current_color()
    surface = pygame.Surface((WIDTH,HEIGHT))
    
    blocky.render_character()

    pygame.display.update()
    me= window.get_at((0,0))
    blocky.eyes.winking()
    if blocky.falling:
        pygame.time.delay(2)
    else:
        pygame.time.delay(4)

    keys = pygame.key.get_pressed()  #checking pressed keys

    if keys[pygame.K_LEFT]:
        blocky.clear_shadow()
        dir =Direction.LEFT
        if blocky.x - MOVE >= 0:
             me= window.get_at((blocky.x-1, blocky.y+ CHARCTER))
             if not Is_filled_pixel.left(blocky.x, blocky.y):
                blocky.x-= MOVE
             elif not Is_filled_pixel.left(blocky.x-MOVE+1, blocky.y-(MOVE*5)):
               blocky.x-= MOVE
               blocky.y-= MOVE

    
    if keys[pygame.K_RIGHT]:
        blocky.clear_shadow()
        dir = Direction.RIGHT
        if blocky.x + CHARCTER + MOVE <= WIDTH:
             me= window.get_at((blocky.x+1+ CHARCTER,blocky.y+CHARCTER))
             if not Is_filled_pixel.right(blocky.x, blocky.y):
                blocky.x+= MOVE
             elif not Is_filled_pixel.right(blocky.x + MOVE+1, blocky.y - (MOVE*5)):
               blocky.x+= MOVE
               blocky.y-= MOVE

    if blocky.jumping:
        blocky.clear_shadow()
        if blocky.rising:
            blocky.rise+=1
            if not Is_filled_pixel.top(blocky.x, blocky.y-1):
                blocky.y-=1
            else:
                blocky.jumping = False
            if blocky.rise > JUMP:
                blocky.rising = False
                blocky.jumping= False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over= True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = not clicked


        try:
            if clicked:
                x2,y2 = event.pos
                pygame.draw.rect(window, OBJECT_COLOR, [x2,y2,20,20],0)
                pygame.display.update()

        except:
            pass         

        if event.type == pygame.KEYDOWN:
            blocky.clear_shadow()
            blocky.clear_shadow()
            pygame.display.update()
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if blocky.jumping or blocky.falling:
                    break
                blocky.clear_shadow()
                blocky.jumping = True
                blocky.rising = True
                play_audio("jump.wav")
                blocky.rise=0
            
            if event.key == pygame.K_RETURN:
                blocky.shot()
            if event.key == pygame.K_c:
                pygame.draw.rect(window, BLACK, [0,0,WIDTH, HEIGHT],0)

            

            if event.key == pygame.K_RSHIFT:
                OBJECT_COLOR = (random.randrange(1,255),random.randrange(1,255),random.randrange(1,255))
    
            if event.key == pygame.K_b:
                OBJECT_COLOR = (0,0,0)
                
            if event.key == pygame.K_r:
                OBJECT_COLOR = (255,0,0)
                
            if event.key == pygame.K_g:
                OBJECT_COLOR = (0,255,0)
                
            if event.key == pygame.K_y:
                OBJECT_COLOR = (255,255,0)
                
            if event.key == pygame.K_KP_PLUS or  event.key ==pygame.K_PLUS or event.key == pygame.K_l:
                if CHARCTER <400:
                    y-=10
                    CHARCTER+=10
                    JUMP = int(CHARCTER * 1.8)
                    
            if event.key == pygame.K_MINUS or  event.key ==pygame.K_KP_MINUS:
                if CHARCTER > 10:
                    y+=10
                    CHARCTER-=10
                    JUMP = int(CHARCTER * 1.8)
                
    


    if not Is_filled_pixel.bottom(blocky.x, blocky.y) and not blocky.jumping:
        blocky.clear_shadow()
        blocky.y+=1
        blocky.falling = True
        blocky.fall_played = True
    else:
        blocky.falling = False
        if blocky.fall_played:
            play_audio("fall.wav")
            blocky.fall_played = False

