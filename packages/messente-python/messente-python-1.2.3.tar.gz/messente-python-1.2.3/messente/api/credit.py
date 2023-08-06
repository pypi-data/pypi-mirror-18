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

from messente.api import config
from messente.api import api
from messente.api.response import Response


class CreditResponse(Response):
    def __init__(self, *args, **kwargs):
        Response.__init__(self, *args, **kwargs)

    def get_result(self):
        if self.is_ok():
            return self.get_raw_text().split(" ")[1]
        return None


class CreditAPI(api.API):
    """
    Documentation:
    http://messente.com/documentation/tools/credits-api
    """

    def __init__(self, **kwargs):
        api.API.__init__(self, "credit", **kwargs)

    def get_balance(self):
        r = CreditResponse(self.call_api("get_balance"))
        self.log_response(r)
        return r
