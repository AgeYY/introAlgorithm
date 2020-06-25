#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

mapTable = {'A': 0, 'T': 1, 'C': 2, 'G': 3}

class krHash():
    # Karp-Rabin algorithm. Division method for hash value.
    def __init__(self, p = 2, base = 4):
        # the base can only be 16, 10, 8, 2. Please indicate the base with its original format, i.e. base = 0b10, 0o10, 0x10 or 10.
        self.p = p # prime number
        self.base = base # the base should be same with the alphabet size
        self.nDigit = 0 # number of alphabet currently being stored
        self.hashV = 0 # hash value
    def setP(self, p):
        self.p = p
    def setBase(self, base):
        self.base = base
    def append(self, c):
        # append new letter c which is converted to a number already
        self.hashV = (self.hashV * self.base + c) % self.p
        self.nDigit = self.nDigit + 1
    def skip(self, c):
        self.hashV = ( (self.hashV % self.p) - c * (pow(self.base, self.nDigit - 1) % self.p)) % self.p

class krHashDNA(krHash):
    def append(self, c):
        try:
            num = mapTable[c]
        except KeyError:
            print('Please input the char with A, T, C, or G')
        super().append(num)

    def skip(self, c):
        try:
            num = mapTable[c]
        except KeyError:
            print('Please input the char with A, T, C, or G')
        super().skip(num)

def nearPrime(n):
    # find the largest prime no larger than n
    primes = [2]
    if n < 2:
        return 2
    else:
        for i in range(3, n+1, 2):
            sign = 0 # assume number i is a prime
            for j in primes:
                if i % j == 0:
                    sign = 1 # not a prime
                    break
            if sign == 0:
                primes.append(i)
    return primes[-1]

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.pairs = {}
    # Associates the value v with the key k.
    def put(self, k, v):
        try:
            self.pairs[k].append(v)
        except KeyError:
            self.pairs[k] = [v]
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        try:
            return self.pairs[k]
        except KeyError:
            return []

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    r = krHashDNA(p = nearPrime(k), base = 4)
    for i in range(k):
        r.append(seq[i])
    yield seq[:i + 1], r.hashV
    for i in range(k, len(seq)):
        r.append(seq[i])
        r.skip(seq[i - 3])
        yield seq[i-2:i + 1], r.hashV

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    raise Exception("Not implemented!")

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    raise Exception("Not implemented!")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0]))
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
