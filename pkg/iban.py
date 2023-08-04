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


class Iban:

    def __init__(self):
        # list of registered and partially registered countries
        # https://www.iban.com/structure

        # list of registered countries
        self.iban_register_by_countrycode = {
            "AL": {
                "country": "Albania",
                "sepa": "No",
                "ndigits": 28
            },
            "AD": {
                "country": "Andorra",
                "sepa": "Yes",
                "ndigits": 24
            },
            "AT": {
                "country": "Austria",
                "sepa": "Yes",
                "ndigits": 20
            },
            "AZ": {
                "country": "Azerbaijan",
                "sepa": "No",
                "ndigits": 28
            },
            "BH": {
                "country": "Bahrain",
                "sepa": "No",
                "ndigits": 22
            },
            "BY": {
                "country": "Belarus",
                "sepa": "No",
                "ndigits": 28
            },
            "BE": {
                "country": "Belgium",
                "sepa": "Yes",
                "ndigits": 16
            },
            "BR": {
                "country": "Brazil",
                "sepa": "No",
                "ndigits": 29
            },
            "BG": {
                "country": "Bulgaria",
                "sepa": "Yes",
                "ndigits": 22
            },
            "BI": {
                "country": "Burundi",
                "sepa": "No",
                "ndigits": 27
            },
            "HR": {
                "country": "Croatia",
                "sepa": "Yes",
                "ndigits": 21
            },
            "CY": {
                "country": "Cyprus",
                "sepa": "Yes",
                "ndigits": 28
            },
            "DK": {
                "country": "Denmark",
                "sepa": "Yes",
                "ndigits": 18
            },
            "DJ": {
                "country": "Djibouti",
                "sepa": "No",
                "ndigits": 27
            },
            "EG": {
                "country": "Egypt",
                "sepa": "No",
                "ndigits": 29
            },
            "EE": {
                "country": "Estonia",
                "sepa": "Yes",
                "ndigits": 20
            },
            "FI": {
                "country": "Finland",
                "sepa": "Yes",
                "ndigits": 18
            },
            "FR": {
                "country": "France",
                "sepa": "Yes",
                "ndigits": 27
            },
            "GE": {
                "country": "Georgia",
                "sepa": "No",
                "ndigits": 22
            },
            "DE": {
                "country": "Germany",
                "sepa": "Yes",
                "ndigits": 22
            },
            "GI": {
                "country": "Gibraltar",
                "sepa": "Yes",
                "ndigits": 23
            },
            "GR": {
                "country": "Greece",
                "sepa": "Yes",
                "ndigits": 27
            },
            "GL": {
                "country": "Greenland",
                "sepa": "No",
                "ndigits": 18
            },
            "GT": {
                "country": "Guatemala",
                "sepa": "No",
                "ndigits": 28
            },
            "HU": {
                "country": "Hungary",
                "sepa": "Yes",
                "ndigits": 28
            },
            "IS": {
                "country": "Iceland",
                "sepa": "Yes",
                "ndigits": 26
            },
            "IQ": {
                "country": "Iraq",
                "sepa": "No",
                "ndigits": 23
            },
            "IE": {
                "country": "Ireland",
                "sepa": "Yes",
                "ndigits": 22
            },
            "IL": {
                "country": "Israel",
                "sepa": "No",
                "ndigits": 23
            },
            "IT": {
                "country": "Italy",
                "sepa": "Yes",
                "ndigits": 27
            },
            "JO": {
                "country": "Jordan",
                "sepa": "No",
                "ndigits": 30
            },
            "KZ": {
                "country": "Kazakhstan",
                "sepa": "No",
                "ndigits": 20
            },
            "XK": {
                "country": "Kosovo",
                "sepa": "No",
                "ndigits": 20
            },
            "KW": {
                "country": "Kuwait",
                "sepa": "No",
                "ndigits": 30
            },
            "LV": {
                "country": "Latvia",
                "sepa": "Yes",
                "ndigits": 21
            },
            "LB": {
                "country": "Lebanon",
                "sepa": "No",
                "ndigits": 28
            },
            "LY": {
                "country": "Libya",
                "sepa": "No",
                "ndigits": 25
            },
            "LI": {
                "country": "Liechtenstein",
                "sepa": "Yes",
                "ndigits": 21
            },
            "LT": {
                "country": "Lithuania",
                "sepa": "Yes",
                "ndigits": 20
            },
            "LU": {
                "country": "Luxembourg",
                "sepa": "Yes",
                "ndigits": 20
            },
            "MT": {
                "country": "Malta",
                "sepa": "Yes",
                "ndigits": 31
            },
            "MR": {
                "country": "Mauritania",
                "sepa": "No",
                "ndigits": 27
            },
            "MU": {
                "country": "Mauritius",
                "sepa": "No",
                "ndigits": 30
            },
            "MD": {
                "country": "Moldova",
                "sepa": "No",
                "ndigits": 24
            },
            "MC": {
                "country": "Monaco",
                "sepa": "Yes",
                "ndigits": 27
            },
            "MN": {
                "country": "Mongolia",
                "sepa": "No",
                "ndigits": 20
            },
            "ME": {
                "country": "Montenegro",
                "sepa": "No",
                "ndigits": 22
            },
            "NL": {
                "country": "Netherlands",
                "sepa": "Yes",
                "ndigits": 18
            },
            "NI": {
                "country": "Nicaragua",
                "sepa": "No",
                "ndigits": 28
            },
            "NO": {
                "country": "Norway",
                "sepa": "Yes",
                "ndigits": 15
            },
            "PK": {
                "country": "Pakistan",
                "sepa": "No",
                "ndigits": 24
            },
            "PS": {
                "country": "Palestine",
                "sepa": "No",
                "ndigits": 29
            },
            "PL": {
                "country": "Poland",
                "sepa": "Yes",
                "ndigits": 28
            },
            "PT": {
                "country": "Portugal",
                "sepa": "Yes",
                "ndigits": 25
            },
            "QA": {
                "country": "Qatar",
                "sepa": "No",
                "ndigits": 29
            },
            "RO": {
                "country": "Romania",
                "sepa": "Yes",
                "ndigits": 24
            },
            "RU": {
                "country": "Russia",
                "sepa": "No",
                "ndigits": 33
            },
            "RS": {
                "country": "Serbia",
                "sepa": "No",
                "ndigits": 22
            },
            "SC": {
                "country": "Seychelles",
                "sepa": "No",
                "ndigits": 31
            },
            "SK": {
                "country": "Slovakia",
                "sepa": "Yes",
                "ndigits": 24
            },
            "SI": {
                "country": "Slovenia",
                "sepa": "Yes",
                "ndigits": 19
            },
            "SO": {
                "country": "Somalia",
                "sepa": "No",
                "ndigits": 23
            },
            "ES": {
                "country": "Spain",
                "sepa": "Yes",
                "ndigits": 24
            },
            "SD": {
                "country": "Sudan",
                "sepa": "No",
                "ndigits": 18
            },
            "SE": {
                "country": "Sweden",
                "sepa": "Yes",
                "ndigits": 24
            },
            "CH": {
                "country": "Switzerland",
                "sepa": "Yes",
                "ndigits": 21
            },
            "TL": {
                "country": "Timor-Leste",
                "sepa": "No",
                "ndigits": 23
            },
            "TN": {
                "country": "Tunisia",
                "sepa": "No",
                "ndigits": 24
            },
            "TR": {
                "country": "Turkey",
                "sepa": "No",
                "ndigits": 26
            },
            "UA": {
                "country": "Ukraine",
                "sepa": "No",
                "ndigits": 29
            },
            "BA": {
                "country": "Bosnia and Herzegovina",
                "sepa": "No",
                "ndigits": 20
            },
            "CR": {
                "country": "Costa Rica",
                "sepa": "No",
                "ndigits": 22
            },
            "CZ": {
                "country": "Czech Republic",
                "sepa": "Yes",
                "ndigits": 24
            },
            "DO": {
                "country": "Dominican Republic",
                "sepa": "No",
                "ndigits": 28
            },
            "SV": {
                "country": "El Salvador",
                "sepa": "No",
                "ndigits": 28
            },
            "FK": {
                "country": "Falkland Islands",
                "sepa": "No",
                "ndigits": 18
            },
            "FO": {
                "country": "Faroe Islands",
                "sepa": "No",
                "ndigits": 18
            },
            "VA": {
                "country": "Holy See (the)",
                "sepa": "Yes",
                "ndigits": 22
            },
            "MK": {
                "country": "North Macedonia",
                "sepa": "No",
                "ndigits": 19
            },
            "LC": {
                "country": "Saint Lucia",
                "sepa": "No",
                "ndigits": 32
            },
            "SM": {
                "country": "San Marino",
                "sepa": "Yes",
                "ndigits": 27
            },
            "ST": {
                "country": "Sao Tome and Principe",
                "sepa": "No",
                "ndigits": 25
            },
            "SA": {
                "country": "Saudi Arabia",
                "sepa": "No",
                "ndigits": 24
            },
            "AE": {
                "country": "United Arab Emirates",
                "sepa": "No",
                "ndigits": 23
            },
            "GB": {
                "country": "United Kingdom",
                "sepa": "Yes",
                "ndigits": 22
            },
            "VG": {
                "country": "Virgin Islands, British",
                "sepa": "No",
                "ndigits": 24
            }
        }

        # list of partiab IBAN countries
        self.iban_partial = {
            "DZ": {
                "country": "Algeria",
                "sepa": "No",
                "ndigits": 26
            },
            "AO": {
                "country": "Angola",
                "sepa": "No",
                "ndigits": 25
            },
            "BJ": {
                "country": "Benin",
                "sepa": "No",
                "ndigits": 28
            },
            "BF": {
                "country": "Burkina Faso",
                "sepa": "No",
                "ndigits": 28
            },
            "CM": {
                "country": "Cameroon",
                "sepa": "No",
                "ndigits": 27
            },
            "CV": {
                "country": "Cape Verde",
                "sepa": "No",
                "ndigits": 25
            },
            "CF": {
                "country": "Central African Republic",
                "sepa": "No",
                "ndigits": 27
            },
            "TD": {
                "country": "Chad",
                "sepa": "No",
                "ndigits": 27
            },
            "KM": {
                "country": "Comoros",
                "sepa": "No",
                "ndigits": 27
            },
            "CG": {
                "country": "Congo",
                "sepa": "No",
                "ndigits": 27
            },
            "GQ": {
                "country": "Equatorial Guinea",
                "sepa": "No",
                "ndigits": 27
            },
            "GA": {
                "country": "Gabon",
                "sepa": "No",
                "ndigits": 27
            },
            "GW": {
                "country": "Guinea-Bissau",
                "sepa": "No",
                "ndigits": 25
            },
            "HN": {
                "country": "Honduras",
                "sepa": "No",
                "ndigits": 28
            },
            "IR": {
                "country": "Iran",
                "sepa": "No",
                "ndigits": 26
            },
            "CI": {
                "country": "Ivory Coast",
                "sepa": "No",
                "ndigits": 28
            },
            "MG": {
                "country": "Madagascar",
                "sepa": "No",
                "ndigits": 27
            },
            "ML": {
                "country": "Mali",
                "sepa": "No",
                "ndigits": 28
            },
            "MA": {
                "country": "Morocco",
                "sepa": "No",
                "ndigits": 28
            },
            "MZ": {
                "country": "Mozambique",
                "sepa": "No",
                "ndigits": 25
            },
            "NE": {
                "country": "Niger",
                "sepa": "No",
                "ndigits": 28
            },
            "SN": {
                "country": "Senegal",
                "sepa": "No",
                "ndigits": 28
            },
            "TG": {
                "country": "Togo",
                "sepa": "No",
                "ndigits": 28
            },
        }
        self.any_iban_rex = r'\bAL\d{10}[0-9A-Z]{16}\b|\bAD\d{10}[0-9A-Z]{12}\b|\bAT\d{18}\b|\bBH\d{2}[A-Z]{4}[0-9A-Z]{14}\b|\bBE\d{14}\b|\bBA\d{18}\b|\bBG\d{2}[A-Z]{4}\d{6}[0-9A-Z]{8}\b|\bHR\d{19}\b|\bCY\d{10}[0-9A-Z]{16}\b|\bCZ\d{22}\b|\bDK\d{16}\b|\bFO\d{16}\b|\bGL\d{16}\b|\bDO\d{2}[0-9A-Z]{4}\d{20}\b|\bEE\d{18}\b|\bFI\d{16}\b|\bFR\d{12}[0-9A-Z]{11}\d{2}\b|\bGE\d{2}[A-Z]{2}\d{16}\b|\bDE\d{20}\b|\bGI\d{2}[A-Z]{4}[0-9A-Z]{15}\b|\bGR\d{9}[0-9A-Z]{16}\b|\bHU\d{26}\b|\bIS\d{24}\b|\bIE\d{2}[A-Z]{4}\d{14}\b|\bIL\d{21}\b|\bIT\d{2}[A-Z]\d{10}[0-9A-Z]{12}\b|\b[A-Z]{2}\d{5}[0-9A-Z]{13}\b|\bKW\d{2}[A-Z]{4}22!\b|\bLV\d{2}[A-Z]{4}[0-9A-Z]{13}\b|\bLB\d{6}[0-9A-Z]{20}\b|\bLI\d{7}[0-9A-Z]{12}\b|\bLT\d{18}\b|\bLU\d{5}[0-9A-Z]{13}\b|\bMK\d{5}[0-9A-Z]{10}\d{2}\b|\bMT\d{2}[A-Z]{4}\d{5}[0-9A-Z]{18}\b|\bMR13\d{23}\b|\bMU\d{2}[A-Z]{4}\d{19}[A-Z]{3}\b|\bMC\d{12}[0-9A-Z]{11}\d{2}\b|\bME\d{20}\b|\bNL\d{2}[A-Z]{4}\d{10}\b|\bNO\d{13}\b|\bPL\d{10}[0-9A-Z]{,16}n\b|\bPT\d{23}\b|\bRO\d{2}[A-Z]{4}[0-9A-Z]{16}\b|\bSM\d{2}[A-Z]\d{10}[0-9A-Z]{12}\b|\bSA\d{4}[0-9A-Z]{18}\b|\bRS\d{20}\b|\bSK\d{22}\b|\bSI\d{17}\b|\bES\d{22}\b|\bSE\d{22}\b|\bCH\d{7}[0-9A-Z]{12}\b|\bTN59\d{20}\b|\bTR\d{7}[0-9A-Z]{17}\b|\bAE\d{21}\b|\bGB\d{2}[A-Z]{4}\d{14}\b'

    # check if country code is part of registered or partially
    # registered list and the length matches.
    # Return True if is part of list and length matches
    # Return False otherwise
    def is_registered(self, iban):
        country_code = iban[0:2]
        if (country_code in self.iban_register_by_countrycode):
            if (len(iban) != self.iban_register_by_countrycode[country_code]
                ['ndigits']):
                return False
            else:
                return True
        elif (country_code in self.iban_partial):
            if (len(iban) != self.iban_partial[country_code]['ndigits']):
                return False
            else:
                return True
        else:
            return False

    def validate_mod97(self, iban):
        # validate IBAN numbers
        # https://en.wikipedia.org/wiki/International_Bank_Account_Number
        # extract the iso3166-alpha-2 code to the end
        # the first 4 characters
        # https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
        iban2 = iban.upper()
        iso3166 = iban2[0:4]
        iban2 = iban2[4:]
        iban2 = iban2 + iso3166
        iban_all_digits = ''    # all digits
        for c in iban2:
            if c.isalpha():
                iban_all_digits += str(ord(c) - ord('A') + 10)
            else:
                iban_all_digits += c
        # compute modulo 97
        iban_no = int(iban_all_digits)
        if (iban_no % 97 != 1):
            return False
        return True

    def is_valid(self, iban):
        registered = self.is_registered(iban)
        mod97 = self.validate_mod97(iban)
        return (registered and mod97)
