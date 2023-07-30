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
from lib import text


def text_search(file_paths):
    t = text.Text()
    t.search(file_paths)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: {} [paths]\n".format(sys.argv[0]))
        sys.exit(1)

    text_search(sys.argv[1:])
