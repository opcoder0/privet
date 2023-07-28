#!/usr/bin/env python

# Copyright 2023 Sai Kiran Gummaraj <saikiran.gummaraj@gmail.com>
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

import sys

sys.path.append("./filetype/text/")
from libag import *


def is_binary_file(path_name):
    is_binary = false
    text_chars = bytearray(set(range(0x20, 0x100)) - {0x7f})
    try:
        with open(path_name, 'rb') as f:
            bytes = f.read(1024)
            v = bytes.translate(None, text_chars)
            if v is None or v == b'':
                is_binary = false
            else:
                is_binary = true
    except OSError as e:
        print(e)
    return is_binary


if len(sys.argv) < 3:
    sys.stderr.write("Usage: {} \"regex\" [paths]\n".format(sys.argv[0]))
    sys.exit(1)

# Initiate Ag library with default options.
ag_init()

# Search.
nresults, results = ag_search(sys.argv[1], sys.argv[2:])

if nresults == 0:
    print("no result found")
else:
    print("{} results found".format(nresults))

    # Show them on the screen, if any.
    for file in results:
        for match in file.matches:
            print("file: {}, match: {}, start: {} / end: {}".format(
                file.file, match.match, match.byte_start, match.byte_end))

# Free all resources.
if nresults:
    ag_free_all_results(results)

# Release Ag resources.
ag_finish()
