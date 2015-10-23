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
        self.image.clip_draw( 0, self.y, 1280, 960-self.y, 640, int((960 - self.y)/2) )
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


    def handle_event(self, event):

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.x += 5
            self.frame += 1
            if self.frame >= 6:
                self.frame = 6

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.x -= 5
            self.frame -= 1
            if self.frame <= 0:
                self.frame = 0

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.y += 5
            self.frame += 1
            if self.y >= 600:
                self.y = 600

        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            self.y -= 5
            self.frame -= 1
            if self.y <= 0:
                self.y = 0










########################################################################

def handle_events():

    global running
    events = get_events()

    for event in events:

        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

        else:
            Player.handle_event(event)



background = None
player = None
running = True

################################################
def main():

    open_canvas(1280, 960)

    global background, player, running

    background = Background()
    player = Player()

    running = True;

    while running :
        handle_events()

        background.update()

        clear_canvas()

        background.draw()
        player.draw()


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
