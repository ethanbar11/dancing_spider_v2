import spider_classes as sp
import time
import instructables_ik as IK
import motions

if __name__ == '__main__':
    print('hello')
    CSV_CONFIG_PATH = '/home/borat/spider_code/spider_base_positions.csv'
    spider = sp.Spider(CSV_CONFIG_PATH)
    # spider.stand()
    # time.sleep(2)
    # spider.step_forward()
    # spider.step_forward()
    # time.sleep(1)
    spider.dance_stand()
    time.sleep(2)
    for i in range(20):
        spider.ass_up(0.2, 50)
        time.sleep(0.1)
        spider.ass_down(0.2, 50)
        time.sleep(0.1)
    # time.sleep(1)
    # spider.ass_down()
    # time.sleep(1)
    # spider.dance_stand()
