__author__ = '김진근'

import random
import json
import os
import sys
sys.path.append('../LabsAll/Labs')

from pico2d import *

import game_framework
import title_state

name = "MainState"

player = None
background = None
enemy_s = None
enemy_g = None
boss = None


class Background:

    def __init__(self):
        self.image = load_image('background.png')
        self.y = 0

    def draw(self):

        self.image.clip_draw(0, self.y, 800, 600-self.y, 400, int((600 - self.y)/2))
        self.image.clip_draw(0, 0, 800, self.y, 400, 600 - int(600 - (600 - self.y))/2)

    def update(self):
        self.y += 1

        if(self.y >= 600):
            self.y = 0

######################################################################
class Player:

    def __init__(self):
        self.image = load_image('Player.png')
        # self.x, self.y = 640, 300
        self.x, self.y = 400, 100
        self.frame = 3

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 80, self.x, self.y)

#######################################################################

class Enemy_s:

    image = None

    def __init__(self):
        # self.x, self.y = random.randint(50, 1200), 900
        self.x, self.y = random.randint(50, 750), 650
        self.frame = 8

        if self.image == None:
            self.image = load_image('Scourge.png')

    def update(self):
        self.y -= 3

    def draw(self):
        self.image.clip_draw( self.frame * 34, 280, 34, 30 , self.x, self.y )

########################################################################

class Enemy_g:

    image = None

    def __init__(self):
        # self.x, self.y = random.randint(50, 1200), 900
        self.x, self.y = random.randint(50, 750), 600
        self.frame = 8

        if self.image == None:
            self.image = load_image('Guardian.png')

    def update(self):
        self.y -= 1
        # self.randint = random.randint(1,6)
        # if (self.randint % 2 == 0):
        #     self.x += 10
        #     if ( self.x >= 750 ):
        #         self.x = 750
        #
        # else:
        #     self.x -= 10
        #     if ( self.x <= 50 ):
        #         self.x = 50

    def draw(self):
        self.image.clip_draw( self.frame * 81, 700, 81, 70 , self.x, self.y )

#######################################################################

class Boss:

    image = None

    def __init__(self):
        # self.x, self.y = random.randint(50, 1200), 900
        self.x, self.y = random.randint(50, 750), 550
        self.frame = 8

        if Boss.image == None:
            self.image = load_image('Devourer.png')

    def update(self):
        self.y -= 0.1

    def draw(self):
        self.image.clip_draw( self.frame * 72, 1850, 72, 85 , self.x, self.y )

########################################################################

def handle_events():

    global running, player
    events = get_events()

    for event in events:

        if event.type == SDL_QUIT:
            running = False
            game_framework.quit()

        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
            game_framework.change_state(title_state)

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            player.x += 50
            if player.x >= 800:
                player.x = 800

            player.frame += 1
            if player.frame >= 6:
                player.frame = 6

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            player.x -= 50
            if player.x <= 20:
                player.x = 20

            player.frame -= 1
            if player.frame <= 0:
                player.frame = 0

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            player.y += 30
            if player.y >= 550:
                player.y = 550

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            player.y -= 30
            if player.y <= 50:
                player.y = 50

#############################################################################

def enter():

    global background, player, enemy_s, enemy_g, boss

    background = Background()
    player = Player()
    enemy_s = Enemy_s()
    enemy_g = Enemy_g()
    boss = Boss()

######################################################################
def exit():
    global background, player, enemy_s, enemy_g, boss
    del(background)
    del(player)
    del(boss)
    del(enemy_s)
    del(enemy_g)

    close_canvas()

######################################################################

def pause():
    pass


def resume():
    pass

#########################################################################

def update():

        background.update()
        enemy_s.update()
        enemy_g.update()
        boss.update()


#############################################################################

def draw():

        handle_events()
        clear_canvas()

        background.draw()
        player.draw()
        enemy_s.draw()
        enemy_g.draw()
        boss.draw()

        update_canvas()

#############################################################################

def main():

    enter()
    while running:

        handle_events()
        update()
        draw()
    exit()

####################################################################

if __name__ == '__main__':
    main()
