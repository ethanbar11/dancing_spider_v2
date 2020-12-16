import threading
import queue
import time
import random
import requests
import json
import urllib.request

start_time = time.time()

# ---------------------------------------
#
# get song name from microphone steam
#
# ---------------------------------------



def get_song_analysis(artist_name, song_name):
    # to be removed- currently for checking the delay logic
    # time.sleep(random.uniform(0.0, 3.0))
    rec_time = time.time()

    # print(rec_time-start_time)

    # ----------------------------------------------------------------------------
    # Get OAuth token

    post_headers = {
        'Authorization': 'Basic Zjk3ZmJjMmFlMGNjNGY1NDhhYWVlNWRjYmZmOGJhMmQ6MjA2NWI1ZTQ2YTBjNGNhZjg1NWZkODk4MWJlYjUzYTA=',
    }

    post_data = {
        'grant_type': 'client_credentials'
    }

    r = requests.post('https://accounts.spotify.com/api/token', headers=post_headers, data=post_data)
    j_response = json.loads(r.text)
    token = j_response['access_token']

    # ----------------------------------------------------------------------------
    # Get song id

    headers = {
        'Authorization': 'Bearer ' + token,
    }

    params = (
        ('q', 'track:' + song_name + ' artist:' + artist_name),
        ('type', 'track'),
    )
    track = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    j_track = json.loads(track.text)
    song_id = j_track['tracks']['items'][0]['id']
    # ----------------------------------------------------------------------------
    # Get song analysis
    # song_id = '7qCwgzeZQbNp6VHt9wz8i7?si=mc9XZcoKRN2scBpRwgOc5Q'

    get_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }

    analysis = requests.get('https://api.spotify.com/v1/audio-analysis/' + song_id, headers=get_headers)
    j_analysis = json.loads(analysis.text)
    # ----------------------------------------------------------------------------
    # Get list of tempos and duration

    curr_time_sig = 0
    curr_tempo = 0
    first_run = True
    tempo_list = []
    total_time = 0

    num_of_sec = 0
    tot_temp_conf = 0
    num_of_good_temp = 0

    for j in j_analysis['sections']:
        if j['time_signature_confidence'] > 0.5 or first_run:
            curr_time_sig = j['time_signature']
        if j['tempo_confidence'] > 0.5 or first_run:
            curr_tempo = j['tempo']
            first_run = False
        tempo_list.append([curr_tempo, curr_time_sig, j['duration'], j['loudness'],
                           str(int(total_time / 60)) + ":" + str(int((total_time / 60 - int(total_time / 60)) * 60)),
                           j['tempo_confidence']])
        total_time += j['duration']
        tot_temp_conf += j['tempo_confidence']
        num_of_sec += 1
        if j['tempo_confidence'] > 0.6:
            num_of_good_temp += 1
        # print("tempo: " + str(curr_tempo) + " | time signature: " + str(curr_time_sig) + " | duration: " + str(j['duration']) + "\n")
        # total_time += j['duration']

    for r in tempo_list:
        print(r)
    print("Conf Avg: " + str(tot_temp_conf / num_of_sec))
    print("Number of good Sections: " + str(num_of_good_temp))
    print("Number of Sections: " + str(num_of_sec))
    print("Song id: " + song_id)

    print("Total time: " + str(int(total_time / 60)) + ":" + str(int((total_time / 60 - int(total_time / 60)) * 60)))
    print("Total time in secs: ", total_time)

    offset = 0
    speed_lst = []
    tempo = tempo_list[0][0]
    curr_loud = 0
    time_dif = 0
    for i, l in enumerate(tempo_list):
        if abs(l[0] - tempo) > 10:
            time_dif = 60 / l[0]
        elif i == 0:
            time_dif = 60 / l[0]
            curr_loud = l[3]
        else:
            if l[3] <= -11:
                if l[3] - curr_loud >= 4:
                    time_dif /= 2
                    curr_loud = l[3]
            elif -11 <= l[3] <= -5:
                if l[3] - curr_loud >= 3:
                    time_dif /= 2
                    curr_loud = l[3]
                if l[3] - curr_loud <= -2:
                    time_dif *= 2
                    curr_loud = l[3]
            elif l[3] >= -5:
                if l[3] - curr_loud >= 2:
                    time_dif /= 2
                    curr_loud = l[3]
                if l[3] - curr_loud <= -2:
                    time_dif *= 2
                    curr_loud = l[3]
        for i in range(int((l[2] - offset) / time_dif) + 1):
            speed_lst.append(time_dif)
        offset = offset + (int((l[2] - offset) / time_dif) + 1) * time_dif - l[2]
    print(speed_lst)
    # list_for_snir = []
    # for i in speed_lst:
    #     list_for_snir.append(int(i*1000))
    # print(list_for_snir)
    print(sum(speed_lst))
    # ----------------------------------------------------------------------------
    # Test beats vs sections (tempo)
    # j = 1
    # for i in j_analysis['beats']:
    #     print(str(j) + " ")
    #     j += 1
    #     time.sleep(i['duration'])
    #     if j == 10:
    #         break

    # curr_time_sig = 0
    # curr_tempo = 0
    #
    # for j in j_analysis['sections']:
    #     k = 1
    #     if j['time_signature_confidence'] > 0:
    #         curr_time_sig = j['time_signature']
    #     if j['tempo_confidence'] > 0:
    #         curr_tempo = j['tempo']
    #     for r in range(int(curr_tempo * j['duration'] / 60)):
    #         print(str(k) + " ")
    #         k += 1
    #         time.sleep(60 / curr_tempo)
    #         if k == 10:
    #             break
    # # ----------------------------------------------------------------------------
    return speed_lst

if __name__ == '__main__':
    artist_name = "nicki minaj"
    song_name = "anaconda"
    print(get_song_analysis(artist_name,song_name))