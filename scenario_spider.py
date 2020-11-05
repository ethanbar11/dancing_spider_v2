from spider_classes import *
# import robot_server
import random
import analyze_song
import poses, movements


class SpiderScenario:
    def __init__(self, csv_path):
        self.spider = Spider(csv_path)
        robot_server.app.run()
        self.current_pose = None

        # Register events to flask functions.
        pass

        # Going to base position and waiting for start sniffing.
        self.spider.stand()

    def start_sniffing(self):
        # Should write here code to walk forward, backwards and
        # move for the sides to illustrate sniffing (!!).
        pass

    def start_dancing(self, times, start_time):
        # This part should be changed
        times_by_beat_to_dance = analyze_song.get_song_analysis("anaconda", "nicky minaj")
        # Yeah right here it ends
        self.current_pose = poses.Stand(self.spider)
        self.current_pose.perform_pose(times_by_beat_to_dance[0])
        idx = 1
        while idx < len(times_by_beat_to_dance):
            t = times_by_beat_to_dance[idx]
            move_to_other_pose = poses.next_action_movement_or_pose()
            if move_to_other_pose:
                self.current_pose = random.choice(self.current_pose.connected_poses)
                self.current_pose.perform_pose(t)
                idx += 1
            else:
                move_to_make = random.choice(self.current_pose.movements)
                times_to_make_move = random.randint(move_to_make.min_reps, move_to_make.max_reps)
                for t in times_by_beat_to_dance[idx:idx + times_to_make_move]:
                    move_to_make.perform_move(t, freq=SERVO_FREQUENCY)
                idx += times_to_make_move
