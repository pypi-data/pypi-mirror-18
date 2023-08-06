'''TODO:
        Make a class simulation that includes all these functions
        Make a module for handling inputs?
        Make a module for constants?

'''
from FGAme import conf
conf.set_resolution(800, 700)
from FGAme import *
from .rope import Rope
from .platforms import Platforms
from .player import Player
from .music import Music
from math import fabs
from random import randint
from random import uniform
from .main_menu import MainMenu
import pygame
import os
MIN_ROPE_LENGTH = 50
MAX_ROPE_LENGTH = 300
MIN_POS_SCREEN_X = 100
MAX_POS_SCREEN_X, OFFSCREEN_POS_Y  = conf.get_resolution()

LEVELS = [
    (255, 0, 0, 255),
    (0, 255, 0, 255),
    (0, 0, 255, 255),
    (255, 255, 255, 255),
]

PLAYER = Player()
PLATFORM = Platforms()
ROPE = Rope(PLAYER.obj)
MUSIC = Music()
MAIN_MENU = MainMenu()
PAUSED = False
def start_simul():
    margin(10)
    PLATFORM.add(pos=(pos.middle.x, OFFSCREEN_POS_Y-100))
    start_action = MAIN_MENU.proccess_input()
    if start_action == 0:
        run()
    else:
        # Do nothing
        pass


@listen('frame-enter')
def update():
    move_screen(1)
    for platform in PLATFORM.items:
        if(platform.y < 30):
            PLATFORM.remove(platform)

    if PLAYER.score%100 == 0 and PLAYER.score != 0:
        num_of_platforms = randint(1, 3)
        for i in range(0, num_of_platforms):
            pos_x = uniform(MIN_POS_SCREEN_X, MAX_POS_SCREEN_X)
            PLATFORM.add(pos=(pos_x, OFFSCREEN_POS_Y))
         
    if PLAYER.score%1000 == 0:
        world.background = LEVELS.pop()

    if PLAYER.obj.y < 0:
        exit()
    
    ROPE.update()
    PLAYER.update()
    

dx = 20

@listen('long-press', 'left', dx=-dx)
@listen('long-press', 'right', dx=dx)
def wind(dx):
    PLAYER.obj.vel += (dx, 0)

@listen('key-down', 'space', color=(255, 0, 0), max_length=400)
def hook(color, max_length):
    if ROPE.platform == None:
        for platform in PLATFORM.items:
            if (fabs(platform.pos.x-PLAYER.obj.pos.x) < 30 and \
                platform.pos.y > PLAYER.obj.pos.y and \
                fabs(PLAYER.obj.pos.y - platform.pos.y) < max_length): #Hook only if platform is directly above
                platform.color = color
                PLAYER.obj.color = color
                ROPE.connect(platform)
                break
    else:
        ROPE.remove()
        MUSIC.stop_music() # That's a migué line. Fix that please.
        ROPE.platform.color = (0, 0, 0)
        PLAYER.obj.color = (0, 0, 0)
        ROPE.platform = None

@listen('long-press', 'up', climbing_distance=5)
@listen('long-press', 'down', climbing_distance=-5)
def climb_rope(climbing_distance):
    if ROPE.platform != None:
        direction = ROPE.platform.pos - PLAYER.obj.pos
        direction = direction.normalize()

        direction *= climbing_distance
        norm = ROPE.length - direction.norm()*(climbing_distance/fabs(climbing_distance))
        if norm > MIN_ROPE_LENGTH and norm < MAX_ROPE_LENGTH:
            ROPE.length = norm
        else:
            direction = Vec(0, 0)
        PLAYER.obj.move(direction)
    else:
        #Do nothing
        pass

def move_screen(dy):
    for obj in world:
        if type(obj) is not objects.AABB and type(obj) is not draw.Segment and not PAUSED:
            obj.move(0, -dy)
        
def margin(dx):
    W, H = conf.get_resolution()

    world.add.aabb(shape=(10, H), pos=(dx/2, pos.middle.y), mass='inf')
    world.add.aabb(shape=(10, H), pos=(W - dx/2, pos.middle.y), mass='inf')
@listen('key-down','p')
def stop():
    global PAUSED
    PAUSED = not PAUSED
    #world.toggle_pause()
    #PLAYER.toggle_pause()
    MAIN_MENU.proccess_input()
@listen('key-down', 'x')
def quit_game():
    exit()
