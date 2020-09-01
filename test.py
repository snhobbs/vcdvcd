#!/usr/bin/env python

import unittest

from vcdvcd import VCDVCD

class Test(unittest.TestCase):
    def test_data(self):
        vcd = VCDVCD('counter_tb.vcd')
        self.assertEqual(
            vcd.ref('counter_tb.out[1:0]')['tv'][:6],
            [
                ( 0,  'x'),
                ( 2,  '0'),
                ( 6,  '1'),
                ( 8, '10'),
                (10, '11'),
                (12,  '0'),
            ]
        )

if __name__ == '__main__':
    unittest.main()
