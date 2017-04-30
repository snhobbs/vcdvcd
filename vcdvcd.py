from __future__ import print_function

import re

class VCDVCD(object):

    # Verilog standard terminology.
    _VALUE = set(('0', '1', 'x', 'X', 'z', 'Z'))
    _VECTOR_VALUE_CHANGE = set(('b', 'B', 'r', 'R'))

    def __init__(
        self,
        vcd_path,
        only_sigs=False,
        print_deltas=False,
        print_dumps=False,
        signals=[],
        store_tvs=True,
    ):
        """
        Parse a VCD file, and store information about it in this object.

        The bulk of the parsed data can be obtained with :func:`parse_data`.

        :type vcd_path: str
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
        :type print_deltas: print the value of each signal change as hey are parsed
        :type print_deltas: bool
        :type print_dumps: print the value of all signals for each time
                           in which any tracked signal changes
        :type print_dumps: bool
        :param signals: only consider signals in this list.
                        If not given, all signals are considered.
                        Any printing done uses this signal order.
                        If repeated signals are given, they are printed twice.
        :type  signals: List[str]
        :rtype: Dict[str,Any]
        """
        self._data = {}
        self._endtime = 0
        self._signals = []
        self._store_tvs = store_tvs

        all_sigs = not signals
        cur_sig_vals = {}
        hier = []
        num_sigs = 0
        references_to_ids = {}
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
                        time, value, identifier_code,
                        print_deltas, print_dumps, cur_sig_vals
                    )
                elif line0 in self._VALUE:
                    value = line0
                    identifier_code = line[1:]
                    self._add_value_identifier_code(
                        time, value, identifier_code,
                        print_deltas, print_dumps, cur_sig_vals
                    )
                elif line0 == '#':
                    time = int(line[1:])
                    self._endtime = time
                    if print_dumps:
                        ss = []
                        ss.append('{}'.format(time))
                        for ref in print_dumps_refs:
                            identifier_code = references_to_ids[ref]
                            value = cur_sig_vals[identifier_code]
                            size = int(self._data[identifier_code]['size'])
                            ss.append('{0:>{1}s}'.format(value, size))
                        print(' '.join(ss))
                elif '$enddefinitions' in line:
                    if only_sigs:
                        break
                    if print_dumps:
                        print('0 time')
                        if signals:
                            print_dumps_refs = signals
                        else:
                            print_dumps_refs = [self._data[i]['references'][0] for i in cur_sig_vals.keys()]
                        for i,s in enumerate(print_dumps_refs, 1):
                            print('{} {}'.format(i, s))
                        print()
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
                        self._signals.append(reference)
                        if identifier_code not in self._data:
                            self._data[identifier_code] = {
                                'references': [],
                                'size': size,
                                'var_type': type,
                            }
                        self._data[identifier_code]['references'].append(reference)
                        references_to_ids[reference] = identifier_code
                        if print_dumps:
                            cur_sig_vals[identifier_code] = 'x'

    def get_data(self):
        """
        Get the main parsed VCD data.
        """
        return self._data

    def get_endtime(self):
        """
        Last timestamp present in the last parsed VCD.

        This can be extracted from the data, but we also cache while parsing.

        :rtype: int
        """
        return self._endtime

    def get_signals(self):
        """
        Get the set of unique signal names from the parsed VCD,
        in the order they are defined in the file.

        This can be extracted from the data, but we also cache while parsing.

        :rtype: List[str]
        """
        return self._signals

    def _add_value_identifier_code(
        self, time, value, identifier_code,
        print_deltas, print_dumps, cur_sig_vals
    ):
        if identifier_code in self._data:
            entry = self._data[identifier_code]
            if self._store_tvs:
                if 'tv' not in entry:
                    entry['tv'] = []
                entry['tv'].append((time, value))
            if print_deltas:
                print("{} {} {}".format(time, value, entry['references'][0]))
            if print_dumps:
                cur_sig_vals[identifier_code] = value
