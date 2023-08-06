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


from messente.api import api
from messente.api import utils
from messente.api.response import Response
from messente.api.error import ERROR_CODES


error_map = ERROR_CODES.copy()

error_map.update({
    "ERROR 109": "PIN code field is missing in the template value.",
    "ERROR 110": "Verification Session with following ID was not found.",
    "ERROR 111": " ".join([
        "Sender parameter 'from' is invalid."
        "You have not activated this sender name from Messente.com"
    ]),
})


class NumberVerificationResponse(Response):
    _VERIFIED = "VERIFIED"
    _INVALID = "INVALID"
    _EXPIRED = "EXPIRED"
    _THROTTLED = "THROTTLED"

    def __init__(self, *args, **kwargs):
        self._verification_id = kwargs.pop("verification_id", "")
        Response.__init__(self, *args, **kwargs)

    def _get_error_map(self):
        return error_map

    def _parse(self):
        custom_statuses = [
            self._VERIFIED, self._INVALID, self._EXPIRED, self._THROTTLED
        ]
        stripped = self.raw_response.text.strip()
        if stripped in custom_statuses:
            self.status = stripped
        else:
            Response._parse(self)
            self._verification_id = self.status_text

    def is_ok(self):
        return (
            self.is_replied() and
            self.status in ["OK", self._VERIFIED]
        )

    def get_verification_id(self):
        return self._verification_id

    def is_verified(self):
        return (self.status == self._VERIFIED)

    def is_invalid(self):
        return (self.status == self._INVALID)

    def is_expired(self):
        return (self.status == self._EXPIRED)

    def is_throttled(self):
        return (self.status == self._THROTTLED)


class NumberVerificationAPI(api.API):
    """
    Api supporting PIN code based user verification.

    Documentation:
    http://messente.com/documentation/number-verification/number-verification-api

    """
    def __init__(self, **kwargs):
        api.API.__init__(self, "number-verification", **kwargs)

    def send_pin(self, data, **kwargs):
        self.adapt(data)
        if kwargs.get("validate", True):
            self.validate(data, mode="send_pin", fatal=True)
        r = NumberVerificationResponse(
            self.call_api(
                "verify/start",
                data
            ),
        )
        self.log_response(r)
        return r

    def verify_pin(self, data, **kwargs):
        if kwargs.pop("validate", True):
            self.validate(data, mode="verify_pin", fatal=True)
        r = NumberVerificationResponse(
            self.call_api(
                "verify/pin",
                data
            )
        )
        self.log_response(r)
        return r

    def adapt(self, data):
        data["to"] = utils.adapt_phone_number(data.get("to", ""))
        return data

    def _validate(self, data, **kwargs):
        self.adapt(data)
        errors = {}

        if kwargs.get("mode", "") == "send_pin":
            to = data.get("to", "")
            if not to:
                self.set_error_required(errors, "to")
            elif not utils.is_phone_number_valid(to):
                self.set_error(errors, "to")

            template = data.get("template", None)
            if template is not None and "<PIN>" not in str(template):
                self.set_error(errors, "template")

            max_tries = data.get("max_tries", None)
            if max_tries is not None:
                if not str(data["max_tries"]).isdigit() or max_tries < 1:
                    self.set_error(errors, "max_tries")

            retry_delay = data.get("retry_delay", None)
            if retry_delay is not None and not str(retry_delay).isdigit():
                    self.set_error(errors, "retry_delay")

            validity = data.get("validity", None)
            if validity is not None:
                is_positive_int = str(data["validity"]).isdigit()
                if not is_positive_int or validity > 1800:
                    self.set_error(errors, "validity")
        elif kwargs.get("mode", "") == "verify_pin":
            pin = data.get("pin", "")
            if not pin:
                self.set_error_required(errors, "pin")
            else:
                if not str(pin).isdigit() or not int(pin):
                    self.set_error(errors, "pin")

            verification_id = data.get("verification_id", None)
            if not verification_id:
                self.set_error_required(errors, "verification_id")
            elif not isinstance(verification_id, str):
                    self.set_error(errors, "verification_id")
        return (not len(errors), errors)
