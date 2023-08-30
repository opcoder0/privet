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

from pathlib import Path

from privet.search import native
from privet.search import nlp
from privet.search import classify

from privet.filetype import text
from privet.filetype import pdf


def native_search(path_args, extn):
    t = native.Native()
    file_paths = path_args.split(",")
    t.search(file_paths, extn)


def nlp_search(path_args, extn, context, verbose):
    pipeline = nlp.Nlp()
    classifier = classify.Classify(pipeline)
    file_paths = path_args.split(",")
    results = classifier.search(file_paths, extn, context, verbose)
    classifier.analyze(results, context)
    if verbose:
        print(json.dumps(results, sort_keys=True, indent=4))


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
            pipeline = nlp.Nlp()
            doc = pipeline.nlp(content)
            pipeline.visualize(doc)
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
        description=
        "Search for confidential data in files. Requires atleast one file type to run"
    )
    parser.add_argument('-t',
                        '--text',
                        action='store_true',
                        help='search text files')
    parser.add_argument('-p',
                        '--pdf',
                        action='store_true',
                        help='search PDF files')
    parser.add_argument('-d',
                        '--dir',
                        type=str,
                        metavar='/path1,/path2,...',
                        action='store',
                        help='search path to find files')
    parser.add_argument(
        '-s',
        '--searchtype',
        type=str,
        action='store',
        help='search technique; supported values one of: "nlp" or "filter"')

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
    if not args.dir and not args.visualize:
        print()
        print('Missing mandatory argument: directory path to search files\n')
        parser.print_help()
        exit(1)
    if not args.searchtype and not args.visualize:
        print()
        print(
            'Missing mandatory argument: method to use for searching files\n')
        parser.print_help()
        exit(1)

    if not args.visualize and args.searchtype.strip(
    ) != 'nlp' and args.searchtype.strip() != 'filter':
        print()
        print('Invalid value for searchtype\n')
        parser.print_help()
        exit(1)

    if not args.visualize and args.text is False and args.pdf is False:
        print()
        print('Must specify atleast one file type to search\n')
        parser.print_help()
        exit(1)

    if not args.visualize and args.searchtype.strip() == 'nlp' and (
            args.namespace is None or args.namespace.strip() == ''):
        print()
        print('Must specify search namespace. Supported values: [Australia]')
        print()
        parser.print_help()
        exit(1)

    if not args.visualize and args.searchtype.strip() == 'nlp':
        if args.text:
            nlp_search(args.dir, 'txt', args.namespace.strip(), args.verbose)
        else:
            nlp_search(args.dir, 'pdf', args.namespace.strip(), args.verbose)
    elif not args.visualize and args.searchtype.strip() == 'filter':
        if args.text:
            native_search(args.dir, 'txt')
        else:
            native_search(args.dir, 'pdf')
    elif args.visualize:
        visualize_doc(args.visualize)
