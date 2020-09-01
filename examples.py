#!/usr/bin/env python

from __future__ import print_function

import sys
from pprint import PrettyPrinter

import vcdvcd
from vcdvcd import VCDVCD

if (len(sys.argv) > 1):
    vcd_path = sys.argv[1]
else:
    vcd_path = 'counter_tb.vcd'
pp = PrettyPrinter()

print('# data')
vcd = VCDVCD(vcd_path)
pp.pprint(vcd.data)
print()

print('# references_to_ids()')
pp.pprint(vcd.references_to_ids)
print()

print('# timescale')
pp.pprint(vcd.timescale)
print()

print('# signals')
pp.pprint(vcd.signals)
print()

print('# __init__(only_sigs=True)')
vcd = VCDVCD(vcd_path, only_sigs=True)
PrettyPrinter().pprint(vcd.data)
print()

print('# __init__(signals=)')
vcd_only_sigs = VCDVCD(vcd_path, only_sigs=True)
signals = vcd_only_sigs.signals
len_signals = len(signals)
if len_signals > 0:
    print('## 0')
    vcd_signal_0 = VCDVCD(vcd_path, signals=signals[0:1])
    pp.pprint(vcd_signal_0.data)
    print()
    if len_signals > 1:
        print('## 1')
        vcd_signal_1 = VCDVCD(vcd_path, signals=signals[1:2])
        pp.pprint(vcd_signal_1.data)
        print()
        print('## 01')
        vcd_signal_01 = VCDVCD(vcd_path, signals=signals[0:2])
        pp.pprint(vcd_signal_01.data)
        print()
print()

print('# __init__(print_dumps=True)')
VCDVCD(vcd_path, print_dumps=True)
print()

print('# __init__(print_dumps=True, store_tvs=False)')
vcd = VCDVCD(vcd_path, print_dumps=True, store_tvs=False)
PrettyPrinter().pprint(vcd.data)
print()

print('# __init__(print_dumps=True, signals=)')
vcd_only_sigs = VCDVCD(vcd_path, only_sigs=True)
signals = sorted(vcd_only_sigs.signals)
VCDVCD(vcd_path, signals=signals[0:2], print_dumps=True, store_tvs=False)
print()
print('## reverse')
VCDVCD(vcd_path, signals=signals[1::-1], print_dumps=True, store_tvs=False)
print()
print('## repeat')
VCDVCD(vcd_path, signals=(signals[0:1] * 2), print_dumps=True, store_tvs=False)
print()

print('# __init__(print_deltas=True)')
VCDVCD(vcd_path, print_deltas=True, store_tvs=False)
print()

print('# __init__(print_deltas=True, signals=)')
vcd_only_sigs = VCDVCD(vcd_path, only_sigs=True)
signals = sorted(vcd_only_sigs.signals)
if signals:
    VCDVCD(vcd_path, signals=signals[0:1], print_deltas=True, store_tvs=False)
print()

print('# __init__(value_callback=True)')
class MyStreamParserCallbacks(vcdvcd.StreamParserCallbacks):
    def value(
        self,
        vcd,
        time,
        value,
        identifier_code,
        cur_sig_vals,
    ):
        print('{} {} {}'.format(time, value, identifier_code))
vcd = VCDVCD(vcd_path, stream_parser_callbacks=MyStreamParserCallbacks())
print()
