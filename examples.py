#!/usr/bin/env python

from __future__ import print_function

import sys
from pprint import PrettyPrinter

from verilog_vcd import VerilogVCD

if (len(sys.argv) > 1):
    vcd_path = sys.argv[1]
else:
    vcd_path = 'counter_tb.vcd'
pp = PrettyPrinter()

print('# get_data()')
vcd = VerilogVCD(vcd_path)
pp.pprint(vcd.get_data())
print()

print('# get_data(only_sigs=True)')
vcd = VerilogVCD(vcd_path, only_sigs=True)
PrettyPrinter().pprint(vcd.get_data())
print()

print('# get_signals()')
vcd = VerilogVCD(vcd_path, only_sigs=True)
pp.pprint(vcd.get_signals())
print()

print('# __init__(signals=)')
vcd_only_sigs = VerilogVCD(vcd_path, only_sigs=True)
signals = sorted(vcd_only_sigs.get_signals())
len_signals = len(signals)
if len_signals > 0:
    vcd_signal_0 = VerilogVCD(vcd_path, signals=[signals[0]])
    pp.pprint(vcd_signal_0.get_data())
    print()
if len_signals > 1:
    vcd_signal_1 = VerilogVCD(vcd_path, signals=[signals[1]])
    pp.pprint(vcd_signal_1.get_data())
print()

print('# __init__(print_deltas=True)')
VerilogVCD(vcd_path, print_deltas=True)
print()

print('# __init__(print_deltas=True, signals=)')
vcd_only_sigs = VerilogVCD(vcd_path, only_sigs=True)
signals = sorted(vcd_only_sigs.get_signals())
if signals:
    VerilogVCD(vcd_path, signals=[signals[0]], print_deltas=True)
print()

print('# __init__(print_dumps=True)')
VerilogVCD(vcd_path, print_dumps=True)
print()

print('# __init__(print_dumps=True, signals=)')
vcd_only_sigs = VerilogVCD(vcd_path, only_sigs=True)
signals = sorted(vcd_only_sigs.get_signals())
VerilogVCD(vcd_path, signals=signals[0:2], print_dumps=True)
print()
