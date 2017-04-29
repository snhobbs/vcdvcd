# Verilog VCD

Verilog VCD value change dump parser.

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

    counter_tb.out[1:0]
    counter_tb.enable
    counter_tb.clock
    counter_tb.top.out[1:0]
    counter_tb.reset

    0 x x x x x
    1 x 0 1 x 0
    2 x 0 0 x 1
    3 0 0 1 0 1
    4 0 0 0 0 0
    5 0 0 1 0 0
    6 0 1 0 0 0
    7 1 1 1 1 0
    8 1 1 0 1 0
    9 10 1 1 10 0
    10 10 1 0 10 0
    11 11 1 1 11 0
    12 11 1 0 11 0
    13 0 1 1 0 0
    14 0 1 0 0 0
    15 1 1 1 1 0
    16 1 1 0 1 0
    17 10 1 1 10 0
    18 10 1 0 10 0
    19 11 1 1 11 0
    20 11 1 0 11 0
    21 0 1 1 0 0
    22 0 1 0 0 0
    23 1 1 1 1 0
    24 1 1 0 1 0
    25 10 1 1 10 0
    26 10 0 0 10 0
