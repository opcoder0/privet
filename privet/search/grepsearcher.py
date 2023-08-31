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
from privet.search import grepper
from privet.types import cards
from privet.types import iban
from privet.types import passport


class GrepSearcher:
    '''
    GrepSearcher looks for credit card, IBAN, Passport numbers
    in files using regular expression search.
    '''

    def __init__(self):
        self.cc = cards.CreditCard()
        self.iban = iban.Iban()
        self.passport = passport.Passport()
        self.pathfinder = pathfinder.Pathfinder()
        self.grepper = grepper.Grepper()

    def print_results(self, r_type, n_results, results):
        if n_results == 0:
            return
        for result in results:
            result_json = {'type': r_type, 'result': result, 'details': {}}
            if r_type == 'card':
                card_number = result['match'].replace(" ", "")
                is_valid = self.cc.is_valid(card_number)
                card_type = self.cc.card_type(card_number)
                result_json['details']['valid'] = is_valid
                result_json['details']['cardtype'] = card_type
            elif r_type == 'iban':
                iban_number = result['match'].replace(" ", "")
                is_valid = self.iban.is_valid(iban_number)
                result_json['details']['valid'] = is_valid
            print(json.dumps(result_json, sort_keys=True, indent=4))

    def search(self, file_paths, extn):
        filenames = self.pathfinder.findfiles(file_paths, extn, True)
        query = {
            'card': (self.cc.any_cc_rex, self.cc.keywords),
            'iban': (self.iban.any_iban_rex, self.iban.keywords),
        }
        for q_type, q_options in query.items():
            for filename in filenames:
                if extn == 'txt':
                    n_results, results = self.grepper.txt_file(q_options[0],
                                                               filename,
                                                               q_options[1],
                                                               window_size=250)
                elif extn == 'pdf':
                    n_results, results = self.grepper.pdf_file(q_options[0],
                                                               filename,
                                                               q_options[1],
                                                               window_size=250)
                else:
                    raise Exception("Unsupported file extension")
                self.print_results(q_type, n_results, results)
