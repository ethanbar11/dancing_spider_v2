from math import *
from common_constants import *


# COXA_LEN = 27.5
# FEMUR_LEN = 70
# TIBIA_LEN = 80
# TOTAL = COXA_LEN + FEMUR_LEN + TIBIA_LEN
# Z_OFFSET = 50


def change_to_d(angle):
    if angle == pi:
        angle = 0
    x = angle * 180 / pi
    if x - floor(x) > 0.5:
        return ceil(x)
    return floor(x)


def axis_to_angle(x, y, z):
    w = (sqrt(pow(x, 2) + pow(y, 2)))
    w = (1) * w if x >= 0 else (-1) * w
    v = w - length_c
    alpha = atan2(z, v) + acos(
        (pow(length_a, 2) - pow(length_b, 2) + pow(v, 2) + pow(z, 2)) / 2 / length_a / sqrt(pow(v, 2) + pow(z, 2)))
    beta = acos((pow(length_a, 2) + pow(length_b, 2) - pow(v, 2) - pow(z, 2)) / 2 / length_a / length_b);
    gamma = atan2(y, x) if w >= 0 else atan2(-y, -x)
    return change_to_d(alpha), change_to_d(beta), change_to_d(gamma)


# def axis_to_angle_old(x, y, z):
#     # Maybe different sides of the legs?
#     if (x >= 0):
#         w = sqrt(pow(x, 2) + pow(y, 2))
#     else:
#         w = -1 * (sqrt(pow(x, 2) + pow(y, 2)))
#
#     v = w - COXA_LEN
#     alpha_tmp = (pow(FEMUR_LEN, 2) - pow(TIBIA_LEN, 2) + pow(v, 2) + pow(z, 2)) / 2 / FEMUR_LEN / sqrt(
#         pow(v, 2) + pow(z, 2))
#     if (alpha_tmp > 1 or alpha_tmp < -1):
#         print("x=%f y=%f v=%f w=%f" % (x, y, v, w))
#         print("alpha=%f" % alpha_tmp)
#         if (alpha_tmp > 1):
#             alpha_tmp = 1
#         else:
#             alpha_tmp = -1
#     alpha = atan2(z, v) + acos(alpha_tmp)
#
#     beta_tmp = (pow(FEMUR_LEN, 2) + pow(TIBIA_LEN, 2) - pow(v, 2) - pow(z, 2)) / 2 / FEMUR_LEN / TIBIA_LEN
#     if (beta_tmp > 1 or beta_tmp < -1):
#         print("x=%f y=%f v=%f w=%f" % (x, y, v, w))
#         print("beta=%f" % beta_tmp)
#         if (beta_tmp > 1):
#             beta_tmp = 1
#         else:
#             beta_tmp = -1
#     beta = acos(beta_tmp)
#
#     if (w >= 0):
#         gamma = atan2(y, x)
#     else:
#         gamma = atan2(-y, -x)
#
#     return (change_to_d(alpha), change_to_d(beta), change_to_d(gamma))


if __name__ == '__main__':
    # print(axis_to_angle(COXA_LEN + FEMUR_LEN + TIBIA_LEN, 0, 0))
    # print(COXA_LEN + FEMUR_LEN + TIBIA_LEN)
    # print(axis_to_angle(0, COXA_LEN + FEMUR_LEN + TIBIA_LEN, 0))
    print(axis_to_angle(x_default - x_offset, y_start + y_step, z_boot))
