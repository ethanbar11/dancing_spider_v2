from common_constants import *
import math


# Only works for numbers 0<=x<=1
def sin_walk(start_pos, phi, end_pose=None):
    return start_pos[0], \
           start_pos[1] + phi * STEP_LENGTH, \
           start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)


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

        return start_pos[0]+progress_x, start_pos[1] , \
               start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)
    else:
        diff = end_pos[1] - start_pos[1]
        progress_y = diff * (phi - 1 / 2) * 2

        return end_pos[0], start_pos[1] + progress_y, \
               start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)


# Phi is i/n division, the current part of the curve.
def sin_walk_reverse(start_pos, phi, end_pose=None):
    return start_pos[0], \
           start_pos[1] - phi * STEP_LENGTH_LEG_2, \
           start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)


def backward_sin_walk(start_pos, phi, end_pos=None):
    if phi >= 2 / 3:
        return start_pos[0] + SIN_MAX_WIDTH * math.sin(1 / 2 * math.pi), \
               start_pos[1] - phi * STEP_LENGTH, \
               start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)

    return start_pos[0] + SIN_MAX_WIDTH * math.sin(phi * math.pi), \
           start_pos[1] - phi * STEP_LENGTH, \
           start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)


def backward_sin_walk_reverse(start_pos, phi, end_pos=None):
    if phi >= 2 / 3:
        return start_pos[0] + SIN_MAX_WIDTH * math.sin(1 / 2 * math.pi), \
               start_pos[1] + phi * STEP_LENGTH_LEG_2, \
               start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)

    return start_pos[0] + SIN_MAX_WIDTH * math.sin(phi * math.pi), \
           start_pos[1] + phi * STEP_LENGTH_LEG_2, \
           start_pos[2] + SIN_MAX_HEIGHT * math.sin(phi * math.pi)
