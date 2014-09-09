#!/usr/bin/python
"""PyPIKO module."""

from gevent import monkey
monkey.patch_all()

import itertools

from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask.ext.socketio import SocketIO, emit
from threading import Thread

from piko.models import Device
from piko.conf import settings as piko_settings
from piko.db import session, History

from piko import history as history_update


app = Flask(__name__, static_url_path='')
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
users = 0
wrs = [
    Device('192.168.0.29', 81, 255),
    Device('192.168.0.39', 81, 255),
]


def background_thread():
    """Example of how to send server generated events to clients."""
    global d
    while True:
        data = {
            'time': datetime.datetime.now(),
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
        if data['total'] != 0:
            socketio.emit('update', {'data': data}, namespace='/piko')
        time.sleep(10)


@app.route('/')
def index():
    global thread
    if thread is None:
        print 'start thread'
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/_history', methods=["POST"])
def _history():
    type = request.form['type']
    query = session.query(History).filter(History.time > piko_settings.START_DATE).order_by(History.time).all()
    results = [i.serialize for i in query]
    if type == 'yield':
        results = [(int(dt.strftime('%s')) * 1000, sum(v for d, v in grp) / 4 / 1000.0) for dt, grp in itertools.groupby(results, key=lambda x: datetime.fromtimestamp(x[0] / 1000).replace(minute=30))]
        results = sorted(results, key=lambda x: x[0])
    elif type == 'power':
        pass
    return jsonify(type=type, result=results)


@app.route('/_history_update', methods=["POST"])
def _history_update():
    history_update.update()
    return _history()


@app.route('/settings')
def settings():
    return render_template('settings.html')


@socketio.on('connect', namespace='/piko')
def connect():
    global users
    global d
    users += 1
    emit('system', {'data': 'Connected'})
    emit('init', {'data': list(d)})


@socketio.on('disconnect', namespace='/piko')
def disconnect():
    global users
    users -= 1
    if users == 0:
        for wri in wrs:
            wri.disconnect()
    print 'Client disconnected'


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
