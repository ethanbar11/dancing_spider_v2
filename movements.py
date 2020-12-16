import motions
import time

from common_constants import *


# Min time in seconds.
# Real ratio of movements meaning how much time is allocated for the movement,
# And how much is allocated for being in the position for the beat.

def wait(start_time, total_action_time):
    while time.time() - start_time < total_action_time:
        pass


# Here for the default params
class Movement:
    def __init__(self, spider):
        self.min_time = 0.2
        self.min_reps = 8
        self.max_reps = 20
        self.spider = spider
        self.real_ratio_of_movement = 3 / 5


class LiftLeg(Movement):
    def perform_move(self, start_time, t, freq):
        self.spider.legs[2].perform_func_with_axis(t * self.real_ratio_of_movement,
                                                   freq,
                                                   motions.leg_up_and_down)
        wait(start_time, t)


# Expecting to be in Hump stand with head up
class Hump(Movement):
    def hump_half_move(self, total_time, freq, backwords=False):
        diff_y = HUMP_AMOUNT if not backwords else -HUMP_AMOUNT
        end_poses = [(self.spider.legs[0].pos[0], self.spider.legs[0].pos[1] + diff_y, self.spider.legs[0].pos[2]),
                     (self.spider.legs[1].pos[0], self.spider.legs[1].pos[1] + diff_y, self.spider.legs[1].pos[2]),
                     (self.spider.legs[2].pos[0], self.spider.legs[2].pos[1] - diff_y, self.spider.legs[2].pos[2]),
                     (self.spider.legs[3].pos[0], self.spider.legs[3].pos[1] - diff_y, self.spider.legs[3].pos[2])]
        self.spider.perform_func_with_axis(total_time,
                                           freq,
                                           motions.move_leg_straight_line,
                                           end_poses)

    def perform_move(self, start_time1,  t, freq):
        self.hump_half_move(t * self.real_ratio_of_movement / 2, freq, backwords=False)
        wait(start_time1, t / 2)
        start_time2 = time.time()
        self.hump_half_move(t * self.real_ratio_of_movement / 2, freq, backwords=True)
        wait(start_time2, t / 2)


class Twerk(Movement):
    def ass_half_move(self, total_time, freq, up):
        movement_amount = -TWERK_AMOUNT if up else TWERK_AMOUNT
        end_poses = [
            (self.spider.legs[0].pos[0], self.spider.legs[0].pos[1], self.spider.legs[0].pos[2] + movement_amount),
            self.spider.legs[1].pos,
            self.spider.legs[2].pos,
            (self.spider.legs[3].pos[0], self.spider.legs[3].pos[1], self.spider.legs[3].pos[2] + movement_amount)]
        self.spider.perform_func_with_axis(total_time,
                                           freq,
                                           motions.move_leg_straight_line,
                                           end_poses)

    def perform_move(self, start_time1, t, freq):
        self.ass_half_move(t * self.real_ratio_of_movement / 2, freq, up=True)
        wait(start_time1, t / 2)
        start_time2 = time.time()
        self.ass_half_move(t * self.real_ratio_of_movement / 2, freq, up=False)
        wait(start_time2, t / 2)
        print(t, time.time() - start_time1)
