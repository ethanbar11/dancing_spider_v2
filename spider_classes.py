import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit
import time
import instructables_ik as IK

# In seconds
DEFAULT_DELAY = 0.02


def rest():
    time.sleep(0.01)


def int_or_zero(x):
    try:
        return int(x)
    except:
        return 0


class Joint:
    def __init__(self, name, zero_a, zero_b, min_angle, max_angle, is_reversed, servo):
        self.name = name
        self.zero_a = int_or_zero(zero_a)
        self.zero_b = int_or_zero(zero_b)
        self.min = int_or_zero(min_angle)
        self.max = int_or_zero(max_angle)
        if is_reversed == 'V\n':
            self.reversed = True
        else:
            self.reversed = False
        self.servo = servo

    def set_angle(self, angle):
        if self.reversed:
            new_angle = self.zero_a - angle
        else:
            new_angle = self.zero_a + angle
        if new_angle > self.max:
            self.servo.angle = self.max
        elif new_angle < self.min:
            self.servo.angle = self.min
        else:
            self.servo.angle = new_angle

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

    def straighten(self):
        # self.set_angles_from_r(IK.COXA_LEN + IK.FEMUR_LEN+IK.TIBIA_LEN, 0, 0)
        self.coxa_joint.straighten()
        rest()
        self.femur_joint.straighten()
        rest()
        self.tibia_joint.straighten()
        rest()
        self.x = IK.TOTAL
        self.y = 0
        self.z = 0

    def get_up(self):
        self.set_angles_from_r(70, 90, 100)

    def add_delta(self, x_delta, y_delta, z_delta):
        new_x = self.x + x_delta
        new_y = self.y + y_delta
        new_z = self.z + z_delta
        self.set_angles_from_r(new_x, new_y, new_z)

    def is_leg_in(self, point):
        if self.x != point[0] \
                or self.y != point[1] \
                or self.z != point[2]:
            return False
        return True

    def set_angles_from_r(self, x, y, z):
        a, b, g = IK.axis_to_angle(x, y, z)
        print('alpha : {} beta : {} gamma : {}'.format(a, b, g))
        self.tibia_joint.set_angle(a)
        time.sleep(0.1)

        self.femur_joint.set_angle(b)
        time.sleep(0.1)

        self.coxa_joint.set_angle(g)
        time.sleep(0.1)

        self.x = x
        self.y = y
        self.z = z

    def lay(self):
        self.set_angles_from_r(IK.COXA_LEN + IK.FEMUR_LEN + IK.TIBIA_LEN, 0, 0)


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

    def get_up(self):
        for leg in self.legs:
            leg.get_up()

    def lay(self):
        for leg in self.legs:
            leg.lay()

    def is_legs_in(self, points):
        for idx, leg in enumerate(self.legs[1:]):
            if not leg.is_leg_in(points[idx]):
                return False
        return True

    # A list containing tuples items (x,y,z) each.
    def move_legs_to_points(self, points, total_time, delay=DEFAULT_DELAY):
        legs_deltas = self.get_legs_deltas(delay, points, total_time)
        i = 0
        while not self.is_legs_in(points):
            i += 1
            for idx, leg in enumerate(self.legs[1:]):
                if not leg.is_leg_in(points[idx]):
                    leg.add_delta(legs_deltas[idx][0], legs_deltas[idx][1], legs_deltas[idx][2])
            time.sleep(delay)
        pass

    def get_legs_deltas(self, delay, points, total_time):
        legs_deltas = []
        points_amount = total_time / (delay + 0)
        for idx, leg in enumerate(self.legs):
            x_delta = (points[idx][0] - leg.x) / points_amount
            y_delta = (points[idx][1] - leg.y) / points_amount
            z_delta = (points[idx][2] - leg.z) / points_amount
            legs_deltas.append([x_delta, y_delta, z_delta])
        return legs_deltas

    def move_30(self):
        for i in range(16):
            self.kit.servo[i].angle = 30