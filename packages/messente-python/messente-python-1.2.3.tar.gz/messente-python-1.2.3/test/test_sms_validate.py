# -*- coding: utf-8 -*-

import unittest
import time
from messente.api import sms


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.api = sms.SmsAPI(urls="https://test-sms-validate.example.com")
        self.correct_data = {
            "to": "+37212345678",
            "text": "test",
            "time_to_send": int(time.time()) + 60,
            "validity": 10,
            "autoconvert": "full",
            "udh": "MS",
            "mclass": 1,
            "text-store": "nostore",
        }

    def test_validation_pass(self):
        (ok, errors) = self.api._validate(self.correct_data)
        self.assertTrue(ok)
        self.assertDictEqual(errors, {})

    def test_validation_errors(self):
        data = {
            "time_to_send": 123,
            "validity": -1,
            "autoconvert": "invalid",
            "udh": "invalid value",
            "mclass": 4,
            "text-store": "invalid",
        }
        (ok, errors) = self.api._validate(data)
        self.assertFalse(ok)
        self.assertIsInstance(errors, dict)

        expected = {
            "to": "Required 'to'",
            "text": "Required 'text'",
            "time_to_send": "Invalid 'time_to_send'",
            "validity": "Invalid 'validity'",
            "autoconvert": "Invalid 'autoconvert'",
            "udh": "Invalid 'udh'",
            "mclass": "Invalid 'mclass'",
            "text-store": "Invalid 'text-store'",
        }

        self.assertEqual(sorted(expected.keys()), sorted(errors.keys()))
        for field in expected:
            self.assertIn(field, errors)
            self.assertEqual(errors[field], expected[field])

    def test_required_fields(self):
        fields = ["to", "text"]
        for f in fields:
            expected = {f: "Required '%s'" % f}
            data = self.correct_data.copy()
            data.update({f: None})
            (ok, errors) = self.api._validate(data)
            self.assertFalse(ok)
            self.assertDictEqual(errors, expected)
            del data[f]
            (ok, errors) = self.api._validate(data)
            self.assertDictEqual(errors, expected)

    def test_field_values(self):
        cases = {
            "to": {
                "invalid": ["", None, {}, [], 0, "abcde"],
                "valid": ["+372123123123", "0123456-7890"],
            },
            "time_to_send": {
                "invalid": ["", "asd", {}, [], -1, 0, time.time() - 1],
                "valid": [None, time.time() + 1, time.time() + 100],
            },
            "validity": {
                "invalid": ["", "asd", {}, [], -1, 123.23],
                "valid": [None, 0, 10, 360],
            },
            "autoconvert": {
                "invalid": [{}, [], "", "invalid", 5, 6.1],
                "valid": [None, "on", "off", "full"],
            },
            "udh": {
                "invalid": [{}, [], "", "invalid", 3.14, 12, -10],
                "valid": [None, "MS", "UE"],
            },
            "mclass": {
                "invalid": [{}, [], "", "invalid", 3.14, 4, -1],
                "valid": [None, 0, 1, 2, 3],
            },
            "text-store": {
                "invalid": [{}, [], "", "invalid", 3.14, 4, -1],
                "valid": [None, "plaintext", "sha256", "nostore"],
            },
        }
        for field in cases:
            data = self.correct_data.copy()
            for item in cases[field]["invalid"]:
                data.update({field: item})
                (ok, errors) = self.api.validate(data, fatal=False)
                self.assertFalse(ok, "'%s' is invalid" % field)

            for item in cases[field]["valid"]:
                data.update({field: item})
                (ok, errors) = self.api.validate(data, fatal=False)
                self.assertTrue(ok)
                self.assertNotIn(field, errors)
