# -*- coding: utf-8 -*-

import unittest

from test import utils

import messente
from messente.api.config import configuration
from messente.api import sms
from messente.api import delivery
from messente.api import credit
from messente.api import pricing
from messente.api.error import ConfigurationError


module_name = "test-api"
username = "%s-username" % module_name
password = "%s-password" % module_name


class TestApi(unittest.TestCase):
    def test_configuration(self):
        api = messente.api.api.API(
            username=username,
            password=password,
            config_section=module_name,
            urls=utils.TEST_URL
        )
        self.assertEqual(api.api_urls, [utils.TEST_URL])

        self.assertTrue(module_name in configuration.sections())
        self.assertEqual(api.get_str_option("username"), username)
        self.assertEqual(api.get_str_option("password"), password)

    def test_invalid_config_path(self):
        ctors = [
            credit.CreditAPI,
            delivery.DeliveryAPI,
            pricing.PricingAPI,
            sms.SmsAPI,
        ]
        for api_ctor in ctors:
            with self.assertRaises(ConfigurationError):
                api_ctor(
                    ini_path="non-existent-and-thus-invalid.ini"
                )
