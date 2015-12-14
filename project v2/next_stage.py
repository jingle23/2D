__author__ = '김진근'

import random
from pico2d import *

import game_framework
import title_state
import gameover_state

name = "MainState"

player = None
background = None
enemy_s = None
enemy_g = None
boss = None

frame_time = 0
current_time =0.0

################################################################################################
class Timer :
    global frame_time
    font = None
    def __init__(self) :
        self.font = load_font('Background/HYWULB.TTF', 25)
        self.time = 0.0
        self.timer = 0.0
        self.scnt = 0   # 스커지 생성 수
        self.gcnt = 0   # 가디언 생성 수
        self.bcnt = 0   # 보스 생성 수

        self.score = 0  # 점수
        self.skill = 3  # 사용가능 스킬 횟수
#--------------------------------------------------------------------------------------------#
    def update(self, frame_time) :
        self.time += frame_time

        if self.time >= 0.4:
            self.create_enemy_s()
            self.scnt += 1.2
            self.time = 0

        if self.scnt >= 3:
            self.create_enemy_g()
            self.gcnt += 1
            self.scnt = 0

        if (self.gcnt >= 30) and (self.bcnt == 0) :
            self.create_enemy_boss()
            self.bcnt = 1
            self.gcnt = 0

        if self.score >= 10:
            self.skill += 1
            self.score = 0

#--------------------------------------------------------------------------------------------#
    def draw(self) :
        self.font.draw(0, 580, " Score : %02d " %(self.score), (255, 255, 255))
        self.font.draw(600, 580, " Skill Point : %01d " %(self.skill), (255, 255, 255))
        self.font.draw(0, 20, " Shild : %03d"  %(player.hp), (255, 255, 255))


    def create_enemy_s(self) :
        new_enemy_s = Enemy_s()
        enemy_s_list.append(new_enemy_s)
#--------------------------------------------------------------------------------------------#
    def create_enemy_g(self):
        new_enemy_g = Enemy_g()
        enemy_g_list.append(new_enemy_g)
#--------------------------------------------------#
    def create_enemy_boss(self) :
        new_enemy_boss = Boss()
        enemy_boss_list.append(new_enemy_boss)

################################################################################################
class Background:

    def __init__(self):
        self.bgm = load_music('Sound/terran-2.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        self.image = load_image('Background/background3.png')
        self.y = 0
#--------------------------------------------------------------------------------------------#
    def draw(self):
        self.image.clip_draw(0, self.y, 800, 600-self.y, 400, int((600 - self.y)/2))
        self.image.clip_draw(0, 0, 800, self.y, 400, 600 - int(600 - (600 - self.y))/2)
#--------------------------------------------------------------------------------------------#
    def update(self,frame_time):
        self.y += 1
        if(self.y >= 600):
            self.y = 0

        if player.hp <= 0:
            self.bgm.set_volume(0)
################################################################################################
class Player:

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    image = None
    STAND, RIGHT_RUN, LEFT_RUN, UP_RUN, DOWN_RUN = 0, 1, 2, 3, 4

    def __init__(self):
        self.x, self.y = 400, 100
        self.frame = 3
        self.state = self.STAND
        self.hp = 200
        self.speed = 250
        self.total_frame = 0

        self.shoot_sound = load_wav('Sound/missile.wav')
        self.shoot_sound.set_volume(13)
        self.sdeath_sound = load_wav('Sound/Sdeath.wav')
        self.sdeath_sound.set_volume(20)
        self.gdeath_sound = load_wav('Sound/Gdeath.wav')
        self.gdeath_sound.set_volume(35)
        self.ddeath_sound = load_wav('Sound/Ddeath.wav')
        self.ddeath_sound.set_volume(30)
        self.hit_sound = load_wav('Sound/hit.wav')
        self.hit_sound.set_volume(30)
        self.skill_sound = load_wav('Sound/Skill.wav')
        self.skill_sound.set_volume(30)

        if Player.image == None:
            self.image = load_image('Char/Player.png')
#--------------------------------------------------------------------------------------------#
    def handle_event(self, event):

        ## 미사일 발사
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            player.missile_shoot()
            player.sound()

        # 스킬1 사용
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
            player.sound6()
            if timer.skill >= 1:
                player.skill_shoot()
                timer.skill -= 1

        # 스킬2 사용
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_c):
            if timer.skill >= 1:
                player.speed += 100
                timer.skill -= 1
#--------------------------------------------------------------------------------------------#
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
#--------------------------------------------------------------------------------------------#
    def update(self, frame_tim):
        self.total_frame += frame_time
        self.total_frame += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time

        if self.state == self.STAND:
            player.frame = 3

        if self.state == self.RIGHT_RUN:
            player.x += self.speed * frame_time
            if player.x >= 780:
                player.x = 780
            player.frame += 1
            if player.frame >= 6:
                player.frame = 6

        if self.state == self.LEFT_RUN:
            player.x -= self.speed * frame_time
            if player.x <= 20:
                player.x = 20
            player.frame -= 1
            if player.frame <= 0:
                player.frame = 0

        if self.state == self.UP_RUN:
            player.y += self.speed * frame_time
            if player.y >= 550:
                player.y = 550

        if self.state == self.DOWN_RUN:
            player.y -= self.speed * frame_time
            if player.y <= 50:
                player.y = 50
#--------------------------------------------------------------------------------------------#
    def draw_bb(self):
        draw_rectangle( *self.get_bb() )
#--------------------------------------------------------------------------------------------#
    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 30 , self.y + 40
#--------------------------------------------------------------------------------------------#
    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 80, self.x, self.y)
#--------------------------------------------------------------------------------------------#
    def missile_shoot(self):
        newmissile = Missile(self.x, self.y)
        Missile_List.append(newmissile)
#--------------------------------------------------------------------------------------------#
    def skill_shoot(self):
        newmissile = Skill(self.x, self.y + 200)
        skill_list.append(newmissile)
#--------------------------------------------------------------------------------------------#
    def sound(self):
        self.shoot_sound.play()
#--------------------------------------------------------------------------------------------#
    def sound2(self):
        self.sdeath_sound.play()
#--------------------------------------------------------------------------------------------#
    def sound3(self):
        self.gdeath_sound.play()
#--------------------------------------------------------------------------------------------#
    def sound4(self):
        self.ddeath_sound.play()
#--------------------------------------------------------------------------------------------#
    def sound5(self):
        self.hit_sound.play()
#--------------------------------------------------------------------------------------------#
    def sound6(self):
        self.skill_sound.play()
################################################################################################
class Missile:

    def __init__(self, x, y) :
        self.x, self.y = x, y
        self.image = load_image('Char/missile_1.png')
#--------------------------------------------------------------------------------------------#
    def update(self, frame_time) :
        self.y += 500 * frame_time
#--------------------------------------------------------------------------------------------#
    def draw(self) :
        self.image.draw(self.x, self.y)
#--------------------------------------------------------------------------------------------#
    def draw_bb(self):
        draw_rectangle( *self.get_bb() )
#--------------------------------------------------------------------------------------------#
    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20 , self.y + 30
################################################################################################
class Enemy_Missile:

    def __init__(self, x, y):
        self.x , self.y = x, y
        self.frame = 0
        self.image = load_image('Char/Guardian.png')
#--------------------------------------------------------------------------------------------#
    def update(self, frame_time):
        self.y -= 700 * frame_time
#--------------------------------------------------------------------------------------------#
    def draw(self):
       # self.image.clip_draw( self.frame * 35, 0, 35, 60 , self.x, self.y, 52, 90 )
        self.image.clip_draw( 0, 0, 35, 60 , self.x, self.y, 52, 90 )
#--------------------------------------------------------------------------------------------#
    def draw_bb(self):
        draw_rectangle( *self.get_bb() )
#--------------------------------------------------------------------------------------------#
    def get_bb(self):
        return self.x - 18, self.y - 22, self.x + 18 , self.y + 22

################################################################################################
class Boss_Left_Missile:

    def __init__(self, x, y):
        self.x , self.y = x, y
        self.frame = 0
        self.image = load_image('Char/Guardian.png')
#--------------------------------------------------------------------------------------------#
    def update(self, frame_time):
        # self.x -= self.x / self.y
        self.x -= 2
        self.y -= 500 * frame_time
#--------------------------------------------------------------------------------------------#
    def draw(self):
       # self.image.clip_draw( self.frame * 35, 0, 35, 60 , self.x, self.y, 52, 90 )
        self.image.clip_draw( 0, 0, 35, 60 , self.x, self.y, 52, 90 )
#--------------------------------------------------------------------------------------------#
    def draw_bb(self):
        draw_rectangle( *self.get_bb() )
#--------------------------------------------------------------------------------------------#
    def get_bb(self):
        return self.x - 18, self.y - 22, self.x + 18 , self.y + 22

################################################################################################
class Boss_Right_Missile:

    def __init__(self, x, y):
        self.x , self.y = x, y
        self.frame = 0
        self.image = load_image('Char/Guardian.png')
#--------------------------------------------------------------------------------------------#
    def update(self, frame_time):
        # self.x += self.x / self.y
        self.x += 2
        self.y -= 500 * frame_time
#--------------------------------------------------------------------------------------------#
    def draw(self):
       # self.image.clip_draw( self.frame * 35, 0, 35, 60 , self.x, self.y, 52, 90 )
        self.image.clip_draw( 0, 0, 35, 60 , self.x, self.y, 52, 90 )
#--------------------------------------------------------------------------------------------#
    def draw_bb(self):
        draw_rectangle( *self.get_bb() )
#--------------------------------------------------------------------------------------------#
    def get_bb(self):
        return self.x - 18, self.y - 22, self.x + 18 , self.y + 22


#################################################################################################
class Skill :

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    def __init__(self, x, y) :
        self.x, self.y = x, y
        self.frame = 0
        self.total_frame = 0
        self.image = load_image('Char/skill.png')
#--------------------------------------------------------------------------------------------#
    def update(self, frame_time) :
        self.total_frame += frame_time * Skill.FRAMES_PER_ACTION * Skill.ACTION_PER_TIME
        self.frame = int(self.total_frame) % 5

        if (self.frame == 4) :
            del skill_list[0]
        #     return True
        # else :
        #     return False

#--------------------------------------------------------------------------------------------#
    def draw(self) :
        self.image.clip_draw(self.frame * 115, 130, 115, 115, self.x, self.y, 300, 300)
#--------------------------------------------------------------------------------------------#
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
#--------------------------------------------------------------------------------------------#
    def get_bb(self):
        return self.x-250, self.y-250, self.x+250, self.y+250

#################################################################################################
class Enemy_s:

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    image = None

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 650
        self.frame = 8
        self.hp = 30
        self.speed = 800
        self.total_frame = 0

        if self.image == None:
            self.image = load_image('Char/Scourge.png')
#--------------------------------------------------------------------------------------------#
    def update(self, frame_time):
        self.total_frame += frame_time
        self.total_frame += Enemy_s.FRAMES_PER_ACTION * Enemy_s.ACTION_PER_TIME * frame_time

        self.y -= self.speed * frame_time
        # if(self.y < 0):
        #     del enemy_s_list[0]
#--------------------------------------------------------------------------------------------#
    def draw(self):
        self.image.clip_draw( self.frame * 34, 280, 34, 30 , self.x, self.y )
#--------------------------------------------------------------------------------------------#
    def draw_bb(self):
        draw_rectangle( *self.get_bb() )
#--------------------------------------------------------------------------------------------#
    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20 , self.y + 20

########################################################################

class Enemy_g:
    SHOT_PER_SEC = 1
    image = None
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 600
        self.frame = 8
        self.hp = 40
        self.missile_count = 0
        self.speed = 100
        self.total_frame = 0
        # self.gdeath_sound = load_wav('Sound/Sdeath.wav')
        # self.gdeath_sound.set_volume(30)

        if self.image == None:
            self.image = load_image('Char/Guardian.png')
#--------------------------------------------------------------------------------------------#
    def update(self, frame_time):
        self.y -= self.speed * frame_time
        self.missile_count += frame_time

        if self.missile_count > 1.0 :
            enemy_missile = Enemy_Missile(self.x, self.y)
            enemy_missile_list.append(enemy_missile)
            self.missile_count = 0
#--------------------------------------------------------------------------------------------#
    def draw(self):
        self.image.clip_draw( self.frame * 81, 700, 81, 70 , self.x, self.y )
#--------------------------------------------------------------------------------------------#
    def draw_bb(self):
        draw_rectangle( *self.get_bb() )
#--------------------------------------------------------------------------------------------#
    def get_bb(self):
        return self.x - 40, self.y - 30, self.x + 35 , self.y + 30

################################################################################################
class Enemy_s_death :   # 스커지 죽음 모션

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    def __init__(self, x, y) :
        self.x, self.y = x, y
        self.frame = 0
        self.total_frame = 0
        self.image = load_image('Char/Scourge.png')

#--------------------------------------------------------------------------------------------#
    def update(self, frame_time) :
        self.total_frame += frame_time * Enemy_s_death.FRAMES_PER_ACTION * Enemy_s_death.ACTION_PER_TIME
        self.frame = int(self.total_frame) % 5
        if (self.frame == 4) :
            return True
        else :
            return False
#--------------------------------------------------------------------------------------------#
    def draw(self) :
        self.image.clip_draw( self.frame * 70 ,85, 60, 65 , self.x, self.y)

################################################################################################

class Enemy_g_death :   # 가디언 죽음 모션
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    def __init__(self, x, y) :
        self.x, self.y = x, y
        self.frame = 0
        self.total_frame = 0
        self.image = load_image('Char/Guardian.png')
#--------------------------------------------------------------------------------------------#
    def update(self, frame_time) :
        self.total_frame += frame_time * Enemy_s_death.FRAMES_PER_ACTION * Enemy_s_death.ACTION_PER_TIME
        self.frame = int(self.total_frame) % 5
        if (self.frame == 4) :
            return True
        else :
            return False
#--------------------------------------------------------------------------------------------#
    def draw(self) :
        self.image.clip_draw( self.frame * 115 ,510, 115, 115 , self.x, self.y)

###################################################################################
class Boss:
    global frame_time
    SHOT_PER_SEC = 1

    image = None

    def __init__(self):
        self.x, self.y = 400, 500
        self.frame = 8
        self.hp = 100
        self.missile_count = 0
        self.speed = 150

        if Boss.image == None:
            self.image = load_image('Char/Devourer.png')
#--------------------------------------------------------------------------------------------#
    def update(self, frame_time):
        self.missile_count += frame_time
        if self.missile_count > 2 :

            # 일직선 미사일
            enemy_missile_1 = Enemy_Missile(self.x, self.y+30)

            # 왼쪽 대각선 미사일
            enemy_missile_2 = Boss_Left_Missile(self.x-30, self.y+20)
            enemy_missile_4= Boss_Left_Missile(self.x-80, self.y)

            # 오른쪽 대각선 미사일
            enemy_missile_5 = Boss_Right_Missile(self.x+30, self.y+20)
            enemy_missile_6 = Boss_Right_Missile(self.x+80, self.y)


            enemy_missile_list.append(enemy_missile_1)
            enemy_missile_list.append(enemy_missile_2)
            enemy_missile_list.append(enemy_missile_5)
            enemy_missile_list.append(enemy_missile_4)
            enemy_missile_list.append(enemy_missile_6)

            self.missile_count = 0
#--------------------------------------------------------------------------------------------#
    def draw(self):
        self.image.clip_draw( self.frame * 72, 1850, 72, 85 , self.x, self.y, 180, 212 )
#--------------------------------------------------------------------------------------------#
    def draw_bb(self):
        draw_rectangle( *self.get_bb() )
#--------------------------------------------------------------------------------------------#
    def get_bb(self):
        return self.x - 45, self.y - 90, self.x + 90 , self.y + 90

########################################################################
class Boss_death :  # 디바우러 죽음 모션

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    def __init__(self, x, y) :
        self.x, self.y = x, y
        self.frame = 0
        self.total_frame = 0
        self.image = load_image('Char/Devourer.png')
#--------------------------------------------------------------------------------------------#
    def update(self) :
        self.total_frame += frame_time * Boss_death.FRAMES_PER_ACTION * Boss_death.ACTION_PER_TIME
        self.frame = int(self.total_frame) % 5
        if (self.frame == 4) :
            return True
        else :
            return False
#--------------------------------------------------------------------------------------------#
    def draw(self) :
        self.image.clip_draw( self.frame * 110 ,1150, 110, 100 , self.x, self.y, 300, 300)

#######################################################################
def handle_events( ):

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

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.total_frame = 0
        self.image = load_image('Char/Explosion.png' )

    def update(self, frame_time):
        self.total_frame += frame_time * Enemy_s_death.FRAMES_PER_ACTION * Enemy_s_death.ACTION_PER_TIME
        self.frame = int(self.total_frame) % 16
        if (self.frame == 15) :
            return True
        else :
            return False
    def draw(self):
        self.image.clip_draw(int(self.frame %4)*120, 360-int(self.frame//4)*120, 120, 120, self.x, self.y)

############################################################################################################################################################

def get_frame_time():
    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time

############################################################################################################################################################
def enter():

    global background, timer, player, enemy_s_list, enemy_g_list, enemy_boss_list,\
        enemy_missile_list, Missile_List, enemy_death, explosion, skill_list, boss_left_list, boss_right_list

    background = Background()
    player = Player()
    timer = Timer()

    enemy_s_list = []       # 스커지 리스트
    enemy_g_list = []       # 가디언 리스트
    enemy_boss_list = []    # 디바우러 리스트

    Missile_List = []       # 플레이어 미사일 리스트
    enemy_missile_list = [] # 가디언 미사일 리스트
    boss_left_list = []     # 보스 왼쪽 미사일
    boss_right_list = []    # 보스 오른쪽 미사일
    skill_list = []         # 스킬 리스트

    enemy_death = []        # 적 폭발 리스트
    explosion = []          # 플레이어 폭발 리스트

######################################################################
def exit():
    del(background)
    del(timer)
    del(player)

    del(enemy_s_list)
    del(enemy_g_list)
    del(enemy_boss_list)

    del(Missile_List)
    del(enemy_missile_list)
    del(skill_list)

    del(enemy_death)
    del(explosion)

    close_canvas()


def pause():
    pass


def resume():
    pass

#########################################################################

def update():
    global background, timer, player, enemy_s_list, enemy_g_list, enemy_boss_list,\
        enemy_missile_list, Missile_List, enemy_death, explosion, skill_list, frame_time

    frame_time = get_frame_time()
#--------------------------------------------------------------------------------------------#
    background.update(frame_time)
    timer.update(frame_time)
    player.update(frame_time)
#--------------------------------------------------------------------------------------------#
    # 적 업데이트
    for enemy_s in enemy_s_list:
        enemy_s.update(frame_time)
        if enemy_s.y <= 0:
            enemy_s_list.remove(enemy_s)

    for enemy_g in enemy_g_list:
        enemy_g.update(frame_time)
        if enemy_g.y <= 0:
            enemy_g_list.remove(enemy_g)

    for boss in enemy_boss_list:
        boss.update(frame_time)

    if player.hp <= 0:
        game_framework.push_state(gameover_state)
#--------------------------------------------------------------------------------------------#
    # 미사일 업데이트
    for missile in Missile_List:
        missile.update(frame_time)
        if missile.y >= 600:
            Missile_List.remove(missile)

    for missile in enemy_missile_list:
        missile.update(frame_time)
        if missile.y <= 0:
            enemy_missile_list.remove(missile)

    for missile in boss_left_list:
        missile.update(frame_time)
        if missile.y <= 0:
            boss_left_list.remove(missile)

    for missile in boss_right_list:
        missile.update(frame_time)
        if missile.y <= 0:
            boss_right_list.remove(missile)

    for skill in skill_list:
        skill.update(frame_time)
#--------------------------------------------------------------------------------------------#
    # 폭발 업데이트
    for death in enemy_death:
        death.update(frame_time)
    for player_explosion in explosion:
        player_explosion.update(frame_time)
#--------------------------------------------------------------------------------------------#
    # 플레이어 미사일 + 스커지 충돌체크
    for player_missile in Missile_List:
        for enemy_s in enemy_s_list:
            if collide( player_missile, enemy_s ):  # 충돌체크가 Ture이면
                Missile_List.remove( player_missile )
                enemy_s.hp -= 10

                if enemy_s.hp <= 0:
                    player.sound2()
                    # 스커지 죽는 draw함수 불러옴
                    enemy_s_kill = Enemy_s_death( enemy_s.x, enemy_s.y )
                    enemy_death.append(enemy_s_kill)
                    enemy_s_list.remove( enemy_s )
                    timer.score += 1

#--------------------------------------------------------------------------------------------#
    # 스킬 + 스커지 충돌체크
    for skill in skill_list:
        for enemy_s in enemy_s_list:
            if collide( skill, enemy_s ):  # 충돌체크가 Ture이면
                enemy_s.hp -= 100

                if enemy_s.hp <= 0:
                    player.sound2()
                    # 스커지 죽는 draw함수 불러옴
                    enemy_s_kill = Enemy_s_death( enemy_s.x, enemy_s.y )
                    enemy_death.append(enemy_s_kill)
                    enemy_s_list.remove( enemy_s )
                    timer.score += 1
#--------------------------------------------------------------------------------------------#
    # 플레이어 미사일 + 가디언 충돌체크
    for player_missile in Missile_List:
        for enemy_g in enemy_g_list:
            if collide( player_missile, enemy_g ):

                Missile_List.remove( player_missile )
                enemy_g.hp -= 10
                if enemy_g.hp <= 0:
                    player.sound3()
                    # 가디언 죽는 draw함수 불러옴
                    enemy_g_kill = Enemy_g_death( enemy_g.x, enemy_g.y )
                    enemy_death.append(enemy_g_kill)
                    enemy_g_list.remove( enemy_g )
                    timer.score += 2

#--------------------------------------------------------------------------------------------#
    # 스킬 + 가디언 충돌체크
    for skill in skill_list:
        for enemy_g in enemy_g_list:
            if collide( skill, enemy_g ):  # 충돌체크가 Ture이면
                enemy_g.hp -= 100

                if enemy_g.hp <= 0:
                    player.sound3()
                    enemy_g_kill = Enemy_g_death( enemy_g.x, enemy_g.y )
                    enemy_death.append(enemy_g_kill)
                    enemy_g_list.remove( enemy_g )
                    timer.score += 1

#--------------------------------------------------------------------------------------------#
    # 플레이어 미사일 + 디바우러 충돌체크
    for player_missile in Missile_List:
        for boss in enemy_boss_list:
            if collide( player_missile, boss ):

                Missile_List.remove( player_missile )
                boss.hp -= 10
                if boss.hp <= 0:
                    player.sound4()
                    boss_kill = Enemy_g_death( boss.x, boss.y )
                    enemy_death.append(boss_kill)
                    enemy_boss_list.remove( boss )
                    timer.bcnt = 0
                    timer.score += 5

#--------------------------------------------------------------------------------------------#
    # 스킬 + 디바우러 충돌체크
    for skill in skill_list:
        for boss in enemy_boss_list:
            if collide( skill, boss ):  # 충돌체크가 Ture이면
                boss.hp -= 100
                if boss.hp <= 0:
                    player.sound4()
                    boss_kill = Enemy_g_death( boss.x, boss.y )
                    enemy_death.append(boss_kill)
                    enemy_boss_list.remove( boss )
                    timer.bcnt = 0
                    timer.score += 5

#--------------------------------------------------------------------------------------------#
    # 스커지 몸체 + 플레이어 충돌체크
    for enemy_s in enemy_s_list:
        if collide( enemy_s, player ):
            player.sound5()
            enemy_s_list.remove(enemy_s)
            player_explosion = Explosion(player.x, player.y)
            explosion.append(player_explosion)
            player.hp -= 20
            if player.hp <= 0:
                player.hp = 0

#--------------------------------------------------------------------------------------------#
    # 가디언 미사일 + 플레이어 충돌체크
    for enemy_missile in enemy_missile_list:
        if collide( enemy_missile, player ):
            player.sound5()
            enemy_missile_list.remove( enemy_missile )
            player_explosion = Explosion(player.x, player.y)
            explosion.append(player_explosion)
            player.hp -= 20
            if player.hp <= 0:
                player.hp = 0

#############################################################################
def draw():
    global frame_time

    handle_events()
    clear_canvas()

    background.draw()
    player.draw()
    # player.draw_bb()
    timer.draw()
#--------------------------------------------------------------------------------------------#
    # 적 몸체 그리기
    for enemy_s in enemy_s_list:
        enemy_s.draw()
        # enemy_s.draw_bb()
    for enemy_g in enemy_g_list:
        enemy_g.draw()
        # enemy_g.draw_bb()
    for boss in enemy_boss_list:
        boss.draw()
        # boss.draw_bb()
#--------------------------------------------------------------------------------------------#
    # 미사일 그리기
    for missile in Missile_List:
        missile.draw()
        # missile.draw_bb()
    for missile in enemy_missile_list:
        missile.draw()
        # missile.draw_bb()
    for skill in skill_list:
        skill.draw()
        # skill.draw_bb()
#--------------------------------------------------------------------------------------------#
    # 폭발 그리기
    for death in enemy_death:
        is_die = death.update(frame_time)
        death.draw()
        if is_die == False:
            if death.total_frame >= 5:
                enemy_death.remove(death)

    for player_explosion in explosion:
        is_die = player_explosion.update(frame_time)
        player_explosion.draw()
        if is_die == False:
            if player_explosion.total_frame >= 5:
                explosion.remove(player_explosion)
#--------------------------------------------------------------------------------------------#
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
