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


class Text:

    def __init__(self, filename):
        self.filename = filename
        try:
            self.txt_fp = open(filename, 'r', encoding='utf-8')
        except OSError as os_err:
            print(os_err)
            raise

    def __del__(self):
        if self.txt_fp is not None:
            self.txt_fp.close()

    def as_text(self):
        if self.txt_fp is not None:
            return self.txt_fp.read()
        return ''

    def content(self):
        return self.as_text()
