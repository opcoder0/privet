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
import glob
import logging

import magic


class Pathfinder:
    '''
    Pathfinder returns a list of filenames under a list of
    path names.
    '''

    # return a list of filenames under the given pathnames
    # for the given extension
    def findfiles(self, filepaths, file_extension, recurse):
        '''
        findfiles returns list of files under filepaths with extension (in
        file_extension). The function finds files at top level or recursively
        based on recurse argument.
        '''

        result = []
        for filepath in filepaths:
            search_path = pathlib.Path(filepath)
            if recurse is True:
                search_path = search_path.joinpath('**')
            else:
                search_path = search_path.joinpath('*')
            extn = f'*.{file_extension}'
            search_path = search_path.joinpath(extn)
            mime_idx = 0
            mime_ext = ''
            if file_extension == 'txt':
                mime_idx = 0
                mime_ext = 'text'
            elif file_extension == 'pdf':
                mime_idx = 1
                mime_ext = 'pdf'
            else:
                raise Exception('Unsupported file extension')

            for filename in glob.iglob(search_path.as_posix(),
                                       recursive=recurse):
                try:
                    mime = magic.from_file(filename, mime=True)
                    if mime.split('/')[mime_idx] != mime_ext:
                        logging.warning(
                            'Unrecognized file format {}. Skipping'.format(
                                filename))
                        continue
                except Exception as e:
                    logging.warning(
                        'exception while checking mime for {}. Skipping'.
                        format(filename))
                    continue
                result.append(filename)
        return result
