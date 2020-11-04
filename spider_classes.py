import math
import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit
import time
import instructables_ik as IK
import threading
from common_constants import *
import motions


def int_or_zero(x):
    try:
        return int(x)
    except:
        return 0


class Joint:
    def __init__(self, name, zero_a, zero_b, min_angle, max_angle, is_reversed, servo):
        self.name = name
        self.zero_a = 0
        self.zero_b = 0
        self.min = 0
        self.max = 180
        if is_reversed == 'V\n':
            self.reversed = True
        else:
            self.reversed = False
        self.servo = servo
        self.angle = None

    def set_angle(self, angle):
        self.servo.angle = angle
        self.angle = angle

    def straighten(self):
        self.servo.angle = self.zero_a


class Leg:
    def __init__(self, num, coxa_joint, femur_joint, tibia_joint):
        self.num = num
        self.coxa_joint = coxa_joint
        self.femur_joint = femur_joint
        self.tibia_joint = tibia_joint
        self.x = None
        self.y = None
        self.z = None

    @property
    def angles(self):
        return (self.coxa_joint.angle, self.femur_joint.angle, self.tibia_joint.angle)

    @property
    def pos(self):
        return self.x, self.y, self.z

    def straighten(self):
        self.coxa_joint.set_angle(90)
        self.femur_joint.set_angle(90)
        self.tibia_joint.set_angle(180)
        # self.set_angles_from_r(TOTAL, 0, 0)

    def get_up(self):
        self.set_angles_from_r(20, 20, -50)

    def add_hard_coded_angle_fix(self, a, b, g):
        return a + 90, b + 90, g

    def set_angles_from_r(self, x, y, z):
        a, b, g = IK.axis_to_angle(self.num, x, y, z)

        a, b, g = self.add_hard_coded_angle_fix(a, b, g)
        print('alpha : {} beta : {} gamma : {}'.format(a, b, g))

        self.coxa_joint.set_angle(a)
        self.femur_joint.set_angle(b)
        self.tibia_joint.set_angle(g)

        self.x = x
        self.y = y
        self.z = z

    def step_forward(self):
        if self.num == 1 or self.num == 4:
            self.perform_func_with_axis(STEP_TIME, SERVO_FREQUENCY, motions.silly_tan_walk_reversed,
                                        (x_default + x_offset, y_start, z_default))
        elif self.num == 2:
            self.perform_func_with_axis(STEP_TIME, SERVO_FREQUENCY, motions.silly_tan_walk, (25.3, -56.8, -50))
        elif self.num == 3:
            self.perform_func_with_axis(STEP_TIME, SERVO_FREQUENCY, motions.silly_tan_walk, (25.3, 56.8, -50))

    def move_heap_forward(self):
        angle_to_add = -33

        if self.num <= 2:
            angle_to_add *= -1
        current_angle = self.coxa_joint.angle
        self.coxa_joint.set_angle(current_angle + angle_to_add)
        self.x, self.y, self.z = IK.angle_to_axis(self.num, self.coxa_joint.angle,
                                                  self.femur_joint.angle,
                                                  self.tibia_joint.angle)

    def perform_func_with_axis(self, t, freq, func, end_pos=None):
        points = self.func2seg_axis(t, freq, func, end_pos)
        for point in points:
            print(point)
            self.set_angles_from_r(point[0], point[1], point[2])
            time.sleep(1 / freq)

    # def perform_func_with_angles(self, t, freq, func, end_pos=None):
    #     points = self.func2seg_axis

    # t is time
    def func2seg_axis(self, t, freq, func, end_pos=None):
        n = int(t * freq)
        return [func(self.pos, i / n, end_pos) for i in range(n + 1)]

    def func2seg_angles(self, t, freq, func, end_pos=None):
        n = int(t * freq)
        return [func(self.angles, i / n, end_pos) for i in range(n + 1)]


def get_servos_dictionary(kit):
    for i in range(16):
        kit.servo[i].set_pulse_width_range(500, 2400)
    return {'1A': kit.servo[2], '1B': kit.servo[1], '1C': kit.servo[0], '2A': kit.servo[6], '2B': kit.servo[5],
            '2C': kit.servo[4], '3A': kit.servo[10], '3B': kit.servo[9], '3C': kit.servo[8], '4A': kit.servo[14],
            '4B': kit.servo[13], '4C': kit.servo[12]}


class Spider:
    def __init__(self, csv_path):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = adafruit_pca9685.PCA9685(self.i2c)
        self.kit = ServoKit(channels=16)
        self.pca.frequency = 60
        self.joints = {}
        self.legs = []
        servos = get_servos_dictionary(self.kit)
        self.init_joints(csv_path, servos)
        self.init_legs()
        self.is_running = True

    def init_legs(self):
        for i in range(1, 5):
            leg = Leg(i, self.joints[str(i) + 'A'],
                      self.joints[str(i) + 'B'],
                      self.joints[str(i) + 'C'])
            self.legs.append(leg)

    def init_joints(self, csv_path, servos):
        with open(csv_path, 'r') as f:
            lines = f.readlines()[1:]
            for line in lines:
                splitted = line.split(',')
                name = splitted[0]
                joint = Joint(splitted[0], splitted[1], splitted[2], splitted[3],
                              splitted[4], splitted[5], servos[name])
                self.joints[name] = joint

    def straighten(self):
        for leg in self.legs:
            leg.straighten()
            time.sleep(0.01)

    def stand(self):
        self.legs[0].set_angles_from_r(x_default - x_offset, y_start + y_step, z_default)
        self.legs[1].set_angles_from_r(x_default - x_offset, -(y_start + y_step), z_default)
        self.legs[2].set_angles_from_r(x_default + x_offset, y_start, z_default)
        self.legs[3].set_angles_from_r(x_default + x_offset, y_start, z_default)

    def dance_stand(self):
        self.legs[0].set_angles_from_r(x_default, y_default, z_default)
        self.legs[1].set_angles_from_r(x_default, -y_default, z_default)
        self.legs[2].set_angles_from_r(x_default, y_default, z_default)
        self.legs[3].set_angles_from_r(x_default, -y_default, z_default)

    def step_forward(self):
        self.legs[2].step_forward()
        for leg in self.legs[::-1]:
            leg.move_heap_forward()
        time.sleep(0.5)
        self.legs[0].step_forward()
        self.legs[1].step_forward()
        for leg in self.legs[::-1]:
            leg.move_heap_forward()
        time.sleep(0.5)
        self.legs[3].step_forward()

    # Getting points for all for legs. We have same function for only one leg inside Leg.
    def func2seg_axis(self, t, freq, func, end_poses=None):
        n = int(t * freq)
        legs_points = []
        for idx, leg in enumerate(self.legs):
            legs_points.append([func(leg.pos, i / n, end_poses[idx]) for i in range(n + 1)])
        return legs_points

    # Performing function over all 4 legs. We have same function only for one leg inside Leg.
    def perform_func_with_axis(self, t, freq, func, end_poses=None):
        points = self.func2seg_axis(t, freq, func, end_poses)
        points_amount = len(points[0])
        for i in range(points_amount):
            for j in range(4):
                leg_num = j + 1
                point = points[j][i]
                print(leg_num, point)
                self.legs[j].set_angles_from_r(point[0], point[1], point[2])
            time.sleep(1 / freq)

    def ass_up(self, total_time, freq):
        end_poses = [(self.legs[0].pos[0], self.legs[0].pos[1], self.legs[0].pos[2] - 60),
                     self.legs[1].pos,
                     self.legs[2].pos,
                     (self.legs[3].pos[0], self.legs[3].pos[1], self.legs[3].pos[2] - 60)]
        self.perform_func_with_axis(total_time,
                                    freq,
                                    motions.move_leg_straight_line,
                                    end_poses)
        # self.legs[0].set_angles_from_r(self.legs[0].pos[0], self.legs[0].pos[1], self.legs[0].pos[2] - 60)
        # self.legs[3].set_angles_from_r(self.legs[3].pos[0], self.legs[3].pos[1], self.legs[3].pos[2] - 60)

    def ass_down(self, total_time, freq):
        end_poses = [(self.legs[0].pos[0], self.legs[0].pos[1], self.legs[0].pos[2] + 60),
                     self.legs[1].pos,
                     self.legs[2].pos,
                     (self.legs[3].pos[0], self.legs[3].pos[1], self.legs[3].pos[2] + 60)]
        self.perform_func_with_axis(total_time,
                                    freq,
                                    motions.move_leg_straight_line,
                                    end_poses)
