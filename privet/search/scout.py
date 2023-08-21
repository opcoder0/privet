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

import mmap
import re

import privet


class Scout:

    # PDF to text conviersion is a pain as there can be unexpected spaces
    # in words and some of those part words can be real dictionary words.
    # The function tries to stich up broken words to the best possible
    # word based on what is found in dictionary. If a part of a broken word
    # happens to be a dictionary word this algorithm just chucks the broken
    # word as-is. This could lead to further issues on that line.
    def cleanup_words(self, elines):
        # line is a cleaned line of text string
        # lines is the cleaned lines that is returned
        # eline is a line before processing (error-line)
        # broken is a list that holds broken up words
        line = ''
        lines = []
        broken = []
        for eline in elines:
            words = eline.split(' ')
            nwords = len(words)
            merged_word = ''
            line = ''
            for i in range(nwords):
                is_a_word = words[i].lower() in privet.wordset
                if is_a_word:
                    if len(broken) > 0:
                        line = line + ' ' + ' '.join(broken)
                    line = line + ' ' + words[i]
                    broken = []
                    continue
                if words[i].endswith('.') or words[i].endswith(';') or words[
                        i].endswith(':') or words[i].endswith(','):
                    if words[i][:-1].lower() in privet.wordset:
                        if len(broken) > 0:
                            line += ' '.join(broken)
                        line = line + ' ' + words[i]
                        broken = []
                        continue
                    else:
                        line = line + ' ' + words[i]
                        broken = []
                        continue
                merged_word += words[i]
                broken.append(words[i])
                if merged_word.lower() in privet.wordset:
                    line = line + ' ' + merged_word
                    merged_word = ''
                    broken = []
            if len(broken) > 0:
                line = line + ' ' + ' '.join(broken)
                broken = []
            lines.append(line)
        return lines

    def num_words(self, lines):
        nwords = 0
        for line in lines:
            nwords += len(line.split(' '))
        return nwords

    def txt(self, regexp, filename, keywords=None, window_size=0):

        nresults = 0
        results = []
        curr_pos = 0
        nwords = 0
        look_around = False
        save_prev = 0
        save_curr = 0
        rex = re.compile(regexp)

        if keywords is not None and len(keywords) > 0 and window_size > 0:
            look_around = True

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

    def pdf(self, regexp, filename, keywords=None, window_size=0):

        nresults = 0
        results = []
        nwords = 0
        look_around = False
        rex = re.compile(regexp)

        if keywords is not None and len(keywords) > 0 and window_size > 0:
            look_around = True

        data = ''
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
                        nwords_till_now = self.num_words(lines[0:line_count])
                        if nwords_till_now < window_size:
                            if i > 1:
                                j = i - 1
                                while j > 0 or nwords_till_now >= window_size:
                                    prev_page = reader.pages[j]
                                    prev_text = prev_page.extract_text()
                                    prev_lines = prev_text.split('\n')
                                    prev_lines = self.cleanup_words(prev_lines)
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
