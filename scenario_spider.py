from spider_classes import *
# import robot_server
import random
import analyze_song
import poses
import modifyDanceList


class SpiderScenario:
    def __init__(self, csv_path):
        self.spider = Spider(csv_path)
        # robot_server.app.run()
        self.current_pose = None

        self.stand = poses.Stand(self.spider)
        self.dance_stand = poses.DanceStand(self.spider)
        self.hump_stand = poses.HumpStand(self.spider)

        self.stand.connected_poses = [self.dance_stand, self.hump_stand]
        self.dance_stand.connected_poses = [self.stand, self.hump_stand]
        self.hump_stand.connected_poses = [self.stand, self.dance_stand]

        # Going to base position and waiting for start sniffing.
        self.current_pose = self.stand
        self.current_pose.perform_pose(time.time(), 0.5)

    def start_sniffing(self):
        # Should write here code to walk forward, backwards and
        # move for the sides to illustrate sniffing (!!).
        self.spider.step_forward()

    def start_dancing(self, times, start_time):
        # times_by_beat_to_dance = modifyDanceList.get_modified_list(times, start_time)
        times_by_beat_to_dance = analyze_song.get_song_analysis("nicki minaj", "anaconda")
        # Yeah right here it ends
        start_time = time.time()
        self.current_pose = self.stand
        self.current_pose.perform_pose(start_time, times_by_beat_to_dance[0])
        idx = 1
        while idx < len(times_by_beat_to_dance):
            start_time = time.time()
            t = times_by_beat_to_dance[idx]
            move_to_other_pose = poses.next_action_movement_or_pose()
            if move_to_other_pose:
                self.current_pose = random.choice(self.current_pose.connected_poses)
                self.current_pose.perform_pose(start_time, t)
                idx += 1
            else:
                move_to_make = random.choice(self.current_pose.movements)
                times_to_make_move = random.randint(move_to_make.min_reps, move_to_make.max_reps)
                for t in times_by_beat_to_dance[idx:idx + times_to_make_move]:
                    move_to_make.perform_move(start_time, t, freq=SERVO_FREQUENCY)
                    start_time = time.time()
                idx += times_to_make_move
