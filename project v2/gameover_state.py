__author__ = '김진근'
__author__ = '김진근'
import game_framework
import main_state
import next_stage

from pico2d import *
# 게임오버 추가
name = "stage2"
image = None


def enter():
    global image
    image = load_image('Background/gameover.png')


def exit():
    global image
    del(image)

def handle_events():
    events = get_events()

    for event in events:

        if event.type == SDL_QUIT:
            game_framework.quit()

        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()

            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(next_stage)


def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()




def update():
    pass


def pause():
    pass


def resume():
    pass






