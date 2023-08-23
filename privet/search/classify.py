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

from privet.search import pathfinder
from privet.search import nlp
from privet.filetype import pdf
from privet.filetype import text
from privet.types import australia
from privet.types.matcher_base import MatcherBase

from spacy.matcher import Matcher


class Classify:

    def __init__(self, pipeline: nlp.Nlp):
        self.pipeline = pipeline
        self.pathfinder = pathfinder.Pathfinder()

    def search(self, file_paths, extn, context):
        search_results = []
        filenames = self.pathfinder.findfiles(file_paths, extn, True)
        mb = None
        if context.lower() == 'australia':
            mb = australia.Australia()

        for filename in filenames:
            if extn == 'pdf':
                doc = pdf.Pdf(filename)
            else:
                doc = text.Text(filename)
            _, pages = doc.as_text()
            result = {}
            entities, matcher_results = self.classify(pages, mb)
            result[filename] = (entities, matcher_results)
            search_results.append(result)
        return search_results

    def classify(self, pages, mb: MatcherBase):

        all_text = ' '.join(pages)
        # TODO remove newlines at the source
        all_text = all_text.replace('\n', ' ')
        doc = self.pipeline.nlp(all_text)
        entities = self.entities(doc)
        matcher_patterns = mb.get_matchers()
        matcher_results = []
        for mp_dict in matcher_patterns:
            n_kw = self.match(doc, mp_dict['name'], mp_dict['keywords'])
            n_regex = self.patterns(doc, mp_dict['regex'])
            v = {}
            v[mp_dict['name']] = {'keywords': n_kw, 'regex': n_regex}
            matcher_results.append(v)
        return entities, matcher_results

    def entities(self, doc):
        entities = {}
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_] += 1
            else:
                entities[ent.label_] = 1
        return entities

    def match(self, doc, name, list_of_kwlist):

        if len(list_of_kwlist) == 0:
            return 0

        matcher_pattern = []
        matcher = Matcher(self.pipeline.nlp.vocab)
        # add the keywords
        for kwlist in list_of_kwlist:
            for kw in kwlist:
                bn_pattern = list()
                parts = kw.split(' ')
                if len(parts) == 1:
                    bn_pattern.append({"LEMMA": parts[0]})
                elif len(parts) > 1:
                    for part in parts:
                        bn_pattern.append({"LOWER": part.lower()})
                matcher_pattern.append(bn_pattern)

        matcher.add(name, matcher_pattern)
        matches = matcher(doc)
        # print("Matches:",
        #      [doc[start:end].text for match_id, start, end in matches])
        return len(matches)

    def patterns(self, doc, list_of_re_list):

        if len(list_of_re_list) == 0:
            return 0

        n_patterns = 0
        for re_list in list_of_re_list:
            for regexp in re_list:
                for match in re.finditer(regexp, doc.text):
                    start, end = match.span()
                    span = doc.char_span(start, end)
                    if span is not None:
                        n_patterns += 1
        return n_patterns
