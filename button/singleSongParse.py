import requests
import json
import AudD

spotify_auth = "Basic Zjk3ZmJjMmFlMGNjNGY1NDhhYWVlNWRjYmZmOGJhMmQ6MjA2NWI1ZTQ2YTBjNGNhZjg1NWZkODk4MWJlYjUzYTA="


def parse():
    # ----------------------------------------------------------------------------
    # Record music and get song details
    AudD.get_recording()
    song_id, artist_name, song_name = AudD.get_song_details()
    if song_name == "":
        return [], "", "", ""
    # ----------------------------------------------------------------------------
    # Get OAuth token
    post_headers = {
        'Authorization': spotify_auth,
    }

    post_data = {
        'grant_type': 'client_credentials'
    }

    r_token = requests.post('https://accounts.spotify.com/api/token', headers=post_headers, data=post_data)
    j_r_token = json.loads(r_token.text)
    token = j_r_token['access_token']

    # ----------------------------------------------------------------------------
    # Get song id (only if failed in AudD
    if song_id == "":
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
    get_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }

    analysis = requests.get('https://api.spotify.com/v1/audio-analysis/' + song_id, headers=get_headers)
    j_analysis = json.loads(analysis.text)
    # ----------------------------------------------------------------------------
    # Get list of tempos and duration

    curr_tempo = 0
    first_run = True
    tempo_list = []
    total_time = 0

    for j in j_analysis['sections']:
        if j['tempo_confidence'] > 0.5 or first_run:
            curr_tempo = j['tempo']
            first_run = False
        tempo_list.append([curr_tempo, j['time_signature'], j['duration'], j['loudness'],
                           str(int(total_time / 60)) + ":" + str(int((total_time / 60 - int(total_time / 60)) * 60)),
                           j['tempo_confidence']])
        total_time += j['duration']

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
        elif i != 1 or tempo_list[i - 1][2] > 20:
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
    return speed_lst, song_name, artist_name, song_id
