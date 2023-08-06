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
from messente.api.error import ConfigurationError
from messente.logging import log

from six.moves import configparser

configuration = configparser.SafeConfigParser()

configuration.add_section("api")
configuration.add_section("sms")
configuration.add_section("credit")


configuration.set("api", "test", "ASD")
configuration.set(
    "api",
    "urls",
    "https://api2.messente.com https://api3.messente.com"
)

configuration.set(
    "api", "username", os.getenv("MESSENTE_API_USERNAME", "")
)
configuration.set(
    "api", "password", os.getenv("MESSENTE_API_PASSWORD", "")
)


def load(path):
    global configuration
    log.debug("Loading configuration file: %s", path)
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        raise ConfigurationError(
            "Invalid configuration file '%s'" % path
        )

    configuration.read(path)
