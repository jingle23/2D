__author__ = '김진근'
from pico2d import *
import random
import game_framework
import title_state
import json
import os
import sys
sys.path.append('../LabsAll/Labs')

name = "MainState"

#######################################################################################################

class Background:

    MOVE_PER_SEC = 250

    def __init__(self):
        self.image = load_image('Background/background.png')
        self.y = 0

## 스크롤
    def draw(self):
        self.image.clip_draw(0, self.y, 800, 600-self.y, 400, int((600 - self.y)/2))
        self.image.clip_draw(0, 0, 800, self.y, 400, 600 - int(600 - (600 - self.y))/2)

    def update(self, frame_time):

        speed = frame_time * self.MOVE_PER_SEC
        self.y += speed

        if(self.y >= 600):
            self.y = 0

######################################################################

#===============================================================================#
class Timer :
    def __init__(self) :
        self.time = 0.0
        self.timer = 0.0
        self.min = 0.0
        self.sec = 0.0
        self.boss_count = 0.0
        self.boss_live = False
#--------------------------------------------------#
    def update(self, frame_time) :
        self.timer += frame_time
        self.time += frame_time
        self.boss_count += frame_time
        self.min = int(self.timer/60)
        self.sec = int(self.timer%60)
        self.creat_enemy()
        # self.creat_enemy_boss()
#--------------------------------------------------#
    def creat_enemy(self) : #create enemy plane to 1.5seconds
        if self.time >= 1.5 :
            new_enemy_s = Enemy_s()
            new_enemy_g = Enemy_g()
            enemy_s_list.append(new_enemy_s)
            enemy_g_list.append(new_enemy_g)
            self.time = 0.0
#--------------------------------------------------#
    ## 보스 등장할 조건을 뭐로 하지??? - 생각 후 결정

    # def creat_enemy_boss(self) : #create enemy boss to 10seconds
    #     if (self.boss_count >= 10 and self.boss_live == False) :
    #         self.boss_live = True
    #         new_boss = Boss()
    #         enemy_boss_list.append(new_boss)
    #         self.boss_count = 0.0

#===============================================================================#

class Player:

    MOVE_PER_SEC = 500
    image = None
    STAND, RIGHT_RUN, LEFT_RUN, UP_RUN, DOWN_RUN = 0, 1, 2, 3, 4

    def __init__(self):
        self.x, self.y = 400, 100
        self.frame = 3
        self.state = self.STAND
        self.hp = 100

        if Player.image == None:
            self.image = load_image('Char/Player.png')


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


    def update(self, frame_time):

        move_distance = frame_time * self.MOVE_PER_SEC

        if self.state == self.STAND:
            player.frame = 3

        if self.state == self.RIGHT_RUN:
            player.x += move_distance
            if player.x >= 780:
                player.x = 780

            player.frame += 1
            if player.frame >= 6:
                player.frame = 6


        if self.state == self.LEFT_RUN:
            player.x -= move_distance
            if player.x <= 20:
                player.x = 20

            player.frame -= 1
            if player.frame <= 0:
                player.frame = 0


        if self.state == self.UP_RUN:
            player.y += move_distance
            if player.y >= 550:
                player.y = 550


        if self.state == self.DOWN_RUN:
            player.y -= move_distance
            if player.y <= 50:
                player.y = 50

    def draw_bb(self):
        draw_rectangle( *self.get_bb() )

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 30 , self.y + 40

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 80, self.x, self.y)

    def missile_shoot(self):
        newmissile = Missile(self.x, self.y)
        Missile_List.append(newmissile)

#########################################################################

class Missile:
    MOVE_PER_SEC = 1000

    def __init__(self, x, y) :
        self.x, self.y = x, y
        self.image = load_image('Char/missile_1.png')

    def update(self, frame_time) :
        move_distance = frame_time * self.MOVE_PER_SEC

        self.y += move_distance
        if(self.y > 600) :
            self.y = 0
            del Missile_List[0]

    def draw(self) :
        self.image.draw(self.x, self.y)

    def draw_bb(self):
        draw_rectangle( *self.get_bb() )

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20 , self.y + 30

#########################################################################

class Enemy_Missile:

    SPEED_PER_SEC = 900

    def __init__(self, x, y):
        self.x , self.y = x, y
        self.frame = 0
        self.image = load_image('Char/Guardian.png')

    def update(self, frame_time):
        speed = frame_time * self.SPEED_PER_SEC
        self.y -= speed

        if(self.y < 0) :
            del enemy_missile_list[0]

    def draw(self):
       self.image.clip_draw( self.frame * 35, 0, 35, 60 , self.x, self.y )

#########################################################################

class Enemy_s:

    MOVE_PER_SEC = 1000
    image = None

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 650
        self.frame = 8
        self.hp = 10

        if self.image == None:
            self.image = load_image('Char/Scourge.png')

    def update(self,frame_time):

        speed = frame_time * self.MOVE_PER_SEC
        self.y -= speed

    def draw(self):
        self.image.clip_draw( self.frame * 34, 280, 34, 30 , self.x, self.y )

    def draw_bb(self):
        draw_rectangle( *self.get_bb() )

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20 , self.y + 20

########################################################################

class Enemy_g:
    MOVE_PER_SEC = 200
    SHOT_PER_SEC = 1

    image = None

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 600
        self.frame = 8
        self.hp = 20
        self.missile_count = 0

        if self.image == None:
            self.image = load_image('Char/Guardian.png')

    def update(self, frame_time):
        self.missile_count += frame_time * self.SHOT_PER_SEC
        speed = frame_time * self.MOVE_PER_SEC

        if self.missile_count > 1 :
            self.missile_count = 0
            enemy_missile = Enemy_Missile(self.x, self.y)
            enemy_missile_list.append(enemy_missile)
        self.y -= speed

    def draw(self):
        self.image.clip_draw( self.frame * 81, 700, 81, 70 , self.x, self.y )

    def draw_bb(self):
        draw_rectangle( *self.get_bb() )

    def get_bb(self):
        return self.x - 40, self.y - 30, self.x + 35 , self.y + 30

#######################################################################

class Enemy_s_death :   # 스커지 죽음 모션
    def __init__(self, x, y) :
        self.x, self.y = x, y
        self.frame = 0
        self.image = load_image('Char/Scourge.png')
#--------------------------------------------------#
    def update(self, frame_time) :
        self.frame = (self.frame + 1) % 5
        if (self.frame == 4) :
            return True
        else :
            return False
#--------------------------------------------------#
    def draw(self) :
        self.image.clip_draw( self.frame * 70 ,140, 60, 70 , self.x, self.y)

################################################################################

class Enemy_g_death :   # 가디언 죽음 모션
    def __init__(self, x, y) :
        self.x, self.y = x, y
        self.frame = 0
        self.image = load_image('Char/Guardian.png')
#--------------------------------------------------#
    def update(self, frame_time) :
        self.frame = (self.frame + 1) % 5
        if (self.frame == 4) :
            return True
        else :
            return False
#--------------------------------------------------#
    def draw(self) :
        self.image.clip_draw( self.frame * 110 ,508, 110, 115 , self.x, self.y)

###################################################################################


class Boss:

    image = None

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 550
        self.frame = 8

        if Boss.image == None:
            self.image = load_image('Char/Devourer.png')

    def update(self):
        self.y -= 0.1

    def draw(self):
        self.image.clip_draw( self.frame * 72, 1850, 72, 85 , self.x, self.y )

    def draw_bb(self):
        draw_rectangle( *self.get_bb() )

    def get_bb(self):
        return self.x - 25, self.y - 45, self.x + 40 , self.y + 45

########################################################################
class Boss_death :  # 디바우러 죽음 모션
    def __init__(self, x, y) :
        self.x, self.y = x, y
        self.frame = 0
        self.image = load_image('Char/Devourer.png')
#--------------------------------------------------#
    def update(self, frame_time) :
        self.frame = (self.frame + 1) % 5
        if (self.frame == 4) :
            return True
        else :
            return False
#--------------------------------------------------#
    def draw(self) :
        self.image.clip_draw( self.frame * 110 ,1150, 110, 100 , self.x, self.y)

#######################################################################
def handle_events( frame_time ):

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
def collide(a, b):  # 충돌체크
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True

#############################################################################
class Explosion:    #플레이어 폭발시 호출

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.image = load_image('Char/Explosion.png' )

    def update(self):
        self.frame = (self.frame + 1)  % 16

        if(self.frame == 15):
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(int(self.frame %4)*120, 360-int(self.frame//4)*120, 120, 120, self.x, self.y)

#############################################################################
def enter():

    global background, timer, player, enemy_s_list, enemy_g_list, enemy_boss_list,\
        enemy_missile_list, Missile_List, enemy_death, explosion

    background = Background
    player = Player()
    timer = Timer()

    enemy_s_list = []       # 스커지 리스트
    enemy_g_list = []       # 가디언 리스트
    enemy_boss_list = []    # 디바우러 리스트
    enemy_missile_list = [] # 가디언 미사일 리스트
    Missile_List = []       # 플레이어 미사일 리스트
    enemy_death = []        # 적 폭발 리스트
    explosion = []          # 플레이어 폭발 리스트

######################################################################
def exit():
    del(background)
    del(timer)
    del(player)

    del(enemy_s_list)
    del(enemy_g_list)
    del(Missile_List)
    del(enemy_missile_list)
    del(enemy_death)
    del(explosion)

    close_canvas()

######################################################################
def pause():
    pass
def resume():
    pass
#########################################################################

def update(frame_time):

        background.update( frame_time )
        timer.update( frame_time )
        player.update( frame_time )

        for enemy_s in enemy_s_list:
            enemy_s.update(frame_time)

        for enemy_g in enemy_g_list:
            enemy_g.update(frame_time)

        for missile in Missile_List:
            missile.update(frame_time)

        for missile in enemy_missile_list:
            missile.update(frame_time)

        # 플레이어 미사일 + 스커지 충돌체크
        for player_missile in Missile_List:
            for enemy_s in enemy_s_list:
                if collide( player_missile, enemy_s ):  # 충돌체크가 Ture이면

                    Missile_List.remove( player_missile )
                    enemy_s.hp -= 10
                    if enemy_s.hp <= 0:
                        # 스커지 죽는 draw함수 불러옴
                        enemy_s_kill = Enemy_s_death( enemy_s.x, enemy_s.y )
                        enemy_death.append(enemy_s_kill)
                        enemy_s_list.remove( enemy_s )

        # 플레이어 미사일 + 가디언 충돌체크
        for player_missile in Missile_List:
            for enemy_g in enemy_g_list:
                if collide( player_missile, enemy_g ):

                    Missile_List.remove( player_missile )
                    enemy_g.hp -= 10
                    if enemy_g.hp <= 0:
                        # 가디언 죽는 draw함수 불러옴
                        enemy_g_kill = Enemy_g_death( enemy_g.x, enemy_g.y )
                        enemy_death.append(enemy_g_kill)
                        enemy_g_list.remove( enemy_g )


        # 스커지 몸체 + 플레이어 충돌체크
        for enemy_s in enemy_s_list:
            if collide( enemy_s, player ):
                player.hp -= 100
                enemy_s_list.remove(enemy_s)
                if player.hp <= 0:
                    player_explosion = Explosion(player.x, player.y)
                    explosion.append(player_explosion)

        # 가디언 미사일 + 플레이어 충돌체크
        for enemy_missile in enemy_g_list:
            if collide( enemy_missile, player ):
                enemy_missile_list.remove( enemy_missile )
                player.hp -= 35
                if player.hp <= 0:
                    player_explosion = Explosion(player.x, player.y)
                    explosion.append(player_explosion)


#############################################################################

def draw(frame_time):

        handle_events()
        clear_canvas()

        background.draw()
        player.draw()

        for enemy_s in enemy_s_list:
            enemy_s.draw()

        for enemy_g in enemy_g_list:
            enemy_g.draw()

        for missile in Missile_List:
            missile.draw()

        player.draw_bb()

        for enemy_s in enemy_s_list:
            enemy_s.draw()
            enemy_s.draw_bb()

        for enemy_g in enemy_g_list:
            enemy_g.draw()
            enemy_g.draw_bb()

        for missile in Missile_List:
            missile.draw()
            missile.draw_bb()

        for missile in enemy_missile_list:
            missile.draw()
            missile.draw_bb()

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
