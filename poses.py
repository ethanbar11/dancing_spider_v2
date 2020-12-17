import random
from movements import *


# Returns True for Other pose and False for movement
def next_action_movement_or_pose():
    return random.random() > MOVEMENT_THRESHOLD


class StandBase:
    def __init__(self, spider):
        self.spider = spider
        self.connected_poses = None

    # Should be overriden by son
    def perform_pose(self, t):
        pass

    def perform_pose_wrapped(self, t):
        self.spider.time_master.start_movement()
        self.perform_pose(t)
        self.spider.time_master.end_movement()


class Stand(StandBase):
    def __init__(self, spider):
        super().__init__(spider)
        self.movements = [StepRotate(self.spider)]
        # self.movements = [StepForward(self.spider,True),StepForward(self.spider,False)]
        # self.movements = [LiftLeg(self.spider)]#, StepForward(self.spider, True)]

    def perform_pose(self, t):
        self.spider.legs[0].set_angles_from_r(x_default - x_offset, y_start + y_step, z_default)
        self.spider.legs[1].set_angles_from_r(x_default - x_offset, -(y_start + y_step), z_default)
        self.spider.legs[2].set_angles_from_r(x_default + x_offset, y_start, z_default)
        self.spider.legs[3].set_angles_from_r(x_default + x_offset, y_start, z_default)
        for i in self.spider.legs:
            print(i.coxa_joint.angle)


class OmerAdamStand(StandBase):
    def __init__(self, spider):
        super().__init__(spider)
        self.movements = [LiftArm(self.spider)]

    def perform_pose(self, t):
        self.spider.legs[0].set_angles_from_r(x_default - x_offset, y_start + y_step, z_default)
        self.spider.legs[1].set_angles_from_r(x_default - x_offset, -(y_start + y_step), z_default)
        self.spider.legs[2].set_angles_from_r(x_default + x_offset, y_start + 5, z_default + 30)
        self.spider.legs[3].set_angles_from_r(x_default + x_offset - 20, y_start + 20, z_default)


class DanceStand(StandBase):
    def __init__(self, spider):
        super().__init__(spider)
        self.movements = [Twerk(self.spider), HeapMove(self.spider), PushUp(self.spider)]
        # self.movements = [HeapMove(self.spider)]
        # self.movements = [PushUp(self.spider)]

    def perform_pose(self, t):
        self.spider.legs[0].set_angles_from_r(x_default, y_default, z_default)
        self.spider.legs[1].set_angles_from_r(x_default, -y_default, z_default)
        self.spider.legs[2].set_angles_from_r(x_default, y_default, z_default)
        self.spider.legs[3].set_angles_from_r(x_default, -y_default, z_default)


class HumpStand(StandBase):
    def __init__(self, spider):
        super().__init__(spider)
        self.movements = [Hump(self.spider)]

    def perform_pose(self, t):
        self.spider.legs[0].set_angles_from_r(x_default, y_default, z_hump_stand + 30)
        self.spider.legs[1].set_angles_from_r(x_default, -y_default, z_hump_stand - 30)
        self.spider.legs[2].set_angles_from_r(x_default, y_default, z_hump_stand - 30)
        self.spider.legs[3].set_angles_from_r(x_default, -y_default, z_hump_stand + 30)


stand = Stand(None)
dance_stand = DanceStand(None)
hump_stand = HumpStand(None)
omer_adam_stand = OmerAdamStand(None)
