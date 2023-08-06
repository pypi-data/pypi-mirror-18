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
from messente.api.error import ERROR_CODES


error_map = ERROR_CODES.copy()
error_map.update({
    "FAILED 102": " ".join([
        "No delivery report yet, try again in 5 seconds"
    ]),
})


class DeliveryResponse(Response):
    def __init__(self, *args, **kwargs):
        Response.__init__(self, *args, **kwargs)

    def _get_error_map(self):
        return error_map

    def get_result(self):
        return self.status_text


class DeliveryAPI(api.API):
    """
    Documentation:
    http://messente.com/documentation/sms-messaging/delivery-report
    """

    def __init__(self, **kwargs):
        api.API.__init__(self, "delivery", **kwargs)

    def get_dlr_response(self, sms_id):
        r = DeliveryResponse(
            self.call_api("get_dlr_response", dict(sms_unique_id=sms_id))
        )
        self.log_response(r)
        return r

    def get_report(self, sms_id):
        return self.get_dlr_response(sms_id)
