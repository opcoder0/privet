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

import glob
import mmap
import os
import pathlib
import re


class Pathfinder:

    def __init__(self):
        pass

    # returns
    #  nresults: number of occurances of the string matching the regexp
    #  results: a list of results indicating filename and position in the file
    def find(self, regexp, filepaths, file_extension, recurse):
        nresults = 0
        results = []
        rex = re.compile(regexp)
        for filepath in filepaths:
            search_path = pathlib.Path(filepath)
            if recurse is True:
                search_path = search_path.joinpath('**')
            else:
                search_path = search_path.joinpath('*')
            extn = '*.{ext}'.format(ext=file_extension)
            search_path = search_path.joinpath(extn)
            for filename in glob.iglob(search_path.as_posix(),
                                       recursive=recurse):
                with open(filename, 'r+b') as file:
                    mm = mmap.mmap(file.fileno(), 0)
                    done = False
                    line_count = 0
                    while not done:
                        line = mm.readline()
                        if len(line) == 0:
                            done = True
                        else:
                            line_count += 1
                            # TODO handle more than one occurance/match on
                            # the same line
                            match = rex.search(str(line))
                            if match is not None:
                                begin, end = match.span()
                                nresults += 1
                                result = {
                                    'filename': filename,
                                    'match': match.group(),
                                    'page': 0,
                                    'line': line_count,
                                    'begin': begin,
                                    'end': end
                                }
                                results.append(result)
                    mm.close()
        return nresults, results
