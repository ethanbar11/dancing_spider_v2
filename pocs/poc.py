import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit
import time


class Joint:
    def __init__(self, ctrl, angle, invert):
        self.ctrl = ctrl
        self.standing_angle = angle
        self.do_invert = invert
        # self.ctrl.set_pulse_width_range(500,2400)

    def set_angle(self, angle):
        if self.do_invert:
            self.ctrl.angle = 180 - angle
        else:
            self.ctrl.angle = angle


class Leg:
    def __init__(self, num, joints):
        self.joints = joints


class Spider:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = adafruit_pca9685.PCA9685(self.i2c)
        self.kit = ServoKit(channels=16)
        self.pca.frequency = 60
        self.legs = []
        joint1 = Joint(self.kit.servo[2],0,False)
        # joint2 = Joint(self.kit.servo[10], 0,False)
        # joint3 = Joint(self.kit.servo[10], 10,True)
        joint1.set_angle(180)
        # for i in range(100, 900):
        #     joint2.ctrl.angle = i / 10
        #     time.sleep(0.01)
        # joint2.ctrl.angle = 10
        # joints1 = {'A':}
        # for i in range(4):
        #     index = i * 4
        #     self.legs.append({'C': self.kit.servo[index],
        #                       'B': self.kit.servo[index + 1],
        #                       'A': self.kit.servo[index + 2]})

    def stand(self):
        # self.legs[0]['A'].angle=30
        for leg in self.legs:
            for key, val in leg.items():
                val.angle = 90
                time.sleep(0.001)
        # time.sleep(1)
print('woho')
# def stand(pca):
if __name__ == '__main__':
    spider = Spider()
    # spider.stand()
