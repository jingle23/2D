__author__ = '김진근'

name = "StartState"
import game_framework
from pico2d import *

import title_state
import main_state


name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    open_canvas()
    image = load_image('Background/intro.png')


def exit():
    global image
    del(image)
    close_canvas()


def update(frame_time):
    global logo_time

    if( logo_time > 2.0 ):
        logo_time = 0
        game_framework.push_state(title_state)

    logo_time += frame_time

    pass


def draw():
    global image
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

    pass


def handle_events():
    events = get_events()
    pass


######################################################################
def pause():
    pass
def resume():
    pass
#########################################################################