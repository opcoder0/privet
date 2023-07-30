#!/usr/bin/env python

# Copyright 2023 Sai Kiran Gummaraj <saikiran.gummaraj@gmail.com>
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
import sys
from . import libag


class Text:

    def __init__(self):
        # Initiate Ag library with default options.
        libag.ag_init()

        # card regex for validating credit card numbers from
        # https://www.regular-expressions.info/creditcard.html
        # recognizes Visa, MasterCard, American Express, Diners Club,
        # Discover and JCB
        #
        # Visa, Master, Diners, JCB = 16 digits
        visa_card = r'\b(?:4[0-9]{12}(?:[0-9]{3})?)\b'
        self.re_visa = re.compile(visa_card)
        master_card = r'\b(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}\b'
        self.re_master = re.compile(master_card)
        diners_card = r'\b3(?:0[0-5]|[68][0-9])[0-9]{11}\b'
        self.re_diners = re.compile(diners_card)
        jcb = r'\b(?:2131|1800|35\d{3})\d{11}\b'
        self.re_jcb = re.compile(jcb)
        # Amex = 15 digits
        amex_card = r'\b3[47][0-9]{13}\b'
        self.re_amex = re.compile(amex_card)

    def __del__(self):
        # Release Ag resources.
        libag.ag_finish()

    def search(self, file_paths):
        self.search_credit_cards(file_paths)

    def search_credit_cards(self, file_paths):

        # look for numbers that look like credit card with or without space in between
        card_regex = r'(\b\d{4}\s+\d{4}\s+\d{4}\s+\d{4}\b)|(\b\d{16}\b)|(\b\d{15}\b)|(\b\d{4}\s+\d{4}\s+\d{4}\s+\d{3}\b)'
        # Search.
        nresults, results = libag.ag_search(card_regex, file_paths)
        if nresults == 0:
            print("no result found")
        else:
            print("{} credit card(s) found".format(nresults))
            for file in results:
                for match in file.matches:
                    print("file: {}, match: {}, start: {} / end: {}, type: {}".
                          format(file.file, match.match, match.byte_start,
                                 match.byte_end,
                                 self.card_type(match.match.replace(" ", ""))))

        # Free all resources.
        if nresults:
            libag.ag_free_all_results(results)

    def card_type(self, card_number):
        visa = self.re_visa.match(card_number)
        if visa is not None:
            return "Visa"
        master = self.re_master.match(card_number)
        if master is not None:
            return "MasterCard"
        amex = self.re_amex.match(card_number)
        if amex is not None:
            return "Amex"
        diners = self.re_diners.match(card_number)
        if diners is not None:
            return "Diners"
        jcb = self.re_jcb.match(card_number)
        if jcb is not None:
            return "JCB"
        return "Invalid/Unknown"
