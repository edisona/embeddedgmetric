#!/usr/bin/env python

import unittest
import binhex
from gmetric import gmetric_write, gmetric_read

class gmetricUnitTest(unittest.TestCase):

    def testWriteRead(self):
        # don't remember how I got this, but I think its directly 
        # from gmond
        result = "0000000000000006737472696e67000000000003666f6f00000000036261720000000000000000030000003c00000000"
        orig = {'SLOPE': 'both', 'NAME': 'foo', 'VAL': 'bar', 'TMAX': 60,
                'UNITS': '', 'DMAX': 0, 'TYPE': 'string'}

        buf = gmetric_write(**orig)
        self.assertEqual(48, len(buf))
        self.assertEqual(result, binhex.binascii.hexlify(buf))

        # now read it in!
        values = gmetric_read(buf)
        self.assertEqual(values, orig)

if __name__ == '__main__':
    unittest.main()
