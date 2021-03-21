from flask import Flask, render_template, request, redirect, url_for, session
from random import randint
import time, singleSongParse, requests, threading

NUM_OF_GIFS = 4
SPIDER_IP = "192.168.1.12"
press_time = 0

app = Flask(__name__)


# @app.route('/', methods=['GET'])
# def index():
#     try:
#         rand_gif = session['rand_gif']
#     except:
#         rand_gif = -1
#     return render_template('index.html', content=[rand_gif])

@app.route('/', methods=['POST', 'GET'])
def btn_req():
    global press_time
    rand_gif = -1
    shtut = ''
    if request.method == "POST":
        rand_gif = randint(0, NUM_OF_GIFS - 1)
        press_time = time.time()
    elif request.method == 'GET' and request.args.get('q') == 'song':
        shtut = start_sniff()
        if not shtut:
            return render_template('index.html', content=[-3, shtut])
        rand_gif = -2
    return render_template('index.html', content=[rand_gif, shtut])

def start_sniff():
    global press_time
    start_time = press_time
    url = "http://" + SPIDER_IP + ":5000/start_sniffing"
    res = requests.post(url)
    print(res.text)

    speed_list, song_name, artist_name, spotify_id = singleSongParse.parse()
    stop_time = time.time()
    print(stop_time - start_time)
    if speed_list:
        url = "http://" + SPIDER_IP + ":5000/start_dancing"
        data = {
            "start_time": start_time,
            "speed_list": speed_list
        }
        res = requests.post(url, json=data)
        print(res.text)
        return str(spotify_id)
    else:
        print('bassa')
        return None
        # todo: handle fail...


if __name__ == '__main__':
    app.run()
