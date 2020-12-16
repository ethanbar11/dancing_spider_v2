import random
from movements import *


# Returns True for Other pose and False for movement
def next_action_movement_or_pose():
    return random.random() > MOVEMENT_THRESHOLD


class Stand:
    def __init__(self, spider):
        self.spider = spider
        self.movements = [LiftLeg(self.spider)]
        self.connected_poses = None

    def perform_pose(self, start_time, t):
        self.spider.legs[0].set_angles_from_r(x_default - x_offset, y_start + y_step, z_default)
        self.spider.legs[1].set_angles_from_r(x_default - x_offset, -(y_start + y_step), z_default)
        self.spider.legs[2].set_angles_from_r(x_default + x_offset, y_start, z_default)
        self.spider.legs[3].set_angles_from_r(x_default + x_offset, y_start, z_default)
        wait(start_time, t)


class DanceStand:
    def __init__(self, spider):
        self.spider = spider
        self.movements = [Twerk(self.spider)]
        self.connected_poses = None

    def perform_pose(self, start_time, t):
        self.spider.legs[0].set_angles_from_r(x_default, y_default, z_default)
        self.spider.legs[1].set_angles_from_r(x_default, -y_default, z_default)
        self.spider.legs[2].set_angles_from_r(x_default, y_default, z_default)
        self.spider.legs[3].set_angles_from_r(x_default, -y_default, z_default)
        wait(start_time, t)


class HumpStand:
    def __init__(self, spider):
        self.spider = spider
        self.movements = [Hump(self.spider)]
        self.connected_poses = None

    def perform_pose(self, start_time, t):
        self.spider.legs[0].set_angles_from_r(x_default, y_default, z_hump_stand + 30)
        self.spider.legs[1].set_angles_from_r(x_default, -y_default, z_hump_stand - 30)
        self.spider.legs[2].set_angles_from_r(x_default, y_default, z_hump_stand - 30)
        self.spider.legs[3].set_angles_from_r(x_default, -y_default, z_hump_stand + 30)
        wait(start_time, t)


stand = Stand(None)
dance_stand = DanceStand(None)
hump_stand = HumpStand(None)
