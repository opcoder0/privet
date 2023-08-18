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
from privet.search import pathfinder
from privet.types import cards
from privet.types import iban
from privet.types import passport


class Native:

    def __init__(self):
        self.cc = cards.CreditCard()
        self.iban = iban.Iban()
        self.passport = passport.Passport()
        self.pathfinder = pathfinder.Pathfinder()

    def search(self, file_paths):
        # search credit card
        n_cards, cards = self.pathfinder.find(self.cc.any_cc_rex,
                                              file_paths,
                                              'txt',
                                              True,
                                              self.cc.keywords,
                                              window_size=250)
        print("Found {} cards".format(n_cards))
        for card in cards:
            card_number = card['match']
            card_number = card_number.replace(" ", "")
            is_valid = self.cc.is_valid(card_number)
            card_type = self.cc.card_type(card_number)
            filename = card['filename']
            page = card['page']
            line = card['line']
            begin = card['begin']
            end = card['end']
            keyword_found = card['keyword_found']
            print(
                'f:{fname},cc:{cc},t:{cctype},v:{valid},p:{page},l:{line},b:{bp},e:{ep},keyword_found:{kw}'
                .format(fname=filename,
                        cc=card_number,
                        cctype=card_type,
                        valid=is_valid,
                        page=page,
                        line=line,
                        bp=begin,
                        ep=end,
                        kw=keyword_found))
        # search IBAN
        n_ibans, ibans = self.pathfinder.find(self.iban.any_iban_rex,
                                              file_paths, 'txt', True)
        print("Found {} IBANs".format(n_ibans))
        for iban in ibans:
            iban_number = iban['match']
            iban_number = iban_number.replace(" ", "")
            is_valid = self.iban.is_valid(iban_number)
            filename = iban['filename']
            page = iban['page']
            line = iban['line']
            begin = iban['begin']
            end = iban['end']
            keyword_found = iban['keyword_found']
            print(
                'f:{fname},cc:{iban},v:{valid},p:{page},l:{line},b:{bp},e:{ep},keyword_found:{kw}'
                .format(fname=filename,
                        iban=iban_number,
                        valid=is_valid,
                        page=page,
                        line=line,
                        bp=begin,
                        ep=end,
                        kw=keyword_found))
