import spider_classes as sp
import time
import instructables_ik as IK
import motions

if __name__ == '__main__':
    print('hello')
    CSV_CONFIG_PATH = '/home/borat/spider_code/spider_base_positions.csv'
    spider = sp.Spider(CSV_CONFIG_PATH)
    spider.stand()
    time.sleep(3)
    spider.step_forward()
    spider.step_forward()
    spider.step_forward()

