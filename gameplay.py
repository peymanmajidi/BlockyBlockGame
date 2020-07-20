import random, pygame, menu, time, os
from contants import GREEN
import menu as Menu
import threading as thread


def random_color_generator():
    return (random.randrange(1,255),random.randrange(1,255),random.randrange(1,255))

def play_audio(soundname):
    pygame.mixer.music.load("assets/sounds/"+soundname)
    pygame.mixer.music.play(0)

def change_paint_color(key):
    paint_color = GREEN
    if key == pygame.K_RSHIFT:
        paint_color = random_color_generator()

    if key == pygame.K_b:
        paint_color = (0,0,0)
        
    if key == pygame.K_r:
        paint_color = (255,0,0)
        
    if key== pygame.K_g:
        paint_color = (0,255,0)
        
    if key == pygame.K_y:
        paint_color = (255,255,0)

    return paint_color


def auto_generate_blocky(screen, BlockyBlock):    
    BlockyBlock.Generate_blocky(screen)
    thread.Timer(3, auto_generate_blocky, [screen, BlockyBlock]).start()



def game_loop(window, events, BlockyBlock):
    game_over = False
    for event in events.get():
        if event.type == pygame.QUIT:
            game_over= True

        if event.type == pygame.MOUSEBUTTONDOWN: # mouse click event
            x,y = event.pos
            if BlockyBlock.select(x,y, Character_Size.Normal):
                clicked = False
            else:
                clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        try:
            if clicked:
                x2,y2 = event.pos
                pygame.draw.rect(window, paint_color, [x2,y2,20,20],0)
                pygame.display.update()
        except:
            pass         
        if event.type == pygame.KEYDOWN:
            pygame.display.update()
            BlockyBlock.action_manager(event.key)

            if event.key == pygame.K_TAB:
                BlockyBlock.Generate_blocky(window)

            paint_color = change_paint_color(event.key)
            menu.mouse_color(window, paint_color)
                
            if event.key == pygame.K_c: # clear all drawing
                pygame.draw.rect(window, BLACK, [0,0,WIDTH, HEIGHT],0)
                BlockyBlock.render_all()
    return game_over