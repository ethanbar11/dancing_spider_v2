from math import sqrt, atan2, acos


def axis_to_angle_quad(x, y, z, spider):
    if (x >= 0):
        w = sqrt(pow(x, 2) + pow(y, 2))
    else:
        w = -1 * (sqrt(pow(x, 2) + pow(y, 2)))

    v = w - spider.coxa_len
    alpha_tmp = (pow(spider.femur_len, 2) - pow(spider.tibia_len, 2) + pow(v, 2) + pow(z,
                                                                                       2)) / 2 / spider.femur_len / sqrt(
        pow(v, 2) + pow(z, 2))
    if (alpha_tmp > 1 or alpha_tmp < -1):
        print("x=%f y=%f v=%f w=%f" % (x, y, v, w))
        print("alpha=%f" % alpha_tmp)
        if (alpha_tmp > 1):
            alpha_tmp = 1
        else:
            alpha_tmp = -1
    alpha = atan2(z, v) + acos(alpha_tmp)

    beta_tmp = (pow(spider.femur_len, 2) + pow(spider.tibia_len, 2) - pow(v, 2) - pow(z,
                                                                                      2)) / 2 / spider.femur_len / spider.tibia_len
    if (beta_tmp > 1 or beta_tmp < -1):
        print("x=%f y=%f v=%f w=%f" % (x, y, v, w))
        print("beta=%f" % beta_tmp)
        if (beta_tmp > 1):
            beta_tmp = 1
        else:
            beta_tmp = -1
    beta = acos(beta_tmp)

    if (w >= 0):
        gamma = atan2(y, x)
    else:
        gamma = atan2(-y, -x)
    return (alpha, beta, gamma)
