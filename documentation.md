    from Verilog_VCD import parse_vcd
    vcd = parse_vcd('/path/to/some.vcd')

=head1 SUBROUTINES

=head2 parse_vcd(file, $opt_ref)

Parse a VCD file and return a reference to a data structure which
includes hierarchical signal definitions and time-value data for all
the specified signals.  A file name is required.  By default, all
signals in the VCD file are included, and times are in units
specified by the C<$timescale> VCD keyword.

    vcd = parse_vcd('/path/to/some.vcd')

It returns a reference to a nested data structure.  The top of the
structure is a Hash-of-Hashes.  The keys to the top hash are the VCD
identifier codes for each signal.  The following is an example
representation of a very simple VCD file.  It shows one signal named
C<chip.cpu.alu.clk>, whose VCD code is C<+>.  The time-value pairs
are stored as an Array-of-Tuples, referenced by the C<tv> key.  The
time is always the first number in the pair, and the times are stored in
increasing order in the array.

    {
      '+' : {
               'tv' : [
                         (
                           0,
                           '1'
                         ),
                         (
                           12,
                           '0'
                         ),
                       ],
               'nets' : [
                           {
                             'hier' : 'chip.cpu.alu.',
                             'name' : 'clk',
                             'type' : 'reg',
                             'size' : '1'
                           }
                         ]
             }
    }

Since each code could have multiple hierarchical signal names, the names are
stored as an Array-of-Hashes, referenced by the C<nets> key.  The example above
only shows one signal name for the code.


=head3 OPTIONS

Options to C<parse_vcd> should be passed as a hash reference.

=over 4

=item timescale

It is possible to scale all times in the VCD file to a desired timescale.
To specify a certain timescale, such as nanoseconds:

    vcd = parse_vcd(file, opt_timescale='ns'})

Valid timescales are:

    s ms us ns ps fs

=item siglist

If only a subset of the signals included in the VCD file are needed,
they can be specified by a signal list passed as an array reference.
The signals should be full hierarchical paths separated by the dot
character.  For example:

    signals = [
        'top.chip.clk',
        'top.chip.cpu.alu.status',
        'top.chip.cpu.alu.sum[15:0]',
    ]
    vcd = parse_vcd(file, siglist=signals)

Limiting the number of signals can substantially reduce memory usage of the
returned data structure because only the time-value data for the selected
signals is loaded into the data structure.

=item use_stdout

It is possible to print time-value pairs directly to STDOUT for a
single signal using the C<use_stdout> option.  If the VCD file has
more than one signal, the C<siglist> option must also be used, and there
must only be one signal specified.  For example:

    vcd = parse_vcd(file, 
                    use_stdout=1,
                    siglist=['top.clk']
                )

The time-value pairs are output as space-separated tokens, one per line.
For example:

    0 x
    15 0
    277 1
    500 0

Times are listed in the first column.
Times units can be controlled by the C<timescale> option.

=item only_sigs

Parse a VCD file and return a reference to a data structure which
includes only the hierarchical signal definitions.  Parsing stops once
all signals have been found.  Therefore, no time-value data are
included in the returned data structure.  This is useful for
analyzing signals and hierarchies.

    vcd = parse_vcd(file, only_sigs=1)

=back


=head2 list_sigs(file)

Parse a VCD file and return a list of all signals in the VCD file.
Parsing stops once all signals have been found.  This is
helpful for deciding how to limit what signals are parsed.

Here is an example:

    signals = list_sigs('input.vcd')

The signals are full hierarchical paths separated by the dot character

    top.chip.cpu.alu.status
    top.chip.cpu.alu.sum[15:0]

=head2 get_timescale( )

This returns a string corresponding to the timescale as specified
by the C<$timescale> VCD keyword.  It returns the timescale for
the last VCD file parsed.  If called before a file is parsed, it
returns an undefined value.  If the C<parse_vcd> C<timescale> option
was used to specify a timescale, the specified value will be returned
instead of what is in the VCD file.

    vcd = parse_vcd(file); # Parse a file first
    ts  = get_timescale();  # Then query the timescale

=head2 get_endtime( )

This returns the last time found in the VCD file, scaled
appropriately.  It returns the last time for the last VCD file parsed.
If called before a file is parsed, it returns an undefined value.

    vcd = parse_vcd(file); # Parse a file first
    et  = get_endtime();    # Then query the endtime

=head1 LIMITATIONS

Only the following VCD keywords are parsed:

    $end                $scope
    $enddefinitions     $upscope
    $timescale          $var

The extended VCD format (with strength information) is not supported.

The default mode of C<parse_vcd> is to load the entire VCD file into the
data structure.  This could be a problem for huge VCD files.  The best solution
to any memory problem is to plan ahead and keep VCD files as small as possible.
When simulating, dump fewer signals and scopes, and use shorter dumping
time ranges.  Another technique is to parse only a small list of signals
using the C<siglist> option; this method only loads the desired signals into
the data structure.  Finally, the C<use_stdout> option will parse the input VCD
file line-by-line, instead of loading it into the data structure, and directly
prints time-value data to STDOUT.  The drawback is that this only applies to
one signal.
