from pocs.quad_robot import QuadRobot
from pocs import inverse_kinematics

if __name__ == '__main__':
    coxa_len = 27.5
    femur_len = 70
    tibia_len = 80
    robot = QuadRobot(coxa_len, femur_len, tibia_len)
    angles= inverse_kinematics.axis_to_angle_quad(0, coxa_len + femur_len + tibia_len, 0, robot)
    print(angles)
