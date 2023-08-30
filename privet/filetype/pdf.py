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

import privet


class Pdf:

    def __init__(self, filename):
        self.filename = filename
        try:
            self.reader = PdfReader(filename)
        except OSError as e:
            print(e)
            raise

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
            gobble_limit = 3
            i = 0
            while i < nwords:
                is_a_word = words[i].lower() in privet.wordset
                if is_a_word:
                    # do optimistic gobbling to see if I can get a longer word
                    # due to erratic spacing issues with PDF conversion to text
                    #
                    # backtrack if there is anything in broken list. start from
                    # that point
                    if len(broken) > 0:
                        pos = 1
                        i = list(map(lambda x: x[pos], broken))[0]
                        broken = []
                    gword = words[i]
                    gwlist = []
                    gwlen = 0
                    k = 1
                    for j in range(i + 1, nwords):
                        if k > gobble_limit:
                            break
                        k += 1
                        if j < nwords:
                            gword += words[j]
                            if gword.lower() in privet.wordset:
                                gwlist.append(gword)
                                i = j
                    gwlen = len(gwlist)
                    if gwlen > 0:
                        if len(broken) > 0:
                            pos = 0
                            broken_words = list(map(lambda x: x[pos], broken))
                            line = line + ' ' + ' '.join(broken_words)
                        line = line + ' ' + gwlist[-1]
                    else:
                        # the word did not get any bigger after merging forward
                        if len(broken) > 0:
                            pos = 0
                            broken_words = list(map(lambda x: x[pos], broken))
                            line = line + ' ' + ' '.join(broken_words)
                        line = line + ' ' + words[i]
                    broken = []
                    i += 1
                    continue
                if words[i].endswith('.') or words[i].endswith(';') or words[
                        i].endswith(':') or words[i].endswith(','):
                    if words[i][:-1].lower() in privet.wordset:
                        if len(broken) > 0:
                            pos = 0
                            broken_words = list(map(lambda x: x[pos], broken))
                            line += ' '.join(broken_words)
                        line = line + ' ' + words[i]
                        broken = []
                        i += 1
                        continue
                    else:
                        line = line + ' ' + words[i]
                        broken = []
                        i += 1
                        continue
                merged_word += words[i]
                broken.append((words[i], i))
                i += 1
                if merged_word.lower() in privet.wordset:
                    line = line + ' ' + merged_word
                    merged_word = ''
                    broken = []
            if len(broken) > 0:
                pos = 0
                broken_words = list(map(lambda x: x[pos], broken))
                line = line + ' ' + ' '.join(broken_words)
                broken = []
            lines.append(line)
        return lines

    def num_words(self, lines):
        nwords = 0
        for line in lines:
            nwords += len(line.split(' '))
        return nwords

    def as_text(self):

        pages = []
        npages = len(self.reader.pages)
        for i in range(npages):
            page = self.reader.pages[i]
            text = page.extract_text()
            lines = text.split('\n')
            # Due to the generator and other factors extracting
            # text from PDF is hard and has un-necessary spaces
            # or missing spaces. The clean-up code below uses
            # english_words to make words from the dictionary.
            # NOTE may cause performance issues.
            lines = self.cleanup_words(lines)
            pages.append('\n'.join(lines))

        return npages, pages

    def content(self):
        n, pages = self.as_text()
        result = ''
        for page in pages:
            result += page
        return result
