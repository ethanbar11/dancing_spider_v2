import motions
import time
import instructables_ik as IK

from common_constants import *


# Min time in seconds.
# Real ratio of movements meaning how much time is allocated for the movement,
# And how much is allocated for being in the position for the beat.


# Here for the default params
class Movement:
    def __init__(self, spider):
        self.min_time = 0.2
        # self.min_reps = 8
        self.min_reps = 1
        self.max_reps = 3
        # self.max_reps = 20
        self.spider = spider
        self.real_ratio_of_movement = 3 / 5

    # Should be override in son
    def perform_move(self, t, freq):
        pass

    def perform_move_wrapped(self, t, freq):
        self.spider.time_master.start_movement()
        self.perform_move(t, freq)
        self.spider.time_master.end_movement()


class LiftLeg(Movement):
    def perform_move(self, t, freq):
        self.spider.legs[2].perform_func_with_axis(t * self.real_ratio_of_movement,
                                                   freq,
                                                   motions.leg_up_and_down)

class LiftArm(Movement):
    def perform_move(self, t, freq):
        self.move_to_side(t * self.real_ratio_of_movement / 2, freq, up=True)
        self.spider.time_master.part_of_movement(1 / 2)
        self.move_to_side(t * self.real_ratio_of_movement / 2, freq, up=False)


    def move_to_side(self, total_time, freq, up):
        target_angle = 170 if up else 30
        x = total_time * freq
        n = int(x)
        wait_buf = x - n
        current_time = time.time()
        time_to_wait = total_time / n

        cur_angle = self.spider.legs[2].tibia_joint.angle
        angles_to_rotate = target_angle - cur_angle

        for i in range(n):
            cur_angle = self.spider.legs[2].tibia_joint.angle
            ang=cur_angle + angles_to_rotate / n
            self.spider.legs[2].tibia_joint.set_angle(cur_angle + angles_to_rotate / n)
            self.spider.legs[2].x, self.spider.legs[2].y, self.spider.legs[2].z = IK.angle_to_axis(self.spider.legs[2].num, self.spider.legs[2].coxa_joint.angle,
                                                    self.spider.legs[2].femur_joint.angle,
                                                    self.spider.legs[2].tibia_joint.angle)
            while time.time() - current_time < time_to_wait:
                pass
            current_time = time.time()


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

    def perform_move(self, t, freq):
        self.hump_half_move(t * self.real_ratio_of_movement / 2, freq, backwords=False)
        self.spider.time_master.part_of_movement(1 / 2)
        self.hump_half_move(t * self.real_ratio_of_movement / 2, freq, backwords=True)


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

    def perform_move(self, t, freq):
        self.ass_half_move(t * self.real_ratio_of_movement / 2, freq, up=True)
        self.spider.time_master.part_of_movement(1 / 2)
        self.ass_half_move(t * self.real_ratio_of_movement / 2, freq, up=False)

class PushUp(Movement):
    def body_half_move(self, total_time, freq, down):
        movement_amount = -TWERK_AMOUNT if down else TWERK_AMOUNT
        end_poses = [
            (self.spider.legs[0].pos[0], self.spider.legs[0].pos[1], self.spider.legs[0].pos[2] + movement_amount),
            (self.spider.legs[1].pos[0], self.spider.legs[1].pos[1], self.spider.legs[1].pos[2] + movement_amount),
            (self.spider.legs[2].pos[0], self.spider.legs[2].pos[1], self.spider.legs[2].pos[2] + movement_amount),
            (self.spider.legs[3].pos[0], self.spider.legs[3].pos[1], self.spider.legs[3].pos[2] + movement_amount)]
        self.spider.perform_func_with_axis(total_time,
                                           freq,
                                           motions.move_leg_straight_line,
                                           end_poses)

    def perform_move(self, t, freq):
        self.body_half_move(t * self.real_ratio_of_movement / 2, freq, down=True)
        self.spider.time_master.part_of_movement(1 / 2)
        self.body_half_move(t * self.real_ratio_of_movement / 2, freq, down=False)

class HeapMove(Movement):
    def __init__(self, spider):
        super().__init__(spider)
        self.min_time = 0.2 # for now...
    def perform_move(self, t, freq):
        self.move_to_side(t * self.real_ratio_of_movement / 2, freq, lefty=True)
        self.spider.time_master.part_of_movement(1 / 2)
        self.move_to_side(t * self.real_ratio_of_movement / 2, freq, lefty=False)

    def move_to_side(self, total_time, freq, lefty):
        DEGREES_TO_MOVE = 45
        x = total_time * freq
        n = int(x)
        wait_buf = x - n
        angles_to_rotate = []
        current_time = time.time()
        time_to_wait = total_time / n
        cur_angles = []

        for i, leg in enumerate(self.spider.legs):
            cur_angle = leg.coxa_joint.angle
            cur_angles.append(cur_angle)
            if lefty:
                tar_angle = 135 + DEGREES_TO_MOVE if i % 2 == 0 else 45 + DEGREES_TO_MOVE
            else:
                tar_angle = 135 - DEGREES_TO_MOVE if i % 2 == 0 else 45 - DEGREES_TO_MOVE
            angles_to_rotate.append(tar_angle - cur_angle)

        for i in range(n):
            for j, leg in enumerate(self.spider.legs):
                current_angle = leg.coxa_joint.angle
                leg.coxa_joint.set_angle(current_angle + angles_to_rotate[j] / x)
                leg.x, leg.y, leg.z = IK.angle_to_axis(leg.num, leg.coxa_joint.angle,
                                                       leg.femur_joint.angle,
                                                       leg.tibia_joint.angle)
            while time.time() - current_time < time_to_wait:
                pass
            current_time = time.time()
