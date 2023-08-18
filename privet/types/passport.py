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


class Passport:

    def __init__(self):
        self.any_passport_rex = r'\b\d{3,17}\b|\b[A-Za-z]\d{4,9}\b|\b[A-Za-z]{2,3}\d{5,9}\b|\b[A-Za-z]{4}\d{4,5}\b|\b[A-Za-z]{6}\d{3}\b|\b[A-Za-z]{2}\d{10,11}\b|\b[A-Za-z]\d{7}[A-Za-z]\b|\b[A-Za-z]\d[A-Za-z]\d{5,7}\b|\b[A-Za-z]{2}\d{5}[A-Za-z]\d\b|\b[A-Za-z]{2}\d[A-Za-z]\d{4,6}\b|\b[A-Za-z]\d{2,3}[A-Za-z]\d{4,5}\b|\b[A-Za-z]\d[A-Za-z]{2,3}\d{4,6}\b|\b[A-Za-z]{2}\d{2}[A-Za-z]\d{5}\b|\b[A-Za-z]{2}\d{3}[A-Za-z]{2}\d{2}\b|\b[A-Za-z]\d[A-Za-z]\d[A-Za-z]\d[A-Za-z]{3}\b|\b\d{7,8}[A-Za-z]\b|\b\d[A-Za-z]\d{6,7}\b|\b\d{5}[A-Za-z]{2}\b|\b\d{2}[A-Za-z]\d{6}\b|\b\d{3}[A-Za-z]\d{5,8}\b|\b\d{2,3}[A-Za-z]{2,3}\d{5,7}\b|\b\d{3}[A-Za-z]{2}\d{6}[A-Za-z]\b'
