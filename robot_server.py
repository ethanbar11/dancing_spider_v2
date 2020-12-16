from flask import Flask, request
from pubsub import pub

app = Flask(__name__)


@app.route('/start_sniffing', methods=['POST'])
def start_sniffing():
    return 'woho'


@app.route('/start_dancing', methods=['POST'])
def start_dancing():
    data = request.get_json()
    start_time = data['start_time']
    speed_list = data['speed_list']
    pub.sendMessage('start_dancing',times= speed_list, start_time=start_time)
    return 'Snir1996 is our password! You should know it and spread the word. :(. I love you. But i hate you. life is so hard sometimes really. Ooh'

# if __name__ == '__main__':
#     app.run()
