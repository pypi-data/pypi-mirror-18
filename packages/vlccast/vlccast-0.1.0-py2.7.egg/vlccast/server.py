#!/usr/bin/env python
import atexit
import os
import socket
import subprocess
import time

import youtube_dl

from flask import Flask, request, jsonify

this_dir, this_filename = os.path.split(__file__)
static_path = os.path.join(os.path.abspath(this_dir), '../static/')
print(static_path)
print(os.getcwd())

app = Flask(__name__, static_folder=static_path, static_url_path='/static/')

vlc = None


def stop_vlc():
    if vlc is not None:
        vlc.terminate()


def start_vlc():
    global vlc
    vlc = subprocess.Popen(["vlc", "--qt-minimal-view", "--extraintf", "rc", "--rc-host", "localhost:9999"])


def get_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9999))
    time.sleep(0.1)
    s.recv(500)
    return s


def send_command(s, cmd):
    s.send(cmd + '\n')
    time.sleep(0.1)
    result = s.recv(500)
    if result != '> ':
        return result[:-4]


def quick_command(cmd):
    conn = get_connection()
    result = send_command(conn, cmd)
    conn.close()
    return result


def get_best_video(data):
    best = {'width': 0}
    for f in data['formats']:
        if f['acodec'] != 'none':
            if f['width'] > best['width']:
                best = f
    return best


@app.route('/api/player/play', methods=['POST'])
def play():
    data = request.get_json()

    ydl = youtube_dl.YoutubeDL()
    youtube_data = ydl.extract_info(data['video_id'], download=False)
    video = get_best_video(youtube_data)

    conn = get_connection()
    send_command(conn, 'add ' + video['url'])
    for i in range(10):
        length = int(send_command(conn, 'get_length'))
        if length != 0:
            break
        time.sleep(0.1)
    volume = send_command(conn, 'volume')
    conn.close()

    return jsonify(
        length=length,
        volume=int(volume),
    )


@app.route('/api/player/pause', methods=['POST'])
def pause():
    quick_command('pause')
    return ('', 204)


@app.route('/api/player/stop', methods=['POST'])
def stop():
    quick_command('stop')
    return ('', 204)


@app.route('/api/player/volume', methods=['GET', 'POST'])
def volume():
    if request.method == 'POST':
        data = request.get_json()
        quick_command('volume ' + str(data['volume']))
        return ('', 204)
    else:
        return jsonify(volume=int(quick_command('volume')))


@app.route('/api/player/rate', methods=['POST'])
def rate():
    data = request.get_json()
    quick_command('rate ' + str(data['rate']))
    return ('', 204)


@app.route('/api/player/seek', methods=['POST'])
def seek():
    data = request.get_json()
    quick_command('seek ' + str(data['time']))
    return ('', 204)


@app.route('/api/player/status', methods=['GET'])
def status():
    conn = get_connection()
    time = send_command(conn, 'get_time')
    playing = send_command(conn, 'is_playing')
    conn.close()
    return jsonify(
        playing=bool(playing),
        time=int(time) if time else None,
    )


@app.route('/')
@app.route('/<path:p>')
def index(p=None):
    print(p)
    return app.send_static_file('index.html')


def start():
    atexit.register(stop_vlc)
    start_vlc()

    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    start()
