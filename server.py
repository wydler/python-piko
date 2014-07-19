#!/usr/bin/python
"""PyPIKO module."""

from gevent import monkey
monkey.patch_all()

import time
import piko
import traceback
import socket
from threading import Thread
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
users = 0
wrs = [
    piko.Device('192.168.178.25', 81, 1),
    piko.Device('192.168.178.24', 81, 2),
    piko.Device('192.168.178.26', 81, 3),
]


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        if users != 0:
            data = {
                'current': 0,
                'daily': 0,
                'total': 0
            }
            for wri in wrs:
                print "next"
                try:
                    wri.update()
                    data['current'] += wri.accumulate_power()
                    data['daily'] += wri.data['daily']
                    data['total'] += wri.data['total']
                except:
                    try:
                        wri.connect()
                    except socket.error as ex:
                        print ex
                    except:
                        traceback.print_exc()
            socketio.emit('update', {'data': data}, namespace='/piko')
        time.sleep(5)


@socketio.on('connect', namespace='/piko')
def connect():
    global users
    users += 1
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
