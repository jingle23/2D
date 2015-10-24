__author__ = '김진근'

import random
from pico2d import *

running = None

######################################################################
class Background:

    def __init__(self):
        self.image = load_image('background.png')
        self.y = 0

    def draw(self):
        self.image.clip_draw(0, self.y, 1280, 960-self.y, 640, int((960 - self.y)/2))
        self.image.clip_draw(0, 0, 1280, self.y, 640, 960 - int(960 - (960 - self.y))/2)

    def update(self):
        self.y += 5

        if(self.y >= 960):
            self.y = 0

######################################################################
class Player:

    def __init__(self):
        self.image = load_image('Player.png')
        self.x, self.y = 640, 300
        self.frame = 3

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 80, self.x, self.y)


    # def handle_event(self, event):
    #
    #     if(event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
    #         self.x += 5
    #         self.frame += 1
    #         if self.frame >= 6:
    #             self.frame = 6
    #
    #     if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
    #         self.x -= 5
    #         self.frame -= 1
    #         if self.frame <= 0:
    #             self.frame = 0
    #
    #     if(event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
    #         self.y += 5
    #         self.frame += 1
    #         if self.y >= 960:
    #             self.y = 960
    #
    #     if(event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
    #         self.y -= 5
    #         self.frame -= 1
    #         if self.y <= 0:
    #             self.y = 0


#######################################################################

class Enemy_s:

    image = None

    def __init__(self):
        self.x, self.y = random.randint(50, 1200), 900
        self.frame = 8

        if Enemy_s.image == None:
            self.image = load_image('Scourge.png')

    def update(self):
        self.y -= 30

    def draw(self):
        self.image.clip_draw( self.frame * 34, 280, 35, 30 , self.x, self.y )



########################################################################
#
# class Missile:
#
#     def __init__(self):
#






########################################################################

def handle_events():

    global running, player
    events = get_events()

    for event in events:

        if event.type == SDL_QUIT:
            running = False

        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

        # Player.handle_event(event)

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            player.x += 50
            if player.x >= 1200:
                player.x = 1200

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
            if player.y >= 900:
                player.y = 900

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            player.y -= 30
            if player.y <= 0:
                player.y = 0

#############################################################################

background = None
player = None
running = True

################################################
def main():

    open_canvas(1280, 960)


    global background, player, running, enemy_s

    background = Background()
    player = Player()
    enemy_s = Enemy_s()

    running = True;

    while running :
        handle_events()

        background.update()
        enemy_s.update()
        # for enemy_s in Enemy_s_List:
        # enemy_s.update()


        clear_canvas()

        background.draw()
        player.draw()
        enemy_s.draw()
        # for enemy_s in Enemy_s_List:
        #     enemy_s.draw()


        update_canvas()

        delay(0.06)

    close_canvas()



#####################################################################


if __name__ == '__main__':
    main()
######################################################################

################################################
# def enter():
#     global background, player
#
#     open_canvas()
#
#     background = Background()
#     player = load_image('Player.gif')
#
# ################################################
# def exit():
#     global background, player
#
#     del(background)
#     del(player)
#
#     close_canvas()
#
# ################################################
# def update():
#     background.update()
#
# ################################################
# def draw():
#     clear_canvas()
#
#     background.draw()
#     player.draw(600, 300)
#
#     update_canvas()
#
# ################################################
#
# def main():
#
#     enter()
#
#     while running:
#         # handle_events()
#         update()
#         draw()
#
#     exit()
