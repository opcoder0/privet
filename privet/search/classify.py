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

import json

from privet.search import pathfinder
from privet.search import nlp
from privet.filetype import pdf
from privet.filetype import text

from privet.types import banks


class Classify:

    def __init__(self, pipeline: nlp.Nlp):
        self.pipeline = pipeline
        self.pathfinder = pathfinder.Pathfinder()

    def search(self, file_paths, extn):
        filenames = self.pathfinder.findfiles(file_paths, extn, True)
        for filename in filenames:
            if extn == 'pdf':
                doc = pdf.Pdf(filename)
            else:
                doc = text.Text(filename)
            _, pages = doc.as_text()
            print('filename: {}'.format(filename))
            self.classify_entity(pages)
            self.classify_pattern(pages)

    def add_banking_pattern(self):
        # bank names
        matcher_pattern = dict()
        for bank_name in banks.bank_names:
            bn_pattern = list()
            parts = bank_name.split(' ')
            for part in parts:
                bn_pattern.append({"TEXT": part})
            bank_pattern = bank_name.replace(' ', '_')
            matcher_pattern[bank_pattern] = [bn_pattern]
        # keywords
        for keyword in banks.statement_keywords:
            bn_pattern = list()
            parts = keyword.split(' ')
            if len(parts) == 1:
                bn_pattern.append({"LEMMA": parts[0]})
            elif len(parts) > 1:
                for part in parts:
                    bn_pattern.append({"LOWER": part})

            kw_pattern = keyword.replace(' ', '_')
            matcher_pattern[kw_pattern] = [bn_pattern]

        self.pipeline.add_matcher(matcher_pattern)

    def classify_entity(self, texts):

        entities = {}
        for text in texts:
            doc = self.pipeline.nlp(text)
            for ent in doc.ents:
                if ent.label_ in entities:
                    entities[ent.label_] += 1
                else:
                    entities[ent.label_] = 1
        print(json.dumps(entities, sort_keys=True, indent=4))

    def classify_pattern(self, texts):
        self.add_banking_pattern()
        all_text = '\n'.join(texts)
        doc = self.pipeline.nlp(all_text)
        matches = self.pipeline.matcher(doc)
        print("Matches:",
              [doc[start:end].text for match_id, start, end in matches])
