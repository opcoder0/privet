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

argentina_kw = [
    'Argentina National Identity number', 'cedula', 'cédula', 'dni',
    'documento nacional de identidad', 'documento número', 'documento numero',
    'registro nacional de las personas', 'rnp'
]


class NationalID:

    def __init__(self):
        self.argentina_regexp = r'[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}'
        self.national_id = {'Argentina': (self.argentina_regexp, argentina_kw)}

    def get(self, country):
        return self.national_id.get(country, (None, None))
