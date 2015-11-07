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

Missile_List = []

player = None
background = None
enemy_s = None
enemy_g = None
boss = None


class Background:

    def __init__(self):
        self.image = load_image('Background/background.png')
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

    image = None

    STAND, RIGHT_RUN, LEFT_RUN, UP_RUN, DOWN_RUN = 0, 1, 2, 3, 4


    def __init__(self):

        if Player.image == None:
            self.image = load_image('Char/Player.png')
        self.x, self.y = 400, 100
        self.frame = 3
        # self.RIGHT, self.LEFT, self.UP, self.DOWN = False, False, False, False
        self.state = self.STAND


## 캐릭터 상하좌우 컨트롤
    def handle_event(self, event):

        ## 미사일 발사
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            player.missile_shoot()

        ## 좌우 키 눌렀을 때
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in ( self.STAND, self.LEFT_RUN, self.UP_RUN, self.DOWN_RUN ):
                self.state = self.RIGHT_RUN

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in ( self.STAND, self.RIGHT_RUN, self.UP_RUN, self.DOWN_RUN ):
                self.state = self.LEFT_RUN

        ## 좌우 키 뗐을 때
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in ( self.RIGHT_RUN,):
                self.state = self.STAND

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in ( self.LEFT_RUN, ):
                self.state = self.STAND

        ## 상하 키 눌렀을 때
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.STAND, self.DOWN_RUN, self.RIGHT_RUN, self.LEFT_RUN):
                self.state = self.UP_RUN

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.STAND, self.UP_RUN, self.RIGHT_RUN, self.LEFT_RUN):
                self.state = self.DOWN_RUN

        ## 상하 키 뗐을 때
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state in (self.UP_RUN,):
                self.state = self.STAND

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.DOWN_RUN,):
                self.state = self.STAND


    def update(self):

        if self.state == self.STAND:
            player.frame = 3

        if self.state == self.RIGHT_RUN:
            player.x += 5
            if player.x >= 780:
                player.x = 780

            player.frame += 1
            if player.frame >= 6:
                player.frame = 6


        if self.state == self.LEFT_RUN:
            player.x -= 5
            if player.x <= 20:
                player.x = 20

            player.frame -= 1
            if player.frame <= 0:
                player.frame = 0


        if self.state == self.UP_RUN:
            player.y += 3
            if player.y >= 550:
                player.y = 550


        if self.state == self.DOWN_RUN:
            player.y -= 3
            if player.y <= 50:
                player.y = 50





    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 80, self.x, self.y)

    def missile_shoot(self):
        newmissile = Missile(self.x, self.y)
        Missile_List.append(newmissile)



#########################################################################

class Missile:
    def __init__(self, x, y) :
        self.x, self.y = x, y
        self.image = load_image('Char/missile_1.png')

    def update(self) :
        self.y += 10
        if(self.y > 600) :
            self.y = 0
            del Missile_List[0]

    def draw(self) :
        self.image.draw(self.x, self.y)




#########################################################################

class Enemy_s:

    image = None

    def __init__(self):
        # self.x, self.y = random.randint(50, 1200), 900
        self.x, self.y = random.randint(50, 750), 650
        self.frame = 8
        self.crash = False

        if self.image == None:
            self.image = load_image('Char/Scourge.png')

    def update(self):
        self.y -= 5

        if self.y < 0:
            self.x , self.y = random.randint(50, 750), 650


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
            self.image = load_image('Char/Guardian.png')

    def update(self):
        self.y -= 0.5

        if self.y < 0:
            self.x , self.y = random.randint(50, 750), 650


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
            self.image = load_image('Char/Devourer.png')

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

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
            game_framework.change_state(title_state)

        else:
            player.handle_event(event)




#############################################################################

def enter():

    global background, player, enemy_s_team, enemy_g_team, boss

    background = Background()
    player = Player()
    enemy_s_team = [Enemy_s() for i in range(5) ]
    enemy_g_team = [Enemy_g() for i in range(2) ]
    boss = Boss()
    Missile_List = []


######################################################################
def exit():
    global background, player, enemy_s_team, enemy_g_team, boss
    del(background)
    del(player)
    del(boss)
    del(enemy_s_team)
    del(enemy_g_team)

    close_canvas()

######################################################################

def pause():
    pass


def resume():
    pass

#########################################################################

def update():

        background.update()
        player.update()

        for enemy_s in enemy_s_team:
            enemy_s.update()

        for enemy_g in enemy_g_team:
            enemy_g.update()

        boss.update()

        for missile in Missile_List:
            missile.update()

#############################################################################

def draw():

        handle_events()
        clear_canvas()

        background.draw()
        player.draw()

        for enemy_s in enemy_s_team:
            enemy_s.draw()

        for enemy_g in enemy_g_team:
            enemy_g.draw()

        for missile in Missile_List:
            missile.draw()

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
