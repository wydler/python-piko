#!/usr/bin/python
"""PyPIKO module."""

from gevent import monkey
monkey.patch_all()

import time
import piko
from threading import Thread
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'aA9CqNkMdvSC7PT'
socketio = SocketIO(app)
thread = None
users = 0
wrs = [
    piko.Device('192.168.0.29'),
    piko.Device('192.168.0.39')
]


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        if users != 0:
            data = {
                'current': -1,
                'daily': -1,
                'total': -1
            }
            for wri in wrs:
                wri.update()
                data['current'] += wri.accumulate_power()
                data['daily'] += wri.data['daily']
                data['total'] += wri.data['total']
            socketio.emit('update', {'data': data}, namespace='/piko')
        time.sleep(2)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/piko')
def connect():
    global users
    users += 1
    if users == 1:
        for wri in wrs:
            wri.connect()
    global thread
    if thread is None:
        print 'start thread'
        thread = Thread(target=background_thread)
        thread.start()
    emit('system', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/piko')
def disconnect():
    global users
    users -= 1
    if users == 0:
        for wri in wrs:
            wri.disconnect()
    print 'Client disconnected'


if __name__ == '__main__':
    socketio.run(app)
