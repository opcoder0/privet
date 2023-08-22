#!/usr/bin/env python

# Copyright 2023 Sai Kiran Gummaraj <opcoder0@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from pathlib import Path
import os
from privet.search import libag
from privet.search import native
from privet.search import nlp
from privet.search import classify
import sys
import shutil


def native_search(path_args, extn):
    t = native.Native()
    file_paths = path_args.split(",")
    t.search(file_paths, extn)


def text_search(path_args, extn):
    t = libag.Text()
    file_paths = path_args.split(",")
    t.search(file_paths, extn)


def nlp_search(path_args, extn):
    pipeline = nlp.Nlp()
    classifier = classify.Classify(pipeline)
    file_paths = path_args.split(",")
    classifier.search(file_paths, extn)


def copy_words_file():
    home_dir = Path.home()
    privet_dir = os.path.join(home_dir, '.privet')
    mod_path = os.path.dirname(__file__)
    words_file = os.path.join(mod_path, 'words.txt')
    privet_words_file = os.path.join(home_dir, '.privet', 'words.txt')
    shutil.copyfile(words_file, privet_words_file)


def privet_init():
    home_dir = Path.home()
    privet_dir = os.path.join(home_dir, '.privet')
    is_dir = os.path.isdir(privet_dir)
    if is_dir:
        words_file = os.path.join(privet_dir, 'words.txt')
        if not os.path.exists(words_file):
            copy_words_file()
    else:
        os.mkdir(privet_dir)
        copy_words_file()


if __name__ == '__main__':

    privet_init()
    parser = argparse.ArgumentParser(
        description=
        "Search for confidential data in files. Requires atleast one file type to run"
    )
    parser.add_argument("-t",
                        "--text",
                        action='store_false',
                        help="search text files")
    parser.add_argument("-p",
                        "--pdf",
                        action='store_false',
                        help="search PDF files")
    parser.add_argument("-d",
                        "--dir",
                        type=str,
                        metavar='/path1,/path2,...',
                        action='store',
                        help="search path to find files")
    parser.add_argument(
        "-s",
        "--searchtype",
        type=str,
        action='store',
        help="search technique; supported values one of: 'nlp' or 'filter'")

    args = parser.parse_args()
    if not args.dir:
        print('Missing mandatory argument: directory path to search files\n')
        parser.print_help()
        exit(1)
    if not args.searchtype:
        print(
            'Missing mandatory argument: method to use for searching files\n')
        parser.print_help()
        exit(1)

    if args.searchtype.strip() != 'nlp' and args.searchtype.strip(
    ) != 'filter':
        print('Invalid value for searchtype\n')
        parser.print_help()
        exit(1)

    if args.text is False and args.pdf is False:
        print('Must specify atleast one file type to search\n')
        parser.print_help()
        exit(1)

    if args.searchtype.strip() == 'nlp':
        if args.text:
            nlp_search(args.dir, 'txt')
        else:
            nlp_search(args.dir, 'pdf')
    elif args.searchtype.strip() == 'filter':
        if args.text:
            native_search(args.dir, 'txt')
        else:
            native_search(args.dir, 'pdf')
