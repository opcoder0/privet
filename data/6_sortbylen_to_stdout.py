#!/usr/bin/env python
import sys

fname = sys.argv[1]
if fname is None or fname == '':
    print('Missing filename to sort')
    sys.exit(1)

f = open(fname, 'r')
l = f.readlines()
l2 = sorted(l, key=len)
f2 = sys.stdout
for line in l2:
    f2.write(line)

f.close()
