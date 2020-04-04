from libraries import *
from game_contants import *

window = pygame.display.set_mode((WIDTH, HEIGHT))

class BlockyBlock:
    players = list()
    def __init__(self, character_name, color, x=0, y=0, emotion = Emotion.NORMAL):
        self.id = BlockyBlock.players.__len__()
        self.name = character_name
        self.color = color
        self.primecolor = color
        self.eyes = Eyes()
        self.x = x
        self.y = y
        self.emotion = emotion
        self.jumping = False
        self.rising = False
        self.falling = False
        self.fall_played = True
        self.fall = 0
        self.rise= 0
        self.alive = True
        self.selected = False
        self.direction = Direction.FRONT
        self.input = Input(SECONDARY_INPUT)
        if x == 0:
            self.x = int(CHARCTER) * 5
        if y == 0:
            self.y = int(CHARCTER)

        BlockyBlock.players.append(self)
        self.render_character()

    # static methods:
    def event_listener(keys):
        for player in BlockyBlock.players:
            player.event_handler(keys)

    def action_manager(key):
        for player in BlockyBlock.players:
            player.action(key)

    def select(x, y):
        for player in BlockyBlock.players:
            if (x >= player.x and x <= (player.x + CHARCTER)) and (y <= (player.y + CHARCTER) and y >= player.y):
                if player.alive:
                    player.select_me()
                return True
        return False
    
    def render_all():
        for player in BlockyBlock.players:
            player.render_character()




    # nonstatic methods:
    def select_me(self):
        if self.alive == False:
            return
        list_of_selected = list(filter(lambda b: b.selected == True and b.alive == True, BlockyBlock.players))
        for selected in list_of_selected:
            selected.color = selected.primecolor
            selected.assign_keystrock(SECONDARY_INPUT)
            selected.emotion = Emotion.NORMAL
            selected.selected = False # deselect all
            selected.render_character()
        self.selected = True
        self.color = WHITE
        self.emotion = Emotion.HAPPY
        self.assign_keystrock(STANDARD_INPUT)
        self.render_character()

    def assign_keystrock(self, input):
        self.input = input

    def set_x(self, x):
        if x + CHARCTER >= WIDTH:
            x = WIDTH - CHARCTER - 1
        if x < 3:
            x = 3
        self.x = x

    def set_y(self, y):
        if y + CHARCTER >= HEIGHT:
            y = HEIGHT - CHARCTER - 1
        if y < 3:
            y = 3
        self.y = y


    def render_character(self, emo = Emotion.NOT_SET):
        x = self.x
        y = self.y
        if emo == Emotion.NOT_SET:
            emo = self.emotion
        pygame.draw.rect(window, self.color, [ x ,y  , CHARCTER , CHARCTER ], 0 ) # [ ]
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

        if self.alive:
            if  self.eyes.keep > 5: # winking
                pygame.draw.circle(window, BLACK, self.eyes.left.get(), int(CHARCTER / 15),0)
                pygame.draw.circle(window, BLACK, self.eyes.right.get(),int(CHARCTER / 15),0) 
                self.eyes.wink_period = random.randrange(100,1000) # random period for winking
            else:  # normal
                pygame.draw.circle(window, BLACK,self.eyes.left.get(),int(CHARCTER / 10),0)
                pygame.draw.circle(window, BLACK,self.eyes.right.get(),int(CHARCTER / 10),0) 
        else: # renser eyes when blocky is dead X:
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/10)+5,y+ int(CHARCTER/8)+2),(x + int(CHARCTER/3)+5,y+ int(CHARCTER/3)+5))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/10)+5,y+ int(CHARCTER/8)+2+1),(x + int(CHARCTER/3)+5,y+ int(CHARCTER/3)+5+1))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/10)+5,y+ int(CHARCTER/8)+2+2),(x + int(CHARCTER/3)+5,y+ int(CHARCTER/3)+5+2))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/3)+5,y+ int(CHARCTER/8)+2),(x + int(CHARCTER/10)+5,y+ int(CHARCTER/3)+5))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/3)+5,y+ int(CHARCTER/8)+2+1),(x + int(CHARCTER/10)+5,y+ int(CHARCTER/3)+5+1))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/3)+5,y+ int(CHARCTER/8)+2+2),(x + int(CHARCTER/10)+5,y+ int(CHARCTER/3)+5+2))

            pygame.draw.line(window, BLACK, (x + int(CHARCTER/10) + int(CHARCTER/2),y+ int(CHARCTER/8)+2),(x + int(CHARCTER/3)+ int(CHARCTER/2),y+ int(CHARCTER/3)+5))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/10) + int(CHARCTER/2),y+ int(CHARCTER/8)+2+1),(x + int(CHARCTER/3)+ int(CHARCTER/2),y+ int(CHARCTER/3)+5+1))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/10) + int(CHARCTER/2),y+ int(CHARCTER/8)+2+2),(x + int(CHARCTER/3)+ int(CHARCTER/2),y+ int(CHARCTER/3)+5+2))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/3)+ int(CHARCTER/2),y+ int(CHARCTER/8)+2),(x + int(CHARCTER/10)+ int(CHARCTER/2),y+ int(CHARCTER/3)+5))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/3)+ int(CHARCTER/2),y+ int(CHARCTER/8)+2+1),(x + int(CHARCTER/10)+ int(CHARCTER/2),y+ int(CHARCTER/3)+5+1))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/3)+ int(CHARCTER/2),y+ int(CHARCTER/8)+2+2),(x + int(CHARCTER/10)+ int(CHARCTER/2),y+ int(CHARCTER/3)+5+2))
        
    
        if emo == Emotion.SAD: # :(
            pygame.draw.arc(window, BLACK, (x+( int(CHARCTER/7)),y+int(CHARCTER/1.7) , CHARCTER-int(CHARCTER / 5), CHARCTER-int(CHARCTER / 5)), math.pi/4,3* math.pi / 4 , int(CHARCTER / 10))
        elif emo == Emotion.HAPPY: # :)
            pygame.draw.arc(window, BLACK, (x+int(CHARCTER / 10),y , CHARCTER-int(CHARCTER / 5), CHARCTER-int(CHARCTER / 5)), 5*math.pi/4,7* math.pi / 4 , int(CHARCTER / 10))
        elif emo == Emotion.NORMAL or emo == Emotion.DEAD: # :|
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/5),y+ int(CHARCTER/3 * 2)),(x+ CHARCTER - int(CHARCTER/5),y+ int(CHARCTER/3 * 2)))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/5),y+ int(CHARCTER/3 * 2)+1),(x+ CHARCTER - int(CHARCTER/5),y+ int(CHARCTER/3 * 2)+1))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/5),y+ int(CHARCTER/3 * 2)+2),(x+ CHARCTER - int(CHARCTER/5),y+ int(CHARCTER/3 * 2)+2))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/5),y+ int(CHARCTER/3 * 2)+3),(x+ CHARCTER - int(CHARCTER/5),y+ int(CHARCTER/3 * 2)+3))
            pygame.draw.line(window, BLACK, (x + int(CHARCTER/5),y+ int(CHARCTER/3 * 2)+4),(x+ CHARCTER - int(CHARCTER/5),y+ int(CHARCTER/3 * 2)+4))
        elif emo == Emotion.WOW or not self.falling: # :o
            pygame.draw.arc(window, BLACK, (x+int(CHARCTER / 2.5),y+int(CHARCTER / 1.8) , int(CHARCTER / 3.5),  int(CHARCTER / 3.5)), 0,2* math.pi  , int(CHARCTER / 7))


    def clear_shadow(self):
        pygame.draw.rect(window, BLACK, [ self.x, self.y, CHARCTER , CHARCTER ], 0)

    def turn_left(self):
        self.clear_shadow()
        self.direction = Direction.LEFT
        if self.x - MOVE >= 0:
             if not Is_filled_pixel.left(self.x, self.y):
                self.x-= MOVE
             elif not Is_filled_pixel.left(self.x-MOVE+1, self.y-(MOVE*5)):
               self.x-= MOVE
               self.y-= MOVE
        self.pushing_left()
        self.render_character()

    def turn_right(self):
        self.clear_shadow()
        self.direction = Direction.RIGHT
        if self.x + CHARCTER + MOVE <= WIDTH:
             if not Is_filled_pixel.right(self.x, self.y):
                self.x+= MOVE
             elif not Is_filled_pixel.right(self.x + MOVE+1, self.y - (MOVE*5)):
               self.x+= MOVE
               self.y-= MOVE
        self.pushing_right()
        self.render_character()

    def zoom_in(self):
        global CHARCTER
        global JUMP
        if CHARCTER < 400:
            self.y-=10
            CHARCTER+=10
            JUMP = int(CHARCTER * 1.8)
    
    def zoom_out(self):
        global CHARCTER
        global JUMP
        if CHARCTER > 10:
            self.y+=10
            CHARCTER-=10
            JUMP = int(CHARCTER * 1.8)

    def do_jump(self):
        if self.jumping or self.falling:
            return
        self.clear_shadow()
        self.jumping = True
        self.rising = True
        play_audio("jump.wav")
        self.rise=0
        self.render_character()

    def action(self, key):
        if key == self.input.jump:
            self.do_jump()
        elif key == self.input.shot:
            self.shot()


    def event_handler(self, keys): # run every miliseconds
        self.eyes.winking()
        if not Is_filled_pixel.bottom(self.x, self.y) and not self.jumping:
            self.clear_shadow()
            self.y+=1
            self.falling = True
            self.fall_played = True
            self.render_character()
        else:
            self.falling = False
            if self.fall_played:
                play_audio("fall.wav")
                self.fall_played = False

        if(keys[self.input.left]):
            self.turn_left()
            

        elif(keys[self.input.right]):
            self.turn_right()
           

        if self.jumping:
            self.clear_shadow()
            if self.rising:
                self.rise+=1
                if not Is_filled_pixel.top(self.x, self.y-1):
                    self.y-=1
                else:
                    self.jumping = False
            if self.rise > JUMP:
                self.rising = False
                self.jumping= False
            self.render_character()
        


    def pushing_left(self): # pushing other players to left
        x1 = self.x - CHARCTER - 1
        x2 = self.x + (2*CHARCTER) + 1
        y1 = self.y - CHARCTER - 1
        y2 = self.y + (2*CHARCTER) + 1
        players_arround = list(filter(lambda p: x1 <= p.x and x2 >= p.x + CHARCTER and y1 <= p.y and y2 >= p.y + CHARCTER, BlockyBlock.players) )
        for player in players_arround:
            if player.id == self.id:
                continue
            if (self.x == player.x+ CHARCTER ) or (self.x  == player.x+ CHARCTER +1):
                if (self.y - CHARCTER <= player.y-CHARCTER and self.y > player.y-CHARCTER) or ( self.y - CHARCTER > player.y - CHARCTER and self.y - CHARCTER < player.y ):
                    player.turn_left()
    
    def pushing_right(self): # pushing other players to right
        x1 = self.x - CHARCTER - 1
        x2 = self.x + (2*CHARCTER) + 1
        y1 = self.y - CHARCTER - 1
        y2 = self.y + (2*CHARCTER) + 1
        players_arround = list(filter(lambda p: x1 <= p.x and x2 >= p.x + CHARCTER and y1 <= p.y and y2 >= p.y + CHARCTER, BlockyBlock.players) )
        for player in players_arround:
            if player.id == self.id:
                continue
            if (self.x + CHARCTER == player.x) or (self.x + CHARCTER +1 == player.x):
                if (self.y - CHARCTER <= player.y-CHARCTER and self.y > player.y-CHARCTER) or ( self.y - CHARCTER > player.y - CHARCTER and self.y - CHARCTER < player.y ):
                    player.turn_right()

    def kill_me(self):
        self.alive = False
        self.color = DEAD
        self.emotion = Emotion.DEAD
        self.assign_keystrock(NONE_INPUT)
        self.render_character()


    def shot(self):
        
        # killing other players
        if self.direction == Direction.RIGHT:
            laser_x = WIDTH
            x=self.eyes.left.x
            y=self.eyes.left.y
            list_of_blocky = list(filter(lambda p: p.id!= self.id and x < p.x and (y>=p.y and y<= p.y+CHARCTER) ,BlockyBlock.players))
            list_of_blocky.sort(key= lambda p: p.x, reverse= False)
            for p in list_of_blocky:
                p.kill_me()
                laser_x = p.x
                break
        else:
            laser_x = 0
            x=self.eyes.right.x
            y=self.eyes.right.y
            list_of_blocky = list(filter(lambda p:p.id!= self.id and x> p.x and (y>=p.y and y<= p.y+CHARCTER) ,BlockyBlock.players))
            list_of_blocky.sort(key= lambda p: p.x, reverse= True)
            for p in list_of_blocky:
                p.kill_me()
                laser_x = p.x + CHARCTER
                break

        # draw laser
        if self.direction == Direction.RIGHT or  self.direction == Direction.FRONT:
            pygame.draw.line(window, LASER, self.eyes.left.get2(), (laser_x,self.eyes.left.y),int(CHARCTER/10))
            pygame.draw.line(window, LASER2, self.eyes.right.get2(), (laser_x,self.eyes.left.y),int(CHARCTER/10))
        else:
            pygame.draw.line(window, LASER, self.eyes.left.get2(), (laser_x,self.eyes.left.y),int(CHARCTER/10))
            pygame.draw.line(window, LASER2, self.eyes.right.get2(), (laser_x,self.eyes.left.y),int(CHARCTER/10))

        play_audio("laser.wav")

        self.render_character(Emotion.SAD)
        pygame.display.update()
        pygame.time.delay(40)

        # clean laser
        if self.direction == Direction.RIGHT or  self.direction == Direction.FRONT:
            pygame.draw.line(window, BLACK, (self.eyes.left.x +1,self.eyes.left.y-int(CHARCTER/5)), (WIDTH,self.eyes.left.y-int(CHARCTER/5)),int(CHARCTER/2))
        else:
            pygame.draw.line(window, BLACK, (self.eyes.right.x+1,self.eyes.right.y-int(CHARCTER/5)), (0,self.eyes.right.y-int(CHARCTER/5)),int(CHARCTER/2))

        
        
        BlockyBlock.render_all()





class Eyes:
    def __init__(self):
        self.left = Point()
        self.right = Point()
    def move(self, x):
        self.left.x +=x
        self.right.x +=x
    # winking eyes        
    wink = False # last wink status
    wink_idle = 0 # eye winking when blocky is idle
    wink_period = 20
    keep = 0
    def winking(self):
        self.wink_idle +=1 
        if self.wink_idle % self.wink_period == 0:
            self.wink_idle = 0
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


