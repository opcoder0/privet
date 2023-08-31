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

import re

import spacy
from spacy import displacy
from spacy.tokens import Doc

from privet.search import pathfinder
from privet.filetype import pdf
from privet.filetype import text
from privet.types import australia
from privet.types.matcher_base import MatcherBase


class NLPSearcher:
    '''
    NLPSearcher searches documents combines the power of statistical
    search using Spacy's ability to perform named entitiy recognition
    and pattern matches.
    '''

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.pathfinder = pathfinder.Pathfinder()

    def visualize(self, doc, style="ent"):
        if isinstance(doc, Doc):
            displacy.serve(doc, style)
        elif isinstance(doc, str):
            nlp_doc = self.nlp(doc)
            displacy.serve(nlp_doc, style)
        else:
            print('Invalid doc format')

    def search(self, file_paths, extn, context, verbose=False):
        '''
        search performs context specific search
        '''
        search_results = []
        filenames = self.pathfinder.findfiles(file_paths, extn, True)
        matcher_base = None
        if context.lower() == 'australia':
            matcher_base = australia.Australia()
        for filename in filenames:
            if extn == 'pdf':
                doc = pdf.Pdf(filename)
            else:
                doc = text.Text(filename)
            _, pages = doc.as_text()
            result = {}
            ent_by_type, kw_by_type, matches = self._search(
                pages, matcher_base, verbose)
            result[filename] = (ent_by_type, kw_by_type, matches)
            search_results.append(result)
        return search_results

    def analyze(self, search_results, context):
        matcher_base = None
        if context == 'Australia':
            matcher_base = australia.Australia()

        if matcher_base is not None:
            matcher_base.analyze(search_results)

    def _search(self, pages, matcher_base: MatcherBase, verbose):
        all_text = ' '.join(pages)
        all_text = all_text.replace('\n', ' ')
        matcher_base.setup_patterns(self.nlp)
        doc = self.nlp(all_text)
        # self.pipeline.visualize(doc)
        entities = self.entities(doc)
        keywords_by_type = matcher_base.search_keywords(self.nlp, doc)
        pattern_matches = self.patterns(doc, matcher_base.re_list())
        return entities, keywords_by_type, pattern_matches

    def entities(self, doc):
        '''
        entities create map of entities by type
        '''
        entities = {}
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_] += 1
            else:
                entities[ent.label_] = 1
        return entities

    def patterns(self, doc, re_list):
        '''
        patterns grep all the patterns in the re_list in the doc
        and return the matches
        '''
        if re_list is None or len(re_list) == 0:
            return []
        pattern_matches = set()
        for regexp in re_list:
            for match in re.finditer(regexp, doc.text):
                start, end = match.span()
                span = doc.char_span(start, end)
                if span is not None:
                    pattern_matches.add(span.text)
        return list(pattern_matches)
