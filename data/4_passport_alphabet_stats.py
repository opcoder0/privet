#!/usr/bin/env python

import os
import sys
import re


def printlist(l):
    for line in l:
        print(line.strip())


def main():
    if (len(sys.argv) == 1):
        print('required filename is missing')
        sys.exit(1)

    filename = sys.argv[1]
    f = open(filename, 'r')
    passports = f.readlines()

    # find passports that start with one or more alphabet
    for i in range(1, 15):
        print(">> processing starting with %d alpha ---" % i)
        fname = 'generated.passport.sortedbylen.startwith.%d.alpha.txt' % i
        fh = open(fname, 'w')
        regexp = r'^[a-zA-Z]{%d}\d+'
        match_passport_with_regexp_n(i, passports, regexp, fh)
        fh.close()
        # if the file had no content delete it; remove unwanted files
        fstat = os.stat(fname)
        if fstat.st_size == 0:
            os.remove(fname)

    # find passports that have one or more alphabets
    # in the middle
    for i in range(1, 15):
        print(">> processing %d alpha in middle ---" % i)
        fname = 'generated.passport.sortedbylen.%d.alpha.in.middle.txt' % i
        fh = open(fname, 'w')
        regexp = r'^\d+[a-zA-Z]{%d}\d+'
        match_passport_with_regexp_n(i, passports, regexp, fh)
        fh.close()
        # if the file had no content delete it; remove unwanted files
        fstat = os.stat(fname)
        if fstat.st_size == 0:
            os.remove(fname)

    # find passports that has letters but start with a number
    # and has letters and numbers in between and ends with number
    regexp = r'^\d+[a-zA-Z]{}\d{}[a-zA-Z]{}\d+'
    fname = 'generated.passport.sortedbylen.num.alpha.num.alpha.num.txt'
    fh = open(fname, 'w')
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                match_passport_with_regexp_var(i, j, k, passports, regexp, fh)
    fh.close()
    f.close()


def match_passport_with_regexp_n(n, passports, regexp, fh=sys.stdout):
    regexp = regexp % n
    rex = re.compile(regexp)
    result = []
    for pp in passports:
        if rex.match(pp) is not None:
            if fh == sys.stdout:
                result.append(pp)
            else:
                fh.write(pp)
    if fh == sys.stdout:
        printlist(result)


def match_passport_with_regexp_var(i, j, k, passports, regexp, fh=sys.stdout):
    regexp = regexp.format(i, j, k)
    rex = re.compile(regexp)
    result = []
    for pp in passports:
        if rex.match(pp) is not None:
            if fh == sys.stdout:
                result.append(pp)
            else:
                fh.write(pp)
    if fh == sys.stdout:
        printlist(result)


# def passports_with_n_letters_in_the_middle(n, passports, fh=sys.stdout):
#     # find passports that have only one alphabet
#     # and it is at the beginning
#     regexp = r'^\d+[a-zA-Z]{%d}\d+' % n
#     rex = re.compile(regexp)
#     startwith_n_alpha = []
#     for pp in passports:
#         if rex.match(pp) is not None:
#             if fh == sys.stdout:
#                 startwith_n_alpha.append(pp)
#             else:
#                 fh.write(pp)
#     if fh == sys.stdout:
#         printlist(startwith_n_alpha)
#

if __name__ == '__main__':
    main()
