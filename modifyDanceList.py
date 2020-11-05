import time

def get_modified_list(dance_times, start_time):
    time_sum = 0
    final_dance_times = []
    start_appending = False
    point_found = False
    freeze_time = 0
    for i in dance_times:
        if start_appending:
            final_dance_times.append(i)
            continue
        time_sum += i
        diff = time.time() - start_time
        if time_sum > diff and not point_found:
            point_found = True
            freeze_time += time_sum - diff
            continue
        if point_found:
            freeze_time += i
        if freeze_time >= 1:
            final_dance_times.append(freeze_time)
            start_appending = True
    return final_dance_times




