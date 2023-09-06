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

# list of all bank names by alphabetical order
# source https://en.wikipedia.org/wiki/List_of_banks_in_Australia

import pathlib

from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from tabulate import tabulate

from privet.types.matcher_base import MatcherBase
from privet.types import cards

bank_names = [
    'Alex Bank', 'AMP Bank', 'Australia & New Zealand Banking Group (ANZ)',
    'Australia and New Zealand Banking Group', 'Australian Military Bank',
    'Australian Mutual Bank', 'Australian Settlements Limited (ASL)',
    'Australian Unity Bank Ltd', 'Auswide Bank', 'Bank Australia ',
    'BankFirst', 'Bank of Melbourne', 'Bank of Queensland', 'BankSA',
    'BankVic', 'Bankwest', 'Bendigo & Adelaide Bank', 'Beyond Bank Australia',
    'Challenger Bank', 'Commonwealth Bank', 'Gateway Bank', 'G&C Mutual Bank',
    'Greater Bank', 'Heritage Bank', 'Hume Bank', 'IMB Bank', 'Judo Bank',
    'IN1Bank', 'Macquarie Bank', 'ME Bank', 'MyState Bank',
    'National Australia Bank', 'Newcastle Permanent Building Society',
    'P&N Bank', 'Police Bank	Sydney', 'QBank', 'Qudos Bank', 'RACQ Bank',
    'Regional Australia Bank', 'Rural Bank', 'St George Bank', 'Suncorp Bank',
    'Teachers Mutual Bank', 'Tyro Payments', 'UBank', 'Unity Bank', 'Up',
    'Westpac', 'Avenue Bank', 'International Bank of Australia',
    'Islamic Bank Australia', 'Australian Central Credit Union Ltd ',
    'Australian Military Bank Ltd', 'B&E Ltd', 'Bank Australia',
    'Bank of Heritage Isle', 'Bananacoast Community Credit Union Ltd',
    'Bankstown City Unity Bank', 'Broken Hill Community Credit Union Ltd',
    'Cairns Penny Savings & Loans Ltd', 'Catalyst Money',
    'Central Murray Credit Union Ltd', 'Central West Credit Union Ltd',
    'Coastline Credit Union Ltd', 'Community Alliance Credit Union Ltd',
    'Community CPS Australia Ltd', 'Community First Credit Union Ltd',
    'Credit Union Australia Ltd', 'Credit Union', 'Defence Force Credit Union',
    'DNISTER Ukrainian Credit Co-operative Ltd', 'EECU Ltd',
    'Family First Credit Union Ltd',
    'Fire Brigades Employees Credit Union Ltd',
    'Fire Service Credit Union Ltd', 'Firefighters Mutual Bank',
    'First Choice Credit Union Ltd', 'First Option Credit Union Ltd',
    'Ford Co-operative Credit Society Ltd', 'G&C Mutual Bank Ltd',
    'Goulburn Murray Credit Union Cooperative Ltd', 'Greater Bank',
    'Heritage Bank', 'Horizon Credit Union Ltd', 'Hume Bank',
    'Illawarra Credit Union', 'IMB Limited', 'Intech Bank',
    'Laboratories Credit Union Ltd', 'Lysaght Credit Union Ltd',
    'Macarthur Credit Union Ltd', 'Macquarie Credit Union Ltd',
    'Maitland Mutual Building Society Ltd', 'Northern Inland Credit Union Ltd',
    'NOVA Mutual Ltd', 'Orange Credit Union Ltd',
    'Police Financial Services Limited', 'Police Bank Ltd',
    'Police & Nurses Ltd', 'Police Credit Union Ltd', 'QPCU Ltd',
    'Queensland Country Bank Ltd', 'Railways Credit Union Ltd',
    'Regional Australia Bank', 'Shoalhaven Community Credit Union',
    'South West Slopes Credit Union Ltd', 'Southern Cross Credit Union Ltd',
    'South-West Credit Union Co-Operative Ltd', 'Summerland Credit Union Ltd',
    'Teachers Mutual Bank Ltd', 'The Capricornian Ltd',
    'Traditional Credit Union Ltd', 'Transport Mutual Credit Union Ltd',
    'UniBank Homebush', 'Unity Bank Ltd', 'Victoria Teachers Ltd',
    'Warwick Credit Union Ltd', 'WAW Credit Union Co-Operative Ltd',
    'Woolworths Team Bank Ltd'
]

finance_keywords = [
    'swift bank code', 'correspondent bank', 'base currency', 'usa account',
    'holder address', 'bank address', 'information account', 'fund transfers',
    'bank charges', 'bank details', 'banking information', 'full names',
    'account balance', 'opening balance', 'balance', 'transaction',
    'transaction details', 'debit', 'credit', 'account number',
    'account details', 'credit card number', 'card number', 'bsb number',
    'bsb', 'australia business no', 'business number', 'abn#', 'businessid#',
    'business ID', 'abn', 'businessno#', 'acn', 'australia company no',
    'australia company no#', 'australia company number',
    'australian company no', 'australian company no#',
    'australian company number'
]

drivers_license_keywords = [
    "international driving permits", "australian automobile association",
    "international driving permit", "DriverLicence", "DriverLicences",
    "Driver Lic", "Driver Licence", "Driver Licences", "DriversLic",
    "DriversLicence", "DriversLicences", "Drivers Lic", "Drivers Lics",
    "Drivers Licence", "Drivers Licences", "Driver'Lic", "Driver'Lics",
    "Driver'Licence", "Driver'Licences", "Driver' Lic", "Driver' Lics",
    "Driver' Licence", "Driver' Licences", "Driver'sLic", "Driver'sLics",
    "Driver'sLicence", "Driver'sLicences", "Driver's Lic", "Driver's Lics",
    "Driver's Licence", "Driver's Licences", "DriverLic#", "DriverLics#",
    "DriverLicence#", "DriverLicences#", "Driver Lic#", "Driver Lics#",
    "Driver Licence#", "Driver Licences#", "DriversLic#", "DriversLics#",
    "DriversLicence#", "DriversLicences#", "Drivers Lic#", "Drivers Lics#",
    "Drivers Licence#", "Drivers Licences#", "Driver'Lic#", "Driver'Lics#",
    "Driver'Licence#", "Driver'Licences#", "Driver' Lic#", "Driver' Lics#",
    "Driver' Licence#", "Driver' Licences#", "Driver'sLic#", "Driver'sLics#",
    "Driver'sLicence#", "Driver'sLicences#", "Driver's Lic#", "Driver's Lics#",
    "Driver's Licence#", "Driver's Licences#"
]

medicare_keywords = [
    'medicare payments', 'department of human services', 'medicare', 'medibank'
]

passport_keywords = [
    'passport#', 'passport #', 'passportid', 'passports', 'passportno',
    'passport no', 'passportnumber', 'passport number', 'passportnumbers',
    'passport numbers', 'passport details', 'immigration and citizenship',
    'commonwealth of australia', 'department of immigration',
    'national identity card', 'travel document', 'issuing authority'
]

tfn_keywords = [
    'australian business number', 'marginal tax rate', 'medicare levy',
    'portfolio number', 'service veterans', 'withholding tax',
    'individual tax return', 'tax file number', 'tfn'
]

# regexp_fixedline = [
#     r'\b\(0[2378]\) \d{4} \d{4}\b', r'\b0[2378] \d{4} \d{4}\b',
#     r'\b\+61 [2378] \d{4} \d{4}\b'
# ]
# regexp_mobile = [
#     r'\b0[45]\d{2} \d{3} \d{3}\b', r'\b\+61 [45]\d{2} \d{3} \d{3}\b'
# ]
# regexp_bsb = [r'\b\d{3}-\d{3}\b', r'\b\d{3} \d{3}\b']
# regexp_account_no = [
#     r'\b\d{3} \d{3} \d{3}\b', r'\b\d{2}-\d{3}-\d{4}\b', r'\b\d{4}-\d{5}\b'
# ]
# regexp_abn_acn = [
#     r'\b\d{2}[- ]?\d{3}[- ]?\d{3}[- ]?\d{3}\b', r'\b\d{3} \d{3} \d{3}\b'
# ]
# regexp_license = [
#     r'\b\d{9}\b', r'\b\d{4}[A-Za-z]{5}\b', r'\b[A-Za-z]{2}\d{7}\b',
#     r'\b[A-Za-z]{2}\d{2}[A-Za-z]{5}\b'
# ]
# regexp_medicare = [
#     r'\b[2-6]\d{9}\d?\b', r'\b[2-6]\d{3} \d{5} \d \d?\b',
#     r'\b[2-6]\d{3} \d{5} \d\d?\b'
# ]
# regexp_passport = [r'\b[NEDFACUX]\d{7}\b', r'\bP[ABCDEFUWXZ]\d{7}\b']
# regexp_tfn = [r'\b\d{3} ?\d{3} ?\d{2,3}\b']

regexp_email = [
    r'\b([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})\b'
]


class Australia(MatcherBase):
    '''
    Australia implements MatcherBase and contains keywords, patterns,
    matchers, entities that are relevant in Australia.
    '''

    def __init__(self):
        self.matcher = None
        self.ruler = None
        self.setup_complete = False

    def re_dict(self):
        '''
        re_dict returns the list of regular expression patterns
        that needs to be matched against the document.
        '''
        # NOTE if there are multiple patterns under a single category
        # like email. Just append them all into a single list.
        search_patterns = {
            'email': regexp_email,
            'credit-card': cards.any_cards
        }
        return search_patterns

    def setup_patterns(self, nlp: English):
        '''
        setup_patterns sets up the necessary keywords and patterns
        relevant to this domain
        '''
        if self.setup_complete is True:
            return

        keywords = {
            'Finance': finance_keywords,
            'Drivers License': drivers_license_keywords,
            'Medicare': medicare_keywords,
            'Passport': passport_keywords,
            'TFN': tfn_keywords,
            'Credit Card': cards.keywords
        }
        self.matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        for name, kws in keywords.items():
            patterns = [nlp.make_doc(kw) for kw in kws]
            self.matcher.add(name, patterns)

        self.ruler = nlp.add_pipe('entity_ruler', before='ner')
        self.ruler.from_disk('privet/types/patterns.jsonl')
        self.setup_complete = True

        patterns = []
        for bank in bank_names:
            pattern = {'label': 'BANK', 'pattern': bank}
            patterns.append(pattern)
        self.ruler.add_patterns(patterns)

    def search_keywords(self, nlp: English, doc):
        keywords = {}
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            keyword_str = nlp.vocab.strings[match_id]
            if keyword_str in keywords:
                keywords[keyword_str].add(span.text)
            else:
                keywords[keyword_str] = set()
                keywords[keyword_str].add(span.text)
        for match_id_str, keyword_set in keywords.items():
            keywords[match_id_str] = list(keyword_set)
        return keywords

    def analyze(self, search_results):
        table = []
        for filename, details in search_results.items():
            row = []
            row.append(pathlib.Path(filename).name)
            entity = details['entities']
            is_bank = False
            if entity.get('BANK') is not None:
                row.append('Bank')
                is_bank = True
            else:
                if entity.get('ORG') is not None:
                    row.append('Other')
                else:
                    row.append('None')

            if entity.get('PERSON') is not None:
                row.append('Yes')
            else:
                row.append('No')

            if entity.get('ACCOUNT_NUMBER') is not None:
                row.append('Likely')
            else:
                row.append('Unlikely')

            if entity.get('BSB_NUMBER') is not None:
                row.append('Likely')
            else:
                row.append('Unlikely')

            kw_types = [kw_cat for kw_cat in details['keywords']]
            if len(kw_types) > 0:
                row.append(', '.join(kw_types))
            else:
                row.append('None')

            regex_matches = details['regexp']
            if 'credit-card' in regex_matches and len(
                    regex_matches['credit-card']) > 0:
                row.append('Likely')
            else:
                row.append('Unlikely')

            if 'email' in regex_matches and len(regex_matches['email']) > 0:
                row.append('Likely')
            else:
                row.append('Unlikely')

            table.append(row)
        print(
            tabulate(table,
                     headers=[
                         'Filename', 'Organization Type', 'Person',
                         'Account Number', 'BSB Number', 'Keyword Categories',
                         'Credit Card No.', 'Email'
                     ],
                     tablefmt='mixed_grid'))
