#!/usr/bin/env python
import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    #clean and split in words
    linechars = [c for c in line.lower() if c.isalpha() or c==' ']
    words     = ''.join(linechars).strip().split()

    #emit the key-balue pairs
    for word in words:
        print(word, "\t", 1)