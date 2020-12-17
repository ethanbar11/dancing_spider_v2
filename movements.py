import motions
import time

from common_constants import *


# Min time in seconds.
# Real ratio of movements meaning how much time is allocated for the movement,
# And how much is allocated for being in the position for the beat.


# Here for the default params
class Movement:
    def __init__(self, spider):
        # Minimal time of movement in seconds, can be overridden.
        self.min_time = 0.2
        self.min_reps = 1
        self.max_reps = 3
        self.spider = spider
        self.real_ratio_of_movement = 3 / 5

    # Should be override in son
    def perform_move(self, freq):
        pass

    def perform_move_wrapped(self, t, freq):
        self.t = self.spider.time_master.start_movement(self)
        self.perform_move(freq)
        self.spider.time_master.end_movement()


class LiftLeg(Movement):
    def perform_move(self, freq):
        self.spider.legs[2].perform_func_with_axis(self.t * self.real_ratio_of_movement,
                                                   freq,
                                                   motions.leg_up_and_down)


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

    def perform_move(self, freq):
        self.hump_half_move(self.t * self.real_ratio_of_movement / 2, freq, backwords=False)
        self.spider.time_master.part_of_movement(1 / 2)
        self.hump_half_move(self.t * self.real_ratio_of_movement / 2, freq, backwords=True)


class Twerk(Movement):
    def __init__(self, spider):
        super().__init__(spider)
        self.min_time = 2

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

    def perform_move(self, freq):
        self.ass_half_move(self.t * self.real_ratio_of_movement / 2, freq, up=True)
        self.spider.time_master.part_of_movement(1 / 2)
        self.ass_half_move(self.t * self.real_ratio_of_movement / 2, freq, up=False)


class StepForward(Movement):
    def __init__(self, spider, is_forward_step):
        super().__init__(spider)
        self.min_time = 1.2

    def init_params_for_half_step(self, first):
        front_leg = 2 if first else 1
        back_leg = 0 if first else 3
        one_leg_step_time = self.t * ONE_LEG_STEP_PROPORTION
        heap_move_wait_time = self.t * ONE_HEAP_MOVE_PROPORTION
        return back_leg, front_leg, heap_move_wait_time, one_leg_step_time

    def half_step(self, freq, first=False):
        back_leg, front_leg, heap_move_wait_time, one_leg_step_time = self.init_params_for_half_step(first)

        self.spider.legs[front_leg].step_forward(one_leg_step_time, freq)
        for leg in self.spider.legs[::-1]:
            leg.move_heap_forward()
        time.sleep(heap_move_wait_time)
        self.spider.legs[back_leg].step_forward(one_leg_step_time, freq)

    def perform_move(self, freq):
        self.half_step(freq, first=True)
        self.spider.time_master.part_of_movement(1 / 2)
        self.half_step(freq, first=False)
