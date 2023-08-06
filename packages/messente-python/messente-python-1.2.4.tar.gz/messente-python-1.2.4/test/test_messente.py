# -*- coding: utf-8 -*-

import unittest
import messente


class TestMessenteLibrary(unittest.TestCase):
    def test_invalid_config_path(self):
        with self.assertRaises(messente.api.error.ConfigurationError):
            messente.Messente(
                ini_path="invalid-path.ini",
                urls="https://test-messente.example.com"
            )

    def test_modules_init(self):
        api = messente.Messente(urls="https://test.example.com")
        self.assertIsInstance(api.sms, messente.api.sms.SmsAPI)
        self.assertIsInstance(api.credit, messente.api.credit.CreditAPI)
        self.assertIsInstance(api.delivery, messente.api.delivery.DeliveryAPI)
        self.assertIsInstance(api.pricing, messente.api.pricing.PricingAPI)
        apis = [api.sms, api.credit, api.delivery, api.pricing]
        for item in apis:
            self.assertIsInstance(item, messente.api.api.API)
        del api

    def test_error_messages(self):
        codes = messente.api.error.ERROR_CODES
        self.assertGreater(len(codes), 0)
        for c in codes:
            self.assertGreater(len(codes[c]), 0)
