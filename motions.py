from common_constants import *
import math


# x is phi
def silly_tan_walk(start_pos, phi, end_pos):
    if phi <= 1 / 2:
        diff = end_pos[1] - start_pos[1]
        progress_y = diff * phi * 2

        return start_pos[0], start_pos[1] + progress_y, \
               start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)
    else:
        diff = end_pos[0] - start_pos[0]
        progress_x = diff * (phi - 1 / 2) * 2

        return start_pos[0] + progress_x, end_pos[1], \
               start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)


def silly_tan_walk_reversed(start_pos, phi, end_pos):
    if phi <= 1 / 2:
        diff = end_pos[0] - start_pos[0]
        progress_x = diff * phi * 2

        return start_pos[0] + progress_x, start_pos[1], \
               start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)
    else:
        diff = end_pos[1] - start_pos[1]
        progress_y = diff * (phi - 1 / 2) * 2

        return end_pos[0], start_pos[1] + progress_y, \
               start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)


# Dance Moves
# From stand
def leg_up_and_down(start_pos, phi, end_pos=None):
    if phi <= 1 / 2:
        new_z = start_pos[2] + 2 * phi * (LIFT_LEG_FINAL_Z - start_pos[2])
    else:
        new_z = LIFT_LEG_FINAL_Z + 2 * (phi - 1 / 2) * (start_pos[2] - LIFT_LEG_FINAL_Z)
    return start_pos[0], start_pos[1], new_z


def move_leg_straight_line(start_pose, phi, end_pose):
    x = start_pose[0] + phi * (end_pose[0] - start_pose[0])
    y = start_pose[1] + phi * (end_pose[1] - start_pose[1])
    z = start_pose[2] + phi * (end_pose[2] - start_pose[2])
    return x, y, z
