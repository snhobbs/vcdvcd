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

    vcdcat -h

Dump all signal values:

    vcdcat counter_tb.vcd

Output:

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

Dump all deltas:

    vcdcat -d counter_tb.vcd

Output:

    0 x counter_tb.top.out[1:0]
    0 0 counter_tb.reset
    0 0 counter_tb.enable
    0 1 counter_tb.clock
    0 x counter_tb.out[1:0]
    1 0 counter_tb.clock
    1 1 counter_tb.reset
    2 0 counter_tb.out[1:0]
    2 0 counter_tb.top.out[1:0]
    2 1 counter_tb.clock
    3 0 counter_tb.clock
    3 0 counter_tb.reset
    4 1 counter_tb.clock
    5 0 counter_tb.clock
    5 1 counter_tb.enable
    6 1 counter_tb.out[1:0]
    6 1 counter_tb.top.out[1:0]
    6 1 counter_tb.clock
    7 0 counter_tb.clock
    8 2 counter_tb.out[1:0]
    8 2 counter_tb.top.out[1:0]
    8 1 counter_tb.clock
    9 0 counter_tb.clock
    10 3 counter_tb.out[1:0]
    10 3 counter_tb.top.out[1:0]
    10 1 counter_tb.clock
    11 0 counter_tb.clock
    12 0 counter_tb.out[1:0]
    12 0 counter_tb.top.out[1:0]
    12 1 counter_tb.clock
    13 0 counter_tb.clock
    14 1 counter_tb.out[1:0]
    14 1 counter_tb.top.out[1:0]
    14 1 counter_tb.clock
    15 0 counter_tb.clock
    16 2 counter_tb.out[1:0]
    16 2 counter_tb.top.out[1:0]
    16 1 counter_tb.clock
    17 0 counter_tb.clock
    18 3 counter_tb.out[1:0]
    18 3 counter_tb.top.out[1:0]
    18 1 counter_tb.clock
    19 0 counter_tb.clock
    20 0 counter_tb.out[1:0]
    20 0 counter_tb.top.out[1:0]
    20 1 counter_tb.clock
    21 0 counter_tb.clock
    22 1 counter_tb.out[1:0]
    22 1 counter_tb.top.out[1:0]
    22 1 counter_tb.clock
    23 0 counter_tb.clock
    24 2 counter_tb.out[1:0]
    24 2 counter_tb.top.out[1:0]
    24 1 counter_tb.clock
    25 0 counter_tb.clock
    25 0 counter_tb.enable
    26 1 counter_tb.clock
