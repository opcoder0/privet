#!/usr/bin/env python

# print passports that have atleast one alphabet in it
# it can be anywhere in the passport (beginning/middle/end)

import re

regexp = r'[a-zA-Z]'
rex = re.compile(regexp)

f = open('./generated.passport.sortedbylen.txt', 'r')
l = f.readlines()

f1 = open('./generated.passport.sortedbylen.withalpa.txt', 'w')

for line in l:
    if rex.search(line) is not None:
        f1.write(line)

f.close()
f1.close()
