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
    def find(self,
             regexp,
             filepaths,
             file_extension,
             recurse,
             keywords=None,
             window_size=0):
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
            save_prev = 0
            save_curr = 0
            curr_pos = 0
            nwords = 0
            look_around = False
            if keywords is not None and len(keywords) > 0 and window_size > 0:
                look_around = True
            for filename in glob.iglob(search_path.as_posix(),
                                       recursive=recurse):
                save_prev = 0
                save_curr = 0
                with open(filename, 'r+b') as file:
                    mm = mmap.mmap(file.fileno(), 0)
                    done = False
                    line_count = 0
                    while not done:
                        line = mm.readline()
                        if line == b'':
                            done = True
                        else:
                            line = str(line)
                            line_count += 1
                            nwords += len(line.split(' '))
                            if nwords >= window_size:
                                save_prev = save_curr
                                save_curr = mm.tell()
                                nwords = 0
                            match = rex.search(line)
                            keyword_found = False
                            if match is not None:
                                begin, end = match.span()
                                if look_around is True:
                                    # look for keywords in the
                                    # 'window_size' window.
                                    save = mm.tell()
                                    # check if we have the number words in the window
                                    # if not use the previous saved window
                                    mm.seek(save_curr)
                                    data = str(mm.read(save - save_curr))
                                    if len(data.split(' ')) < window_size:
                                        mm.seek(save_prev)
                                        data = str(mm.read(save - save_prev))
                                    for keyword in keywords:
                                        if data.find(keyword):
                                            keyword_found = True
                                            break
                                nresults += 1
                                result = {
                                    'filename': filename,
                                    'match': match.group(),
                                    'page': 0,
                                    'line': line_count,
                                    'begin': begin - 2,
                                    'end': end - 2,
                                    'keyword_found': keyword_found
                                }
                                results.append(result)
                    mm.close()
        return nresults, results
