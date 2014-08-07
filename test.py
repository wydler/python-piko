#!/usr/bin/python

import piko
import sys
import traceback

if __name__ == "__main__":
    devices = (
        piko.Device('192.168.178.24', 81, 2),
        piko.Device('192.168.178.25', 81, 1),
        piko.Device('192.168.178.26', 81, 3)
    )

    try:
        piko.DEBUG = False
        total = 0
        for device in devices:
            device.connect()
            device.update()
            total += device.data['total']
            device.disconnect()
        print total
    except:
        print "Exception in user code:"
        print '-' * 60
        traceback.print_exc(file=sys.stdout)
        print '-' * 60