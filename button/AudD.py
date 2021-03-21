import requests
import time
import sounddevice as sd
from scipy.io.wavfile import write
import json
import os
fs = 44100
duration = 6
audD_token = '83fa53ca5575a4850edb95f2a1a3202e' #'683508d338539f77485cbb6754c8d46e'


def get_recording():
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    #print(os.path.dirname(os.path.realpath(__file__)))
    write('output.wav', fs, recording)


def get_song_details():
    data = {
        'api_token': audD_token,
        'return': 'spotify',
    }
    #print(os.path.dirname(os.path.realpath(__file__)))
    files = {
        'file': open('output.wav', 'rb'),
    }
    time.sleep(0.02)
    result = requests.post('https://api.audd.io/', data=data, files=files)
    j_result = json.loads(result.text)
    print(j_result)
    try:
        return j_result["result"]["spotify"]["id"], j_result["result"]["spotify"]["artists"][0]["name"], j_result["result"]["spotify"]["name"]
    except:
        try:
            return j_result["result"]["spotify"]["id"], j_result["result"]["artist"], j_result["result"]["title"]
        except:
            return "", "", ""
