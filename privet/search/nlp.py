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

import spacy
from spacy.matcher import Matcher


# Use NLP to classify content that is not easily determinisitc
# unless it is seen in context of its content.
class Nlp:

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.matcher = Matcher(self.nlp.vocab)

    def add_matcher(self, patterns):
        for pattern_key, pattern_list in patterns.items():
            self.matcher.add(pattern_key, pattern_list)
