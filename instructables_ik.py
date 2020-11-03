from math import ceil, atan2, acos, sqrt, pi, floor, pow, radians as rad
from common_constants import *
import math


def change_to_d(angle):
    if angle == pi:
        angle = 0
    x = angle * 180 / pi
    if x - floor(x) > 0.5:
        return ceil(x)
    return floor(x)


def axis_to_angle(leg, x, y, z):
    w = (sqrt(pow(x, 2) + pow(y, 2)))
    # w = w if x >= 0 else (-1) * w
    v = w - COXA_LEN
    # alpha = atan2(y, x) if w >= 0 else atan2(-y, -x)
    alpha = atan2(y, x)
    beta = atan2(z, v) + acos(
        (pow(FEMUR_LEN, 2) - pow(TIBIA_LEN, 2) + pow(v, 2) + pow(z, 2)) / 2 / FEMUR_LEN / sqrt(pow(v, 2) + pow(z, 2)))
    gamma = acos((pow(FEMUR_LEN, 2) + pow(TIBIA_LEN, 2) - pow(v, 2) - pow(z, 2)) / 2 / TIBIA_LEN / FEMUR_LEN)
    # Fixing for different coordinate system.
    beta = -beta if leg == 1 or leg == 3 else beta
    gamma = gamma if leg == 1 or leg == 3 else pi - gamma
    return change_to_d(alpha), change_to_d(beta), change_to_d(gamma)


def cos(x):
    return math.cos(rad(x))


def sin(x):
    return math.sin(rad(x))


def angle_to_axis(leg, a, b, g):
    t1, t2, t3 = get_fixed_angles(leg, a, b, g)
    a1 = COXA_LEN
    a2 = FEMUR_LEN
    a3 = TIBIA_LEN
    # here comes the fixes
    if leg == 2 or leg == 4:
        x = a1 * cos(t1) + a2 * cos(t1) * cos(t2) - a3 * sin(t2) * sin(t3) * cos(t1) + a3 * cos(t1) * cos(t2) * cos(t3)
        y = a1 * sin(t1) + a2 * sin(t1) * cos(t2) - a3 * sin(t1) * sin(t2) * sin(t3) + a3 * sin(t1) * cos(t2) * cos(t3)
        z = a2 * sin(t2) + a3 * sin(t2) * cos(t3) + a3 * sin(t3) * cos(t2)
    else:
        x = a1 * cos(t1) + a2 * cos(t1) * cos(t2) - a3 * sin(t2) * sin(t3) * cos(t1) + a3 * cos(t1) * cos(t2) * cos(t3)
        y = a1 * sin(t1) + a2 * sin(t1) * cos(t2) - a3 * sin(t1) * sin(t2) * sin(t3) + a3 * sin(t1) * cos(t2) * cos(t3)
        z = -a2 * sin(t2) - a3 * sin(t2) * cos(t3) - a3 * sin(t3) * cos(t2)
    return x, y, z


def get_fixed_angles(leg, a, b, g):
    if leg == 2 or leg == 4:
        g = -(180 - g)
    return a - 90, b - 90, 180 - g

    # if leg == 1 or leg == 3:
    #     return a - 90, b - 90, g
    # if leg == 1:
    #     return a - 90, 90 - b, 180 - g
    # elif leg == 2:
    #     return 90 - a, b - 90, 180 - g
    # elif leg == 4:
    #     return 90 - a, b - 90, 180 - g
    # elif leg == 3:
    #     return a - 90, 90 - b, g


def add_hard_coded_angle_fix(a, b, g):
    return a + 90, b + 90, g


# if __name__ == '__main__':
#     # print(angle_to_axis(1, 0, 0, 90))
#     from sympy import var, Matrix, init_printing, pprint, cos, sin
#
#     a1, a2, a3, t1, t2, t3 = var('a1 a2 a3 t1 t2 t3')
#     # a1 = COXA_LEN
#     # a2 = FEMUR_LEN
#     # a3 = TIBIA_LEN
#     # t1 = -18
#     # t2 = 30
#     # t3 = -121
#     H11 = Matrix([[cos(t1), 0, sin(t1), a1 * cos(t1)],
#                   [sin(t1), 0, -cos(t1), a1 * sin(t1)],
#                   [0, 1, 0, 0],
#                   [0, 0, 0, 1]]
#                  )
#     H21 = Matrix([[cos(t2), -sin(t2), 0, a2 * cos(t2)],
#                   [sin(t2), cos(t2), 0, a2 * sin(t2)],
#                   [0, 0, 1, 0],
#                   [0, 0, 0, 1]])
#     H31 = Matrix([[cos(t3), -sin(t3), 0, a3 * cos(t3)],
#                   [sin(t3), cos(t3), 0, a3 * sin(t3)],
#                   [0, 0, 1, 0],
#                   [0, 0, 0, 1]])
#     H12 = Matrix([[cos(t1), 0, -sin(t1), a1 * cos(t1)],
#                   [sin(t1), 0, cos(t1), a1 * sin(t1)],
#                   [0, -1, 0, 0],
#                   [0, 0, 0, 1]]
#                  )
#     H22 = Matrix([[cos(t2), -sin(t2), 0, a2 * cos(t2)],
#                   [sin(t2), cos(t2), 0, a2 * sin(t2)],
#                   [0, 0, 1, 0],
#                   [0, 0, 0, 1]])
#     H32 = Matrix([[cos(t3), -sin(t3), 0, a3 * cos(t3)],
#                   [sin(t3), cos(t3), 0, a3 * sin(t3)],
#                   [0, 0, 1, 0],
#                   [0, 0, 0, 1]])
#
#     # With fixes, might be for 1,3 legs?
#     # H1 = Matrix([[cos(t1), 0, -sin(t1), a1 * cos(t1)],
#     #              [sin(t1), 0, cos(t1), a1 * sin(t1)],
#     #              [0, -1, 0, 0],
#     #              [0, 0, 0, 1]]
#     #             )
#     # H2 = Matrix([[cos(t2), -sin(t2), 0, a2 * cos(t2)],
#     #              [sin(t2), cos(t2), 0, a2 * sin(t2)],
#     #              [0, 0, 1, 0],
#     #              [0, 0, 0, 1]])
#     # H3 = Matrix([[cos(t3), -sin(t3), 0, a3 * cos(t3)],
#     #              [sin(t3), cos(t3), 0, a3 * sin(t3)],
#     #              [0, 0, 1, 0],
#     #              [0, 0, 0, 1]])
#
#     init_printing()
#     F24 = H11 * H21 * H31
#     F13 = H12 * H22 * H32
#     # # pprint(H1)
#     # # pprint(H2)
#     # # pprint(H3)
#     print(F24.col(-1))
#     print(F13.col(-1))
#     # pprint(F24.col(-1))
#     # pprint(F13.col(-1))

if __name__ == '__main__':
    print(x_default - x_offset, 0, z_default)
    ang = axis_to_angle(3, x_default - x_offset, 0, z_default)
    ang=add_hard_coded_angle_fix(ang[0],ang[1],ang[2])
    print(angle_to_axis(3, ang[0]+66, ang[1], ang[2]))
