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
import requests

from messente.logging import Logger
from messente.api import config
from messente.api.error import ConfigurationError
from messente.api.error import InvalidMessageError
from messente.constants import VERSION


class API(Logger):
    """Base class for Messente apis."""

    def __init__(self, config_section, **kwargs):
        self._config_section = config_section
        for section in ["api", self._config_section]:
            if not config.configuration.has_section(section):
                config.configuration.add_section(section)

        if kwargs.get("ini_path", ""):
            config.load(kwargs.pop("ini_path"))

        self._config_getters = {
            str: config.configuration.get,
            int: config.configuration.getint,
            bool: config.configuration.getboolean,
        }

        params = dict()

        for p in params:
            params[p] = kwargs.pop(p, self.get_option(p, data_type=params[p]))

        Logger.__init__(self, **params)

        env_overrides = {
            "username": "MESSENTE_API_USERNAME",
            "password": "MESSENTE_API_PASSWORD",
        }

        for option in env_overrides:
            value = kwargs.pop(option, os.getenv(env_overrides[option], ""))
            if value:
                config.configuration.set(self._config_section, option, value)
        self.api_urls = []
        self.set_urls(kwargs.pop("urls", None))

    def set_urls(self, urls=None):
        if not urls:
            urls = self.get_option("urls", "")
        if not urls:
            raise Exception()
        if type(urls) not in [list, tuple]:
            urls = urls.split(" ")
        self.api_urls = [url.strip() for url in urls]

    def call_api(self, endpoint, data=None, **kwargs):
        data = (data or {})
        method = kwargs.pop("method", "GET")
        custom_api_url = kwargs.pop("api_url", None)
        api_urls = []
        if custom_api_url:
            api_urls.append(custom_api_url)
        else:
            api_urls.extend(self.api_urls)
        if not api_urls:
            raise ConfigurationError("No urls configured")

        # first url that yields any response makes the function return
        for url in api_urls:
            url = "{url}/{endpoint}".format(url=url, endpoint=endpoint)
            data.update(dict(
                username=self.get_option("username"),
                password="[redacted]",
            ))

            self.log.info("%s: %s", method, url)
            self.log.debug("%s", data)

            data.update(dict(password=self.get_option("password")))

            headers = {
                "User-Agent": "messente-python/%s" % str(VERSION)
            }

            try:
                r = None
                method = method.upper()
                if method == "GET":
                    r = requests.get(
                        url,
                        params=data,
                        headers=headers,
                        allow_redirects=True
                    )
                elif method == "POST":
                    r = requests.post(
                        url,
                        params=data,
                        headers=headers,
                        allow_redirects=True
                    )
                return r
            except Exception as e:
                self.log.exception(e)
        self.log.error("No more urls to try. Giving up.")
        return None

    def get_option(self, option, default=None, **kwargs):
        data_type = kwargs.pop("data_type", str)
        fallback_section = kwargs.pop("fallback_section", "api")
        cfg = config.configuration
        if cfg.has_option(self._config_section, option):
            section = self._config_section
        elif cfg.has_option(fallback_section, option):
            section = fallback_section
        else:
            raise ConfigurationError("No such option: %s" % option)
        value = self._config_getters[data_type](section, option)
        return value

    def get_str_option(self, *args, **kwargs):
        return self.get_option(*args, **kwargs)

    def get_int_option(self, *args, **kwargs):
        return self.get_option(*args, data_type=int, **kwargs)

    def get_bool_option(self, *args, **kwargs):
        return self.get_option(*args, data_type=bool, **kwargs)

    def log_response(self, r):
        if not r.is_replied():
            self.log.critical("No response")
        elif not r.is_ok():
            self.log.error(r.get_full_error_msg())
        else:
            self.log.debug(r.get_raw_text())

    def validate(self, data, **kwargs):
        (ok, errors) = self._validate(data, **kwargs)
        if not ok:
            for field in errors:
                self.log.error("%s: %s", field, errors[field])
            if kwargs.get("fatal", False):
                raise InvalidMessageError("Message is invalid")
        return (ok, errors)

    def _validate(self, data, **kwargs):
        return (True, {})

    def set_error(self, errors, field, msg=None):
        errors[field] = (msg or "Invalid '%s'" % field)

    def set_error_required(self, errors, field, msg=None):
        errors[field] = (msg or "Required '%s'" % field)

    def adapt(self, data):
        return data
