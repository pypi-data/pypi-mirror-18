#!/usr/bin/env python2

"""\
Perform various simple manipulations on DNA sequences.

Usage:
    dna len <seq>
    dna rc <seq>
    dna gc <seq>

Commands:
    len: Print the length of the given DNA sequence.
    rc:  Print the reverse-complement of the given DNA sequence.
    gc:  Print the GC content of the given DNA sequence.

Arguments:
    <seq>: The DNA sequence to work with.
"""

from . import dna

def main():
    import docopt
    args = docopt.docopt(__doc__)
    seq = args['<seq>']

    if args['len']:
        print len(seq)
    if args['rc']:
        print dna.reverse_complement(seq)
    if args['gc']:
        print '{.2f}\%'.format(dna.gc_content(seq) / 100)

