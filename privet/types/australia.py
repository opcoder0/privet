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

from privet.types import cards
from privet.types.matcher_base import MatcherBase

bank_names_keywords = [
    'Alex Bank', 'AMP Bank', 'Australia & New Zealand Banking Group (ANZ)',
    'Australian Military Bank', 'Australian Mutual Bank',
    'Australian Settlements Limited (ASL)', 'Australian Unity Bank Ltd',
    'Auswide Bank', 'Bank Australia ', 'BankFirst', 'Bank of Melbourne',
    'Bank of Queensland', 'BankSA', 'BankVic', 'Bankwest',
    'Bendigo & Adelaide Bank', 'Beyond Bank Australia', 'Challenger Bank',
    'Commonwealth Bank', 'Gateway Bank', 'G&C Mutual Bank', 'Greater Bank',
    'Heritage Bank', 'Hume Bank', 'IMB Bank', 'Judo Bank', 'IN1Bank',
    'Macquarie Bank', 'ME Bank', 'MyState Bank', 'National Australia Bank',
    'Newcastle Permanent Building Society', 'P&N Bank', 'Police Bank	Sydney',
    'QBank', 'Qudos Bank', 'RACQ Bank', 'Regional Australia Bank',
    'Rural Bank', 'St George Bank', 'Suncorp Bank', 'Teachers Mutual Bank',
    'Tyro Payments', 'UBank', 'Unity Bank', 'Up', 'Westpac', 'Avenue Bank',
    'International Bank of Australia', 'Islamic Bank Australia',
    'Australian Central Credit Union Ltd ', 'Australian Military Bank Ltd',
    'B&E Ltd', 'Bank Australia', 'Bank of Heritage Isle',
    'Bananacoast Community Credit Union Ltd', 'Bankstown City Unity Bank',
    'Broken Hill Community Credit Union Ltd',
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
    'bank account details', 'medicare payments', 'mortgage account',
    'bank payments', 'information branch', 'credit card loan',
    'department of human services', 'local service', 'medicare'
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

regexp_fixedline = [
    r'^\(0[2378]\)\s\d{4}\s\d{4}$', r'^0[2378]\s\d{4}\s\d{4}$',
    r'^\+61\s[2378]\s\d{4}\s\d{4}'
]

regexp_mobile = [
    r'^0[45]\d{2}\s\d{3}\s\d{3}$', r'^\+61\s[45]\d{2}\s\d{3}\s\d{3}$'
]

regexp_bsb = [
    r'^\d{3}-\d{3}$',
    r'^\d{3} \d{3}$',
    r'^\d{4}-\d{5}$',
]

regexp_account_no = [r'^\d{3}\s\d{3}\s\d{3}$', r'^\d{2}-\d{3}-\d{4}$']

regexp_abn_acn = [
    r'^\d{2}[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{3}$', r'^\d{3}\s\d{3}\s\d{3}$'
]

regexp_license = [
    r'^\d{9}$', r'^\d{4}[A-Za-z]{5}$', r'^[A-Za-z]{2}\d{7}$',
    r'^[A-Za-z]{2}\d{2}[A-Za-z]{5}$'
]

regexp_medicare = [
    r'^[2-6]\d{9}\d?', r'^[2-6]\d{3}\s\d{5}\s\d\s\d?$',
    r'^[2-6]\d{3}\s\d{5}\s\d\d?$'
]

regexp_email = [r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$']

regexp_passport = [r'^[NEDFACUX]\d{7}$', r'^P[ABCDEFUWXZ]\d{7}$']

regexp_tfn = [r'^\d{3}\s?\d{3}\s?\d{2,3}$']

matcher_patterns = [{
    'name':
    'financial / banking information',
    'regex': [regexp_bsb, regexp_account_no, cards.any_cards],
    'keywords': [bank_names_keywords, finance_keywords, cards.keywords]
}, {
    'name': 'identification information',
    'regex': [regexp_license, regexp_passport],
    'keywords': [drivers_license_keywords, passport_keywords]
}, {
    'name': 'medicare / health information',
    'regex': [regexp_medicare],
    'keywords': [medicare_keywords]
}, {
    'name': 'address / contact information',
    'regex': [regexp_fixedline, regexp_mobile, regexp_email],
    'keywords': []
}]


class Australia(MatcherBase):

    def __init__(self):
        self.patterns = matcher_patterns

    def get_matchers(self):
        return self.patterns
