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

import sys
from . import libag
from . import credit_card


class Text:

    def __init__(self):
        # Initiate Ag library with default options.
        libag.ag_init()
        self.cc = credit_card.CreditCard()

    def __del__(self):
        # Release Ag resources.
        libag.ag_finish()

    def search(self, file_paths):
        self.search_credit_cards(file_paths)

    def search_credit_cards(self, file_paths):

        # Search.
        nresults, results = libag.ag_search(self.cc.any_cc_rex, file_paths)
        if nresults == 0:
            print("no result found")
        else:
            print("{} credit card(s) found".format(nresults))
            for file in results:
                for match in file.matches:
                    print("file: {}, match: {}, start: {} / end: {}, type: {}".
                          format(
                              file.file, match.match, match.byte_start,
                              match.byte_end,
                              self.cc.card_type(match.match.replace(" ", ""))))

        # Free all resources.
        if nresults:
            libag.ag_free_all_results(results)
