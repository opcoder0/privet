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

import codecs
import sys


def is_text(file_path):
    try:
        with codecs.open(file_path, encoding='utf-8', errors='strict') as f:
            pass
        return True
    except IOError as e:
        sys.stderr.write("%s contains invalid UTF-8\n" % file_path)
    finally:
        return False


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
