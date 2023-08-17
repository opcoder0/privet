#!/usr/bin/env python

#
# Run this only after running 4_*.py
#

files = [
    'generated.passport.sortedbylen.startwith.1.alpha.txt',
    'generated.passport.sortedbylen.startwith.2.alpha.txt',
    'generated.passport.sortedbylen.startwith.3.alpha.txt',
    'generated.passport.sortedbylen.startwith.4.alpha.txt',
    'generated.passport.sortedbylen.startwith.6.alpha.txt',
    'generated.passport.sortedbylen.1.alpha.in.middle.txt',
    'generated.passport.sortedbylen.2.alpha.in.middle.txt',
    'generated.passport.sortedbylen.3.alpha.in.middle.txt'
]

passports = set()
for f in files:
    fh = open(f, 'r')
    lines = fh.readlines()
    for line in lines:
        passports.add(line)
    fh.close()

print('passports with starting and middle alphabets = ', len(passports))

passports2 = set()
files2 = ['generated.passport.sortedbylen.withalpa.txt']
for f in files2:
    fh = open(f, 'r')
    lines = fh.readlines()
    for line in lines:
        if line not in passports:
            passports2.add(line)
    fh.close()

print('passports with alphabets in the middle or other cases = ',
      len(passports2))

print('--- difference ---')
others = passports2.difference(passports)
f = 'generated.passport.sortedbylen.other.txt'
fh = open(f, 'w')
for o in others:
    fh.write(o)
fh.close()
