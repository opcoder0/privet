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


class CreditCard:

    def __init__(self):
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
        # anything like a card number
        self.any_cc_rex = r'(\b\d{4}\s+\d{4}\s+\d{4}\s+\d{4}\b)|(\b\d{16}\b)|(\b\d{15}\b)|(\b\d{4}\s+\d{4}\s+\d{4}\s+\d{3}\b)'

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

    # Luhn algorithm to check if card is valid
    # implementation based on
    # https://en.wikipedia.org/wiki/Luhn_algorithm
    def is_valid(self, card_number):

        sums = 0
        n = len(card_number)
        alt = False
        for i in reversed(range(n)):
            if (i == n - 1):
                alt = True
                continue
            if (alt is False):
                sums += int(card_number[i])
                alt = True
            else:
                v = int(card_number[i]) * 2
                sums += ((v // 10) + (v % 10))
                alt = False

        return ((10 - (sums % 10)) == (int(card_number[n - 1])))
