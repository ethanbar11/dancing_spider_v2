import movements
import spider_classes as sp
import scenario_spider
from pubsub import pub
import robot_server
import time
 
if __name__ == '__main__':
    print('hello')
    artist_name = "nicki minaj"
    song_name = "anaconda"
    CSV_CONFIG_PATH = './spider_base_positions.csv'

    scen = scenario_spider.SpiderScenario(CSV_CONFIG_PATH)
    scen.start_dancing(None, None)
    # Working IMPORTANT
    # pub.subscribe(scen.start_dancing, 'start_dancing')
    # robot_server.app.run('0.0.0.0')
    # Working IMPORTANT ENDING
    # scen.start_dancing()
# from analyze_song import get_song_analysis
#
# if __name__ == '__main__':
#     print('hello')
#     artist_name = "nicki minaj"
#     song_name = "anaconda"
#     CSV_CONFIG_PATH = '/home/borat/spider_code/spider_base_positions.csv'
#     spider = sp.Spider(CSV_CONFIG_PATH)
#     spider.hump_stand()
#     times = get_song_analysis(artist_name, song_name)
#     time.sleep(1)
#     hump = movements.Hump(spider)
#     for idx, t in enumerate(times):
#         hump.perform_move(t, freq=50)
#         start = time.time()
#         # spider.legs[2].perform_func_with_axis(t * 9.0 / 10, 50, motions.leg_up_and_down)
#         # for i in range(2):
#         spider.hump_forward(t * 3 / 5 / 2, 50)
#         spider.hump_forward(t * 3 / 5 / 2, 50, backwords=True)
#         # if idx>100:
#         # print(sp.sum1/sp.counter,sp.sum1,sp.counter)
#         while time.time() - start < t:
#             pass
#         print(t, time.time() - start)
#         # if idx>100:
#         #     print(sp.counter*100/sp.total_n,'%')
#     # cProfile.run('spider.legs[2].perform_func_with_axis(times[0] - 0.08, 50, motions.leg_up_and_down)',sort=2)
#     spider.head_down()
