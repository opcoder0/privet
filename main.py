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
import sys
import shutil


def native_search(path_args, extn):
    t = native.Native()
    file_paths = path_args.split(",")
    t.search(file_paths, extn)


def text_search(path_args):
    t = libag.Text()
    file_paths = path_args.split(",")
    t.search(file_paths)


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
                        metavar='/path1,/path2,...',
                        type=str,
                        action='store',
                        help="search text files")
    parser.add_argument("-p",
                        "--pdf",
                        type=str,
                        metavar='/path1,/path2,...',
                        action='store',
                        help="search PDF files")
    args = parser.parse_args()
    if args.text:
        print("text path: {}".format(args.text))
        native_search(args.text, 'txt')
    elif args.pdf:
        print("text path: {}".format(args.pdf))
        native_search(args.pdf, 'pdf')
    else:
        parser.print_help()
