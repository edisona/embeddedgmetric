#!/usr/bin/env python

import unittest
import binhex
from gmetric import Gmetric

class gmetricUnitTest(unittest.TestCase):

    def testXdr(self):
        result = "0000000000000006737472696e67000000000003666f6f00000000036261720000000000000000030000003c00000000"
        g = Gmetric("127.0.0.1", 8649, 'udp')
        buf = g.makexdr("foo", "bar", "string", "", "both", 60, 0)
        self.assertEqual(48, len(buf))
        self.assertEqual(result, binhex.binascii.hexlify(buf))

if __name__ == '__main__':
    unittest.main()
