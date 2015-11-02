__author__ = '김진근'

# 1. 해야할것 몬스터들이 여러마리 생성되도록
# 2.
# 3. 인트로, 메인화면 넘어가기
# 4. 몬스터가 겹치지 않도록
# 5.

import random


from pico2d import *

running = None

######################################################################
class Background:

    def __init__(self):
        self.image = load_image('background.png')
        self.y = 0

    def draw(self):

        self.image.clip_draw(0, self.y, 800, 600-self.y, 400, int((600 - self.y)/2))
        self.image.clip_draw(0, 0, 800, self.y, 400, 600 - int(600 - (600 - self.y))/2)


    def update(self):
        self.y += 5

        if(self.y >= 600):
            self.y = 0

######################################################################
class Player:

    image = None

    STOP, START = 0, 1

    def __init__(self):
        self.image = load_image('Player.png')
        self.x, self.y = 400, 100
        self.frame = 3
        self.RIGHT, self.LEFT, self.UP, self.DOWN = self.STOP


    def handle_event(self, event):

        ## 미사일발사
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            pass

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.RIGHT = self.START

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.LEFT = self.START

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.UP = self.START


        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            self.DOWN = self.START


    def update(self):
        self.frame = (self.frame + 1) % 6

        if self.RIGHT == self.START:
            self.x = min( 800, self.x + 50 )

            # player.x += 50
            # # player.frame += 1
            #
            # if player.x >= 800:
            #     player.x = 800
            #
            # # if player.frame >= 6:
            # #     player.frame = 6


        if self.LEFT == self.START:
            self.x = max(0, self.x - 50)

            # player.x -= 50
            # # player.frame -= 1
            #
            # if player.x <= 20:
            #     player.x = 20

            # if player.frame <= 0:
            #     player.frame = 0

        if self.UP == self.START:
            self.y = min(550, self.y + 30)

            # player.y += 30
            # if player.y >= 550:
            #     player.y = 550

        if self.DOWN == self.START:
            self.y = max(0, self.y - 30)

            # player.y -= 30
            # if player.y <= 50:
            #     player.y = 50


    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 80, self.x, self.y)




#######################################################################






class Enemy_s:

    image = None

    def __init__(self):
        # self.x, self.y = random.randint(50, 1200), 900
        self.x, self.y = random.randint(50, 750), 600
        self.frame = 8

        if self.image == None:
            self.image = load_image('Scourge.png')

    def update(self):
        self.y -= 50

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
        self.y -= 3
        self.randint = random.randint(1,6)
        if (self.randint % 2 == 0):
            self.x += 10
            if ( self.x >= 750 ):
                self.x = 750

        else:
            self.x -= 10
            if ( self.x <= 50 ):
                self.x = 50

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

        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

        else:
            player.handle_event(event)



#############################################################################

player = None
background = None
enemy_s = None
enemy_g = None
boss = None

running = True

###############################################
def main():

    open_canvas(800, 600)

    global background, player, running, enemy_s,enemy_g, boss

    background = Background()
    player = Player()
    enemy_s = Enemy_s()
    enemy_g = Enemy_g()
    boss = Boss()

    running = True;

    while running :
        handle_events()

        player.update()
        background.update()
        enemy_s.update()
        enemy_g.update()
        boss.update()

        clear_canvas()

        background.draw()
        player.draw()
        enemy_s.draw()
        enemy_g.draw()
        boss.draw()

        update_canvas()

        delay(0.05)

    close_canvas()




######################################################################

# player = None
# background = None
# enemy_s = None
# enemy_g = None
# boss = None
#
# running = True
#
#
# def enter():
#
#     global background, player, enemy_s, enemy_g, boss
#
#     background = Background()
#     player = Player()
#     enemy_s = Enemy_s()
#     enemy_g = Enemy_g()
#     boss = Boss()
#
# ######################################################################
# def exit():
#     global background, player, enemy_s, enemy_g, boss
#     del(background)
#     del(player)
#     del(boss)
#     del(enemy_s)
#     del(enemy_g)
#
#     close_canvas()
#
# ######################################################################
#
# def update():
#
#         background.update()
#         enemy_s.update()
#         enemy_g.update()
#         boss.update()
#
#
# #############################################################################
#
# def draw():
#
#         handle_events()
#         clear_canvas()
#
#         background.draw()
#         player.draw()
#         enemy_s.draw()
#         enemy_g.draw()
#         boss.draw()
#
#         update_canvas()
# #
# # #############################################################################
# #
# def main():
#
#     enter()
#     while running:
#
#         handle_events()
#         update()
#         draw()
#     exit()

####################################################################

if __name__ == '__main__':
    main()




