import spider_classes as sp
import time
import instructables_ik as IK

if __name__ == '__main__':
    CSV_CONFIG_PATH = '/home/borat/spider_code/spider_base_positions.csv'
    spider = sp.Spider(CSV_CONFIG_PATH)
    spider.straighten()
    time.sleep(2)
    # spider.get_up()
    # spider.legs[1].tibia_joint.set_angle(79)
    # spider.legs[0].get_up()
    # spider.legs[0].get_up()
    # spider.legs[0].tibia_joint.set_angle(150)
    # spider.legs[0].tibia_joint.servo.angle=50
    # spider.legs[0].coxa_joint.servo.angle=100
    # spider.straighten()
    # time.sleep(1)
    # spider.legs[2].tibia_joint.set_angle(100)
    # spider.legs[3].tibia_joint.set_angle(100)
    # spider.legs[1].tibia_joint.set_angle(100)
    # time.sleep(1)
    # spider.legs[2].femur_joint.set_angle(60)
    # spider.legs[3].femur_joint.set_angle(60)
    # spider.legs[1].femur_joint.set_angle(60)
    # points = [(62, 40, -28), (62, 0, -28), (62, 0, -28), (62, 40, -28)]
    # spider.move_legs_to_points(points, 5)
    # time.sleep(2)

    # points = [(10, 30, -10) for i in range(4)]
    # spider.move_legs_to_points(points, 2)
    # spider.stand()
    # spider.lay()
    # IK.axis_to_angle(IK.COXA_LEN + IK.FEMUR_LEN, 0, -50)
    # IK.axis_to_angle(IK.COXA_LEN + IK.FEMUR_LEN, 0, -50)
