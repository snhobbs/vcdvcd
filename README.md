# VCDVCD

Python Verilog value change dump (VCD) parser.

The format is defined by the Verilog standard, and can be generated with `$dumpvars`.

The entire VCD is parsed at once. For a stream implementation, see: <https://github.com/GordonMcGregor/vcd_parser>

Forked from Sameer Gauria's version, which is currently only hosted on PyPI with email patches and no public bug tracking: <https://pypi.python.org/pypi/Verilog_VCD>. There is also a read-only mirror at: <https://github.com/zylin/Verilog_VCD>

Library usage examples:

    python examples.py

Install:

    sudo python setup.py install

Nifty terminal CLI VCD viewer:

    ./vcdcat counter_tb.vcd

Sample output:

    0 time
    1 counter_tb.clock
    2 counter_tb.enable
    3 counter_tb.out[1:0]
    4 counter_tb.reset
    5 counter_tb.top.out[1:0]

    0 1 2 3 4 5
    ===========
    0 1 0 x 0 x
    1 0 0 x 1 x
    2 1 0 0 1 0
    3 0 0 0 0 0
    4 1 0 0 0 0
    5 0 1 0 0 0
    6 1 1 1 0 1
    7 0 1 1 0 1
    8 1 1 2 0 2
    9 0 1 2 0 2
    10 1 1 3 0 3
    11 0 1 3 0 3
    12 1 1 0 0 0
    13 0 1 0 0 0
    14 1 1 1 0 1
    15 0 1 1 0 1
    16 1 1 2 0 2
    17 0 1 2 0 2
    18 1 1 3 0 3
    19 0 1 3 0 3
    20 1 1 0 0 0
    21 0 1 0 0 0
    22 1 1 1 0 1
    23 0 1 1 0 1
    24 1 1 2 0 2
    25 0 0 2 0 2
