#!/usr/bin/env python

import sys

if (len(sys.argv) == 1):
    print('required filename is missing')
    sys.exit(1)

filename = sys.argv[1]
f = open(filename, 'r')
l = f.readlines()
s = set()
for line in l:
    s.add(len(line))
f.close()

print('found following lengths:')
print(sorted(s))
