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

from spacy.lang.en import English


class MatcherBase:
    '''
    MatcherBase is the abstract base class that
    context dependent classes need to implement
    for the classifier to get all the information
    required for scanning a document.
    '''

    def __init__(self):
        pass

    def re_list(self):
        '''
        re_list returns the list of regular expression
        patterns to be searched in the doc
        '''
        return None

    def setup_patterns(self, nlp: English):
        '''
        setup_patterns setup up patterns and matchers for
        a context. This needs to be called at the time
        nlp is loaded.
        '''
        return

    def search_keywords(self, nlp: English, doc):
        '''
        search_keywords perform phrase matches against
        the document and returns the results. The phrase
        matches are setup in setup_patterns.
        '''
        return []

    def analyze(self, search_results):
        '''
        analyze analyzes the search results.
        '''
        return
