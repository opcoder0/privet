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
import sys
from privet.search import libag
from privet.search import native


def native_search(path_args):
    t = native.Native()
    file_paths = path_args.split(",")
    t.search(file_paths)


def text_search(path_args):
    t = libag.Text()
    file_paths = path_args.split(",")
    t.search(file_paths)


if __name__ == '__main__':

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
        native_search(args.text)
    elif args.pdf:
        print("pdf search: not supported yet!")
    else:
        parser.print_help()
