import time

from common_constants import MAX_DIFF_BETWEEN_BIT_AND_REAL_IN_SEC


def busy_wait(start_time, total_action_time):
    while time.time() - start_time < total_action_time:
        pass


class TimeMaster:
    def __init__(self, times):
        self.times = times
        self.start_time = time.time()
        self.current_movement_start_time = None
        self.diff_to_add = 0
        self.idx = 0

    def start_movement(self):
        self.current_movement_start_time = time.time()

    # Part should be \in R, 0<part<=1
    def part_of_movement(self, part):
        time_to_wait = self.times[self.idx] + self.diff_to_add
        busy_wait(self.current_movement_start_time, time_to_wait * part)

    def end_movement(self):
        self.part_of_movement(1)
        self.diff_to_add = self.log_and_return_diff()
        # if abs(diff) > MAX_DIFF_BETWEEN_BIT_AND_REAL_IN_SEC:
        #     self.diff_to_add =  diff
        # else:
        # self.diff_to_add = 0
        self.idx += 1


    def get_right_time(self):
        return sum(self.times[:self.idx + 1])


    def log_and_return_diff(self):
        should_be = self.get_right_time()
        actual = time.time() - self.start_time
        diff = should_be - actual
        print('Should be : {} , Actual : {} Diff : {}'.format(should_be, actual, diff))
        return diff
