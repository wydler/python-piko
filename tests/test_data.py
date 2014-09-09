import sys
import traceback

from piko.conf import settings
from piko.models import Device


if __name__ == "__main__":
    devices = (
        Device('192.168.0.39', 81, 255),
        Device('192.168.0.29', 81, 255),
    )

    try:
        settings.DEBUG = False
        total = 0
        for device in devices:
            device.connect()
            device.update()
            print str(device) + " Total: " + str(device.data['total'])
            total += device.data['total']
            device.disconnect()
        print "Total: " + str(total)
    except:
        print "Exception in user code:"
        print '-' * 60
        traceback.print_exc(file=sys.stdout)
        print '-' * 60
