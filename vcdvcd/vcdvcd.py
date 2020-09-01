from __future__ import print_function

import math
import re

class VCDVCD(object):

    # Verilog standard terminology.
    _VALUE = set(('0', '1', 'x', 'X', 'z', 'Z'))
    _VECTOR_VALUE_CHANGE = set(('b', 'B', 'r', 'R'))

    def __init__(
        self,
        vcd_path,
        only_sigs=False,
        print_dumps=False,
        print_dumps_deltas=True,
        signals=None,
        store_tvs=True,
        callbacks=None,
    ):
        """
        Parse a VCD file, and store information about it in this object.

        The bulk of the parsed data can be obtained with :func:`parse_data`.

        :type data: Dict[str,Any]
        :ivar data: Parsed VCD data presented in an per-signal indexed list of deltas.

                    Binary search in this data presentation makes it possible
                    to efficienty find the value of a given signal. TODO implement helper.

        :type deltas: Dict[str,Any]
        :ivar deltas: Parsed VCD data presented in exactly the same format as the input,
                    with all signals mixed up, but sorted in time.

        :ivar endtime: Last timestamp present in the last parsed VCD.

                       This can be extracted from the data, but we also cache while parsing.
        :type endtime: int

        :ivar references_to_ids: map of long-form human readable signal names to the short
                       style VCD dump values
        :type references_to_ids: Dict[str,str]

        :ivar signals: The set of unique signal names from the parsed VCD,
                       in the order they are defined in the file.

                        This can be extracted from the data, but we also cache while parsing.
        :type signals: List[str]

        :ivar timescale: A dictionary of key/value pairs describing the timescale.

                        List of keys:

                        - "timescale": timescale in seconds (SI unit)
                        - "number": time number as specified in the VCD file
                        - "unit": time unit as specified in the VCD file
                        - "factor": numerical factor derived from the unit
        :type timescale: Dict

        :type vcd_path: str
        :param vcd_path: path to the VCD file to parse

        :param store_tv: if False, don't store time values in the data
                         Still parse them sequentially however, which may
                         make them be printed if printing is enabled.
                         This makes huge files more manageable, but prevents
                         fast random access.

        :type  store_tv: bool

        :param only_sigs: only parse the signal names under $scope and exit.
                        The return value will only contain the signals section.
                        This speeds up parsing if you only want the list of signals.
        :type  only_sigs: bool

        :param print_dumps: print the values of all signals as they are parsed
        :type print_dumps: bool

        :param print_dumps_deltas: controls how print_dumps prints exactly:
                        - if True, print only if a value in signals since the previous time
                          If not values changed, don't print anything.
                        - if False, print all values at all times
        :type print_dumps_deltas: bool

        :param signals: only consider signals in this list.
                        If empty, all signals are considered.
                        Printing commands however will only print every wire
                        once with the first reference name found.
                        Any printing done uses this signal order.
                        If repeated signals are given, they are printed twice.
        :type  signals: List[str]

        :param callbacks: callbacks that get called as the VCD file is parsed
        :type callbacks: StreamParserCallbacks
        """
        self.data = {}
        self.endtime = 0
        self.references_to_ids = {}
        self.signals = []
        self.timescale = {}

        self._store_tvs = store_tvs
        self._signal_changed = False

        if signals is None:
            signals = []
        if callbacks is None:
            callbacks = StreamParserCallbacks()
        all_sigs = not signals
        cur_sig_vals = {}
        hier = []
        num_sigs = 0
        references_to_widths = {}
        time = 0
        with open(vcd_path, 'r') as f:
            while True:
                line = f.readline()
                if line == '':
                    break
                line0 = line[0]
                line = line.strip()
                if line == '':
                    continue
                if line0 in self._VECTOR_VALUE_CHANGE:
                    value, identifier_code = line[1:].split()
                    self._add_value_identifier_code(
                        time, value, identifier_code, print_dumps, cur_sig_vals,
                        callbacks
                    )
                elif line0 in self._VALUE:
                    value = line0
                    identifier_code = line[1:]
                    self._add_value_identifier_code(
                        time, value, identifier_code, print_dumps, cur_sig_vals,
                        callbacks
                    )
                elif line0 == '#':
                    if print_dumps and (not print_dumps_deltas or self._signal_changed):
                        ss = []
                        ss.append('{}'.format(time))
                        for i, ref in enumerate(print_dumps_refs):
                            identifier_code = self.references_to_ids[ref]
                            value = cur_sig_vals[identifier_code]
                            ss.append('{0:>{1}s}'.format(binary_string_to_hex(value), references_to_widths[ref]))
                        print(' '.join(ss))
                    time = int(line[1:])
                    self.endtime = time
                    self._signal_changed = False
                elif '$enddefinitions' in line:
                    if only_sigs:
                        break
                    if print_dumps:
                        print('0 time')
                        if signals:
                            print_dumps_refs = signals
                        else:
                            print_dumps_refs = sorted(self.data[i]['references'][0] for i in cur_sig_vals.keys())
                        for i, ref in enumerate(print_dumps_refs, 1):
                            print('{} {}'.format(i, ref))
                            if i == 0:
                                i = 1
                            identifier_code = self.references_to_ids[ref]
                            size = int(self.data[identifier_code]['size'])
                            width = max(((size // 4)), int(math.floor(math.log10(i))) + 1)
                            references_to_widths[ref] = width
                        print()
                        print('0 '.format(i, ), end='')
                        for i, ref in enumerate(print_dumps_refs, 1):
                            print('{0:>{1}d} '.format(i, references_to_widths[ref]), end='')
                        print()
                        print('=' * (sum(references_to_widths.values()) + len(references_to_widths) + 1))
                    callbacks.enddefinitions(self)
                elif '$scope' in line:
                    hier.append(line.split()[2])
                elif '$upscope' in line:
                    hier.pop()
                elif '$var' in line:
                    ls = line.split()
                    type = ls[1]
                    size = ls[2]
                    identifier_code = ls[3]
                    name = ''.join(ls[4:-1])
                    path = '.'.join(hier)
                    reference = path + '.' + name
                    if (reference in signals) or all_sigs:
                        self.signals.append(reference)
                        if identifier_code not in self.data:
                            self.data[identifier_code] = {
                                'references': [],
                                'size': size,
                                'var_type': type,
                            }
                        self.data[identifier_code]['references'].append(reference)
                        self.references_to_ids[reference] = identifier_code
                        if print_dumps:
                            cur_sig_vals[identifier_code] = 'x'
                elif '$timescale' in line:
                    if not '$end' in line:
                        while True:
                            line += " " + f.readline().strip().rstrip()
                            if '$end'  in line:
                                break
                    timescale = ' '.join(line.split()[1:-1])
                    number    = re.findall(r"\d+|$", timescale)[0]
                    unit      = re.findall(r"s|ms|us|ns|ps|fs|$", timescale)[0]
                    factor = {
                        "s":  1e0,
                        "ms": 1e-3,
                        "us": 1e-6,
                        "ns": 1e-9,
                        "ps": 1e-12,
                        "fs": 1e-15,
                    }[unit]
                    self.timescale["timescale"] = int(number) * factor
                    self.timescale["number"] = int(number)
                    self.timescale["unit"]   = unit
                    self.timescale["factor"] = factor

    def _add_value_identifier_code(
        self, time, value, identifier_code,
        print_dumps, cur_sig_vals, callbacks
    ):
        if identifier_code in self.data:
            callbacks.value(
                self,
                time=time,
                value=value,
                identifier_code=identifier_code,
                cur_sig_vals=cur_sig_vals
            )
            entry = self.data[identifier_code]
            self._signal_changed = True
            if self._store_tvs:
                if 'tv' not in entry:
                    entry['tv'] = []
                entry['tv'].append((time, value))
            if print_dumps:
                cur_sig_vals[identifier_code] = value

    def __getitem__(self, refname):
        """
        :type refname: str
        :param refname: human readable name of a signal (reference)

        :return: the signal for the given reference
        """
        return self.data[self.references_to_ids[refname]]


    def get_data(self):
        """
        Deprecated, use the member variable directly.
        """
        return self.data

    def get_endtime(self):
        """
        Deprecated, use the member variable directly.
        """
        return self.endtime

    def get_signals(self):
        """
        Deprecated, use the member variable directly.
        """
        return self.signals

    def get_timescale(self):
        """
        Deprecated, use the member variable directly.
        """
        return self.timescale

class StreamParserCallbacks(object):
    def value(
        self,
        vcd,
        time,
        value,
        identifier_code,
        cur_sig_vals,
    ):
        pass

    def enddefinitions(
        self,
        vcd,
    ):
        pass

class PrintDeltasStreamParserCallbacks(StreamParserCallbacks):
    """
    https://github.com/cirosantilli/vcdvcd#vcdcat-deltas
    """
    def value(
        self,
        vcd,
        time,
        value,
        identifier_code,
        cur_sig_vals,
    ):
        print('{} {} {}'.format(
            time,
            binary_string_to_hex(value),
            vcd.data[identifier_code]['references'][0])
        )

def binary_string_to_hex(s):
    """
    Convert a binary string to hexadecimal.

    If any non 0/1 values are present such as 'x', return that single character
    as a representation.

    :param s: the string to be converted
    :type s: str
    """
    for c in s:
        if not c in '01':
            return c
    return hex(int(s, 2))[2:]
