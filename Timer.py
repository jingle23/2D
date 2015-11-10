__author__ = '김진근'
#########################################################################

class Timer :
    def __init__(self):
        self.time = 0.0
        self.timer = 0.0
        self.min = 0.0
        self.sec = 0.0

    def update(self, frame_time):
        self.timer += frame_time
        self.time += frame_time

        self.min = (int)( self.timer / 60 )
        self.sec = (int)( self.timer % 60 )

        self.create_enemy_s()
        self.create_enemy_g()


    def create_enemy_s(self):
        if self.time >= 1.5 :
            new_enemy_s = Enemy_s()
            enemy_s_list.append( new_enemy_s )

            self.time = 0.0

    def create_enemy_g(self):
        if self.time >= 3:
            new_enemy_g = Enemy_g()
            enemy_g_list.append( new_enemy_g )

            self.time = 0.0



#########################################################################
