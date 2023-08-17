#!/usr/bin/env python

f = open('passport.txt', 'r')
l = f.readlines()
l2 = sorted(l, key=len)
f2 = open('generated.passport.sortedbylen.txt', 'w')
for line in l2:
    f2.write(line)

f2.close()
