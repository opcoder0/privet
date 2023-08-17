#!/usr/bin/env python

import os
import re
import sys
import argparse
from enum import Enum


def get_regex_pattern(string):

    pattern = ''
    # token type 0 for alpha, 1 for digit, 2 for unknown
    TokenType = Enum('TokenType', ['ALPHA', 'DIGIT', 'UNKNOWN'])
    ttype = TokenType.UNKNOWN
    alpha_count = 0
    digit_count = 0
    temp = ''
    for s in string:
        if s.isalpha():
            digit_count = 0
            if ttype != TokenType.ALPHA and ttype != TokenType.DIGIT:
                ttype = TokenType.ALPHA
                alpha_count += 1
                if alpha_count > 1:
                    temp = '[A-Za-z]{%d}' % alpha_count
                else:
                    temp = '[A-Za-z]'
            elif ttype == TokenType.ALPHA:
                alpha_count += 1
                temp = '[A-Za-z]{%d}' % alpha_count
            elif ttype == TokenType.DIGIT:
                pattern += temp
                temp = r'[A-Za-z]'
                alpha_count = 1
                ttype = TokenType.ALPHA
        elif s.isdigit():
            alpha_count = 0
            if ttype != TokenType.ALPHA and ttype != TokenType.DIGIT:
                ttype = TokenType.DIGIT
                digit_count += 1
                if digit_count > 1:
                    temp = '\d{%d}' % digit_count
                else:
                    temp = r'\d'
            elif ttype == TokenType.DIGIT:
                digit_count += 1
                temp = '\d{%d}' % digit_count
            elif ttype == TokenType.ALPHA:
                pattern += temp
                digit_count = 1
                temp = r'\d'
                ttype = TokenType.DIGIT
        else:
            print('unknown character')
            break
    pattern += temp
    return pattern


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=
        "Generate basic non-smart regex for possible passport (number-digit) combo"
    )
    parser.add_argument("-s",
                        "--string",
                        metavar='0124AB395P',
                        type=str,
                        action='store',
                        help="input string")
    parser.add_argument("-f",
                        "--file",
                        type=str,
                        metavar='/path/to/file/with/a_string_per_line',
                        action='store',
                        help="input file")

    args = parser.parse_args()
    if (args.string is None or args.string == '') and (args.file is None
                                                       or args.file == ''):
        parser.print_help()
        sys.exit(1)

    if args.string is not None and args.string != '':
        # print(args.string, ':', get_regex_pattern(args.string))
        print(get_regex_pattern(args.string))
        sys.exit(0)

    if args.file != '':
        if not os.path.isfile(args.file):
            print('Input file not found')
            sys.exit(1)
        with open(args.file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                # print(line.rstrip(), ':', get_regex_pattern(line.rstrip()))
                print(get_regex_pattern(line.rstrip()))
