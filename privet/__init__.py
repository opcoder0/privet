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

import pathlib
import os


def init():
    if len(wordset) > 0:
        return
    home_dir = pathlib.Path.home()
    privet_words_file = os.path.join(home_dir, '.privet', 'words.txt')
    with open(privet_words_file, 'r') as fp:
        for line in fp:
            wordset.add(line.lower())
    print('Wordlist load complete...')


# load word list
wordset = set()
init()
