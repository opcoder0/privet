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
import json
import os
import shutil
import sys

from pathlib import Path

from privet.search import nlpsearcher

from privet.filetype import text
from privet.filetype import pdf


def nlp_search(path_args, extn, context, verbose):
    nlp_searcher = nlpsearcher.NLPSearcher()
    results = nlp_searcher.search(path_args.split(","), extn, context, verbose)
    print(json.dumps(results, indent=4, sort_keys=True))


def copy_words_file():
    home_dir = Path.home()
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


def visualize_doc(filename):
    p = Path(filename)
    supported_extensions = ['.txt', '.pdf']
    if p.is_file():
        extn = p.suffix
        if extn in supported_extensions:
            content = None
            if extn == '.txt':
                txt_doc = text.Text(filename)
                content = txt_doc.content()
            if extn == '.pdf':
                pdf_doc = pdf.Pdf(filename)
                content = pdf_doc.content()
            nlp_searcher = nlpsearcher.NLPSearcher()
            nlp_searcher.visualize(content)
        else:
            print('Unsupported file format. Must be one of',
                  supported_extensions)
            return
    else:
        print(filename, ' must be a file of one of these types ',
              supported_extensions)
        return


if __name__ == '__main__':

    privet_init()
    parser = argparse.ArgumentParser(
        description="Search for confidential data in files")
    parser.add_argument('-f',
                        '--format',
                        action='store',
                        help='Specify file format [txt, pdf]')
    parser.add_argument('-d',
                        '--dir',
                        type=str,
                        metavar='/path1,/path2,...',
                        action='store',
                        help='search path to find files')
    parser.add_argument(
        '-n',
        '--namespace',
        type=str,
        action='store',
        help='search namespace can indicate region or search domain')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='verbose output')
    parser.add_argument('-z',
                        '--visualize',
                        metavar='/path/to/file',
                        action='store',
                        help='Visualize document entites')

    args = parser.parse_args()

    if args.visualize:
        visualize_doc(args.visualize)
    elif args.dir and args.format and args.namespace:
        if args.format not in ['txt', 'pdf']:
            print()
            print(
                'Invalid file format. Allowed values must be one of [txt, pdf]'
            )
            parser.print_help()
            sys.exit(1)
        nlp_search(args.dir, args.format, args.namespace, args.verbose)
    else:
        print()
        print('Missing mandatory argument: directory path to search files\n')
        parser.print_help()
        sys.exit(1)
