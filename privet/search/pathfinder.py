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

from PyPDF2 import PdfReader

import glob
import logging
import magic
import mmap
import pathlib
import os
import re

import privet


class Pathfinder:

    def cleanup_words(self, lines):
        result = []
        clean_line = []
        backup = []
        for line in lines:
            backup = []
            words = line.split(' ')
            if len(words) <= 1:
                result.append(line)
                continue
            nwords = len(words)
            cword = ''
            clean_line = []
            for i in range(nwords):
                cword += words[i]
                is_word = (cword.lower() in privet.wordset)
                # longest word in english_words set with web2 and gcide is 45
                # characters long. In case there is no meaningful word found
                # despite reaching this length just merge them as-is.
                if (not is_word and len(''.join(backup)) <= 45):
                    backup.append(words[i])
                else:
                    if len(backup) > 0:
                        clean_line += backup
                        backup = []

                if (not cword.isalpha()):
                    if len(backup) > 0:
                        clean_line += backup
                    else:
                        clean_line.append(words[i])
                    cword = ''
                    backup = []
                    continue
                if is_word:
                    clean_line.append(cword)
                    cword = ''
                    backup = []
            if len(backup) > 0:
                clean_line += backup
            result.append(' '.join(clean_line))
        return result

    def num_words(self, lines):
        nwords = 0
        for line in lines:
            nwords += len(line.split(' '))
        return nwords

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
        if file_extension.lower() == 'txt':
            return self.txt(regexp, filepaths, file_extension, recurse,
                            keywords, window_size)
        elif file_extension.lower() == 'pdf':
            return self.pdf(regexp, filepaths, file_extension, recurse,
                            keywords, window_size)
        else:
            raise Exception('unsupported file extension')

    def txt(self,
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
                try:
                    mime = magic.from_file(filename, mime=True)
                    if mime.split('/')[0] != 'text':
                        logging.warning(
                            'Unrecognized file format {}. Skipping'.format(
                                filename))
                        continue
                except Exception as e:
                    logging.warning(
                        'exception while checking mime for {}. Skipping'.
                        format(filename))
                    continue

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

    def pdf(self,
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
            nwords = 0
            look_around = False
            if keywords is not None and len(keywords) > 0 and window_size > 0:
                look_around = True
            for filename in glob.iglob(search_path.as_posix(),
                                       recursive=recurse):
                try:
                    mime = magic.from_file(filename, mime=True)
                    if mime.split('/')[1] != 'pdf':
                        logging.warning(
                            'Unrecognized file format {}. Skipping'.format(
                                filename))
                        continue
                except Exception as e:
                    logging.warning(
                        'exception while checking mime for {}. Skipping'.
                        format(filename))
                    continue

                reader = PdfReader(filename)
                npages = len(reader.pages)
                line_count = 0
                for i in range(npages):
                    page = reader.pages[i]
                    text = page.extract_text()
                    lines = text.split('\n')
                    # Due to the generator and other factors extracting
                    # text from PDF is hard and has un-necessary spaces
                    # or missing spaces. The clean-up code below uses
                    # english_words to make words from the dictionary.
                    # NOTE may cause performance issues.
                    lines = self.cleanup_words(lines)
                    done = False
                    line_count = 0
                    for line in lines:
                        line_count += 1
                        nwords += len(line.split(' '))
                        if nwords >= window_size:
                            nwords = 0
                        match = rex.search(line)
                        keyword_found = False
                        if match is not None:
                            begin, end = match.span()
                            if look_around is True:
                                # check if number of words
                                # match window_size
                                # if not get back pages until they do.
                                nwords_till_now = self.num_words(
                                    lines[0:line_count])
                                if nwords_till_now < window_size:
                                    if i > 1:
                                        j = i - 1
                                        while j > 0 or nwords_till_now >= window_size:
                                            prev_page = reader.pages[j]
                                            prev_text = prev_page.extract_text(
                                            )
                                            prev_lines = prev_text.split('\n')
                                            prev_lines = self.cleanup_words(
                                                prev_lines)
                                            nwords_till_now += self.num_words(
                                                prev_lines)
                                            lines = prev_lines + lines
                                data = '\n'.join(lines)
                                for keyword in keywords:
                                    if data.find(keyword):
                                        keyword_found = True
                                        break
                            nresults += 1
                            result = {
                                'filename': filename,
                                'match': match.group(),
                                'page': i + 1,
                                'line': line_count,
                                'begin': begin - 2,
                                'end': end - 2,
                                'keyword_found': keyword_found
                            }
                            results.append(result)
        return nresults, results
