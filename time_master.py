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

        # Being used as the total time of the current movement
        # And the index being added in the add of the movement
        self.time_to_wait = 0
        self.idx_to_add_in_end = 1

        self.idx = 0

    def start_movement(self, movement=None):
        self.time_to_wait = self.times[self.idx] + self.diff_to_add
        self.idx_to_add_in_end = 1
        if movement:
            while self.time_to_wait < movement.min_time:
                self.time_to_wait += self.times[self.idx + self.idx_to_add_in_end]
                self.idx_to_add_in_end += 1
        self.current_movement_start_time = time.time()
        return self.time_to_wait

    # Part should be \in R, 0<part<=1
    def part_of_movement(self, part):
        busy_wait(self.current_movement_start_time, self.time_to_wait * part)

    def end_movement(self):
        self.part_of_movement(1)
        self.diff_to_add = self.log_and_return_diff()
        self.idx += self.idx_to_add_in_end

    def get_right_time(self):
        return sum(self.times[:self.idx + self.idx_to_add_in_end])

    def log_and_return_diff(self):
        should_be = self.get_right_time()
        actual = time.time() - self.start_time
        diff = should_be - actual
        if diff > 0.002:
            print('Should be : {} , Actual : {} Diff : {} Chunks : {}'.format(should_be, actual, diff,
                                                                              self.idx_to_add_in_end))
        return diff
