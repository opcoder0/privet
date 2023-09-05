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
import pathlib

import spacy
from spacy import displacy
from spacy.tokens import Doc

from privet.search import pathfinder
from privet.filetype import pdf
from privet.filetype import text
from privet.types import australia
from privet.types.matcher_base import MatcherBase


class InvalidContextException(Exception):
    '''
    Exception raised for errors related to
    invalid context values.
    '''

    def __init__(self, message='Unsupported context value'):
        self.message = message
        super().__init__(self.message)


class NLPSearcher:
    '''
    NLPSearcher searches documents combines the power of statistical
    search using Spacy's ability to perform named entitiy recognition
    and pattern matches.
    '''

    def __init__(self, context):
        self.nlp = spacy.load('en_core_web_sm')
        self.pathfinder = pathfinder.Pathfinder()
        self.context = None
        self.matcher_base = None
        if context.lower() == 'australia':
            self.matcher_base = australia.Australia()
            self.context = context
        else:
            raise InvalidContextException()

    def visualize(self, filename, style="ent"):
        supported_extensions = ['.txt', '.pdf']
        filename_p = pathlib.Path(filename)
        if filename_p.is_file():
            extn = filename_p.suffix
            if extn in supported_extensions:
                content = None
                if extn == '.txt':
                    txt_doc = text.Text(filename)
                    content = txt_doc.content()
                if extn == '.pdf':
                    pdf_doc = pdf.Pdf(filename)
                    content = pdf_doc.content()
                if content is not None:
                    _, _, _, doc = self._search(content, self.matcher_base,
                                                False)
                    print()
                    print("NOTE: This flag is a developer option \
                        to view model's entity \
                        recognition and matches. The option will \
                        be deprecated")
                    print()
                    displacy.serve(doc, style='ent')
            else:
                print('Unsupported file type')
                return
        else:
            print(f'{filename} is not a file')
            return

    def search(self, file_paths, extn, verbose=0):
        search_results = {}
        filenames = self.pathfinder.findfiles(file_paths, extn, True)
        for filename in filenames:
            if extn == 'pdf':
                doc = pdf.Pdf(filename)
            else:
                doc = text.Text(filename)
            doc_text = doc.as_text()
            ent_by_type, kw_by_type, match_by_type, _ = self._search(
                doc_text, self.matcher_base, verbose)
            search_results[filename] = {}
            search_results[filename]['entities'] = ent_by_type
            search_results[filename]['keywords'] = kw_by_type
            search_results[filename]['regexp'] = match_by_type
        return search_results

    def analyze(self, search_results):
        if self.matcher_base is not None:
            self.matcher_base.analyze(search_results)

    def _search(self, doc_text, matcher_base: MatcherBase, verbose):
        matcher_base.setup_patterns(self.nlp)
        doc = self.nlp(doc_text)
        # self.pipeline.visualize(doc)
        entities = self.entities(doc, verbose)
        keywords_by_type = matcher_base.search_keywords(self.nlp, doc)
        pattern_matches = self.patterns(doc, matcher_base.re_dict())
        return entities, keywords_by_type, pattern_matches, doc

    def entities(self, doc, verbose):
        '''
        entities create map of entities by type
        '''
        entities = {}
        if verbose > 1:
            entities['text'] = {}
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_] += 1
                if verbose > 1:
                    entities['text'][ent.label_].append(ent.text)
            else:
                entities[ent.label_] = 1
                if verbose > 1:
                    entities['text'][ent.label_] = [ent.text]
        return entities

    def patterns(self, doc, regexes):
        '''
        patterns grep all the patterns in the re_dict in the doc
        and return the matches
        '''
        if regexes is None or len(regexes) == 0:
            return {}
        p_match = {}
        for category, regexps in regexes.items():
            p_match[category] = []
            for regexp in regexps:
                for match in re.finditer(regexp, doc.text):
                    start, end = match.span()
                    span = doc.char_span(start, end)
                    if span is not None:
                        p_match[category].append(span.text)
        return p_match
