# -*- coding: utf-8 -*-

# Copyright 2016 Messente Communications OÜ
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

import hashlib
from messente.api import api


class VerificationWidgetAPI(api.API):
    """Documentation: http://messente.com/documentation/verification-widget"""

    def __init__(self, **kwargs):
        api.API.__init__(self, "verification-widget", **kwargs)

    def calculate_signature(self, data):
        plain = "".join(map(lambda k: (k) + str(data[k]), sorted(data)))
        return hashlib.md5(plain.encode("utf8")).hexdigest()

    def verify_signature(self, signature, data):
        return (signature == self.calculate_signature(data))

    def _validate(self, data, **kwargs):
        errors = {}
        url = data.get("callback_url", None)
        if not url:
            self.set_error_required(errors, "callback_url")
        elif not isinstance(url, str):
            self.set_error(errors, "callback_url")

        version = data.get("version", None)
        if version is None or not str(version).isnumeric():
            self.set_error(errors, "version")

        return (not len(errors), errors)
