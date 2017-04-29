from __future__ import print_function

import re

class VCDParseError(Exception):
    pass

class VerilogVCD(object):

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
        timescale='',
    ):
        """
        Parse a VCD file, and store information about it in this object.

        The bulk of the parsed data can be obtained with :func:`parse_data`.

        :type vcd_path: str
        :param only_sigs: only parse the signal names under $scope and exit.
                        The return value will only contain the signals section.
                        This speeds up parsing if you only want the list of signals.
        :type  only_sigs: bool
        :type print_deltas: print the value of each signal change as hey are parsed
        :type print_deltas: bool
        :type print_dumps: print the value of all signals for each time
                           in which any tracked signal changes
        :type print_dumps: bool
        :param signals: only consider signals in this set
        :type  signals: Iterable[str]
        :rtype: Dict[str,Any]
        """
        self._data = {}
        self._endtime = 0
        self._signals = set()
        self._timescale = ''

        signals = set(signals)
        all_sigs = not signals
        cur_sig_vals = {}
        hier = []
        mult = 0
        num_sigs = 0
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
                    time = mult * int(line[1:])
                    self._endtime = time
                    if print_dumps:
                        print(str(time) + ' ' + ' '.join(cur_sig_vals.values()))
                elif '$enddefinitions' in line:
                    if only_sigs:
                        break
                    if print_dumps:
                        print('\n'.join(self._data[i]['nets'][0]['name'] for i in cur_sig_vals.keys()) + '\n')
                elif '$timescale' in line:
                    statement = line
                    if not '$end' in line:
                        while f:
                            line = f.readline()
                            statement += line
                            if '$end' in line:
                                break
                    mult = self._calc_multiplier(statement, timescale)
                elif '$scope' in line:
                    hier.append(line.split()[2])
                elif '$upscope' in line:
                    hier.pop()
                elif '$var' in line:
                    ls = line.split()
                    type = ls[1]
                    size = ls[2]
                    identifier_code = ls[3]
                    name = "".join(ls[4:-1])
                    path = '.'.join(hier)
                    full_name = path + '.' + name
                    if (full_name in signals) or all_sigs:
                        self._signals.add(full_name)
                        if identifier_code not in self._data:
                            self._data[identifier_code] = {}
                        if 'nets' not in self._data[identifier_code]:
                            self._data[identifier_code]['nets'] = []
                        var_struct = {
                            'name': full_name,
                            'size': size,
                            'type': type,
                        }
                        self._data[identifier_code]['nets'].append(var_struct)
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
        Get the set of unique signal names from the parsed VCD.

        This can be extracted from the data, but we also cache while parsing.

        :rtype: Set[str]
        """
        return self._signals

    def get_timescale(self):
        """
        :rtype: str
        """
        return self._timescale

    def _add_value_identifier_code(
        self, time, value, identifier_code,
        print_deltas, print_dumps, cur_sig_vals
    ):
        if identifier_code in self._data:
            entry = self._data[identifier_code]
            if 'tv' not in entry:
                entry['tv'] = []
            entry['tv'].append((time, value))
            if print_deltas:
                print("{} {} {}".format(time, value, entry['nets'][0]['name']))
            if print_dumps:
                cur_sig_vals[identifier_code] = value

    def _calc_multiplier(self, statement, timescale=''):
        """
        Input statement is complete timescale, for example:

            timescale 10ns end

        Input new_units is one of s|ms|us|ns|ps|fs.

        :rtype: float
        """
        fields = statement.split()
        fields.pop()
        fields.pop(0)
        tscale = ''.join(fields)
        new_units = ''
        if timescale:
            new_units = timescale.lower()
            new_units = re.sub(r'\s', '', new_units)
            self._timescale = '1' + new_units
        else:
            self._timescale = tscale
            return 1
        mult = 0
        units = 0
        ts_match = re.match(r'(\d+)([a-z]+)', tscale)
        if ts_match:
            mult  = int(ts_match.group(1))
            units = ts_match.group(2).lower()
        else:
            raise VCDParseError('unsupported timescale')
        mults = {
            'fs': 1e-15,
            'ps': 1e-12,
            'ns': 1e-09,
            'us': 1e-06,
            'ms': 1e-03,
            's': 1e-00,
        }
        mults_keys = mults.keys()
        mults_keys.sort(key=lambda x : mults[x])
        scale = 0
        if units in mults:
            scale = mults[units]
        else:
            raise VCDParseError('unsupported timescale units')
        new_scale = 0
        if new_units in mults:
            new_scale = mults[new_units]
        else:
            raise VCDParseError('illegal user-supplied timescale')
        return ((mult * scale) / new_scale)
