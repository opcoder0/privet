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

aws_access_kw = [
    'secret', 'key', 'aws access key id', 'access key id', 'access key',
    'aws secret access key'
]


class CloudKeys:

    def __init__(self):
        # References
        # https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html
        # https://summitroute.com/blog/2018/06/20/aws_security_credential_formats/
        # https://docs.aws.amazon.com/STS/latest/APIReference/API_Credentials.html
        self.access_key_id_regexp = r'(ABIA|ACCA|AGPA|AIDA|AIPA|AKIA|ANPA|ANVA|APKA|AROA|ASCA|ASIA)[A-Z0-9]{16,128}'
        self.secret_access_key_regexp = r'[A-Za-z0-9\/+]{40}'
        self.cloud_keys = {
            'aws_access_key_id': (self.access_key_id_regexp, aws_access_kw),
            'aws_secret_key': (self.secret_access_key_regexp, aws_access_kw)
        }

    def get(key):
        return self.cloud_keys.get(key, (None, None))
