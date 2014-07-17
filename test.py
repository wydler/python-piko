#!/usr/bin/python

import piko
import sys
import traceback

if __name__ == "__main__":
    try:
        piko.DEBUG = True
        wr1 = piko.Device('192.168.178.24', 81, 2)
        wr1.connect()
        wr1.update()
        print wr1.data
        wr1.disconnect()
    except:
        print "Exception in user code:"
        print '-' * 60
        traceback.print_exc(file=sys.stdout)
        print '-' * 60