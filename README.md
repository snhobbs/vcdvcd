# Verilog VCD

Verilog VCD value change dump parser.

The format is defined by the Verilog standard, and can be generated with `$dumpvars`.

The entire VCD is parsed at once. For a stream implementation, see: <https://github.com/GordonMcGregor/vcd_parser>

Forked from Sameer Gauria's version, which is currently only hosted on PyPI with email patches and no public bug tracking: <https://pypi.python.org/pypi/Verilog_VCD>. There is also a read-only mirror at: <https://github.com/zylin/Verilog_VCD>

Example:

    python examples.py

Install:

    sudo python setup.py install
