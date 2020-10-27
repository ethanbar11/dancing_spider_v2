import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit
import time


def get_servos_dictionary(kit):
    for i in range(16):
        kit.servo[i].set_pulse_width_range(500, 2400)

    return {'1A': kit.servo[2], '1B': kit.servo[1], '1C': kit.servo[0], '2A': kit.servo[6], '2B': kit.servo[5],
            '2C': kit.servo[4], '3A': kit.servo[10], '3B': kit.servo[9], '3C': kit.servo[8], '4A': kit.servo[14],
            '4B': kit.servo[13], '4C': kit.servo[12]}


if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = adafruit_pca9685.PCA9685(i2c)
    kit = ServoKit(channels=16)
    pca.frequency = 60
    servos = get_servos_dictionary(kit)
    for servo_name in servos.keys():
        servos[servo_name].angle = 90
        print(servo_name,str(servos[servo_name].angle))
        time.sleep(0.1)
