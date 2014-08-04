import piko
import unittest

class TestPikoPacket(unittest.TestCase):
    def setUp(self):
        self.p = piko.Packet(0x40, 255, False)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual('b\xff\x03\xff\x00@', self.p.request)
        self.assertFalse(self.p.is_packed())

    def test_pack(self):
        pass

if __name__ == '__main__':
    unittest.main()