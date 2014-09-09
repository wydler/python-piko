import json
import socket
import struct
import hexdump

from piko.conf import settings


class Base(object):
    pass


class Packet(Base):
    """ PIKO packet class."""
    request = ''
    response = ''

    __is_packed = False
    __is_unpacked = False

    def __init__(self, code, address, pack=settings.AUTOPACK):
        self.request = '\x62%s\x03%s\x00%s' % (chr(address), chr(address), chr(code))
        if pack:
            self.pack()

    def pack(self):
        """Pack request packet."""
        if self.__is_packed:
            raise Exception('Packet is already packed.')
        self.request += '%s\x00' % (chr(self._generate_checksum()))
        self.__is_packed = True

    def is_packed(self):
        return self.__is_packed

    def unpack(self, pattern):
        """Unpack response packet."""
        if self.__is_unpacked:
            raise Exception('Packet is already unpacked.')
        self._verify_checksum()
        self.response = struct.unpack(pattern, self.response)
        self.__is_unpacked = True

    def is_unpacked(self):
        return self.__is_unpacked

    def _generate_checksum(self):
        """Generate checksum for packet."""
        chksum = 0
        for i in range(len(self.request)):
            chksum -= ord(self.request[i])
            chksum %= 256
        return chksum

    def _verify_checksum(self):
        """Verify packet checksum."""
        if len(self.response) < 2:
            raise ValueError('Packet too short.')
        chksum = 0
        for i in range(len(self.response) - 2):
            chksum -= ord(self.response[i])
            chksum %= 256
        if chksum != ord(self.response[-2]):
            raise ValueError('Checksum is wrong.')
        return True


class Socket(Base):
    """PIKO socket."""

    def __init__(self, *p):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, *p)
        self._sock.settimeout(5)

    def __getattr__(self, name):
        return getattr(self._sock, name)

    def connect(self, *p):
        """Connect to device."""
        self._sock.connect(*p)

    def disconnect(self):
        self._sock.close()

    def send(self, packet):
        """Send code to device."""
        if settings.DEBUG:
            print '#' * 76
            hexdump.hexdump(packet.request)
        self._sock.send(packet.request)

        packet.response = self._sock.recv(4096)
        if settings.DEBUG:
            print '-' * 76
            hexdump.hexdump(packet.response)
        return packet.response


class Device(Base):
    """Piko device class."""
    data = {}

    def __init__(self, host, port=81, addr=255):
        self.sock = Socket()
        self.host = host
        self.port = port
        self.addr = addr
        self.__prefix = '[%s:%d/%d]' % (host, port, addr)

    def __str__(self):
        return self.__prefix

    def connect(self):
        """Connect to host."""
        print "%s %s" % (self.__prefix, "Connecting".ljust(20, '.')),
        self.sock.connect((self.host, self.port))
        print "OK!"

    def disconnect(self):
        """Close connection with host."""
        print "%s %s" % (self.__prefix, "Disconnecting".ljust(20, '.')),
        self.sock.disconnect()
        print "OK!"

    def update(self):
        """Update all stats."""
        self.data = {}
        self._status()
        self._inverter()
        self._current()
        self._daily()
        self._total()

    def accumulate_power(self):
        """Calculate accumulated power."""
        return self.data['current']['ac_1'][2] + self.data['current']['ac_2'][2] + self.data['current']['ac_3'][2]

    def _status(self):
        """Get the current status."""
        packet = Packet(0x57, self.addr)
        self.sock.send(packet)
        packet.unpack('<xxxxxBBHxxxxBx')
        self.data['status'] = {
            'ens_s': packet.response[0],
            'ens_err': packet.response[1],
            'err': packet.response[2]
        }

    def _inverter(self):
        """Get the inverter data."""
        # Get inverter model.
        self.data['inverter'] = {}
        packet = Packet(0x90, self.addr)
        self.sock.send(packet)
        packet.unpack('<xxxxx16sBxxxxxxBxxxxBx')
        self.data['inverter']['model'] = packet.response[0].strip('\x00')
        self.data['inverter']['string'] = packet.response[1]
        self.data['inverter']['phase'] = packet.response[2]
        # Get inverter name.
        packet = Packet(0x44, self.addr)
        self.sock.send(packet)
        packet.unpack('<xxxxx15sBx')
        self.data['inverter']['name'] = packet.response[0].strip('\x00')
        # Get inverter serial number.
        packet = Packet(0x50, self.addr)
        self.sock.send(packet)
        packet.unpack('<xxxxx13sBx')
        self.data['inverter']['sn'] = packet.response[0]
        # Get item number.
        packet = Packet(0x51, self.addr)
        self.sock.send(packet)
        packet.unpack('<xxxxxIBx')
        self.data['inverter']['ref'] = hex(packet.response[0])

    def _current(self):
        """Get current energy."""
        packet = Packet(0x43, self.addr)
        self.sock.send(packet)
        packet.unpack('<xxxxxHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHBBBBBx')
        self.data['current'] = {}
        self.data['current']['dc_1'] = packet.response[0:5]
        self.data['current']['dc_2'] = packet.response[5:10]
        self.data['current']['dc_3'] = packet.response[10:15]
        self.data['current']['ac_1'] = packet.response[15:19]
        self.data['current']['ac_2'] = packet.response[19:23]
        self.data['current']['ac_3'] = packet.response[23:27]
        self.data['current']['ac_f'] = packet.response[28]
        self.data['current']['ac_s'] = packet.response[29]

    def _daily(self):
        """Get daily energy."""
        packet = Packet(0x9d, self.addr)
        self.sock.send(packet)
        packet.unpack('<xxxxxIBx')
        self.data['daily'] = packet.response[0]

    def _total(self):
        """Get total energy."""
        packet = Packet(0x45, self.addr)
        self.sock.send(packet)
        packet.unpack('<xxxxxIBx')
        self.data['total'] = packet.response[0]
