#!/usr/bin/env python2

def reverse(seq):
    return seq[::-1]

def complement(seq):
    from string import maketrans
    complements = maketrans('ACTGactg', 'TGACtgac')
    return seq.translate(complements)

def reverse_complement(seq):
    return reverse(complement(seq))

def gc_content(seq):
    # This function contains a bug.  Do you see it?
    return sum(x in 'GC' for x in seq) / len(seq)

