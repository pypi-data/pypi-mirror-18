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

import os
from messente import api


class Messente(object):
    def __init__(self, **kwargs):
        if kwargs.get("ini_path", ""):
            api.config.load(kwargs.pop("ini_path"))
        # modules
        self.sms = api.sms.SmsAPI(**kwargs)
        self.credit = api.credit.CreditAPI(**kwargs)
        self.delivery = api.delivery.DeliveryAPI(**kwargs)
        self.pricing = api.pricing.PricingAPI(**kwargs)
        self.number_verification = (
            api.number_verification.NumberVerificationAPI(**kwargs)
        )
        self.verification_widget = (
            api.verification_widget.VerificationWidgetAPI(**kwargs)
        )
