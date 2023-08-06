# -*- coding: utf-8 -*-

import unittest
import time
from messente.api import number_verification


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.api = number_verification.NumberVerificationAPI(
            urls="https://test-sms-validate.example.com"
        )
        self.correct_data = {
            "pin": 1234,
            "verification_id": "2345test"
        }

    def test_validation_pass(self):
        (ok, errors) = self.api._validate(
            self.correct_data,
            mode="verify_pin"
        )
        self.assertTrue(ok)
        self.assertDictEqual(errors, {})

    def test_validation_errors(self):
        data = {
            "pin": "",
            "verification_id": "",
        }
        (ok, errors) = self.api._validate(data, mode="verify_pin")
        self.assertFalse(ok)
        self.assertIsInstance(errors, dict)

    def test_required_fields(self):
        fields = ["pin", "verification_id"]
        for f in fields:
            expected = {f: "Required '%s'" % f}
            data = self.correct_data.copy()
            data.update({f: None})
            (ok, errors) = self.api._validate(data, mode="verify_pin")
            self.assertFalse(ok)
            self.assertDictEqual(errors, expected)
            del data[f]
            (ok, errors) = self.api._validate(data, mode="verify_pin")
            self.assertDictEqual(errors, expected)

    def test_field_values(self):
        cases = {
            "pin": {
                "invalid": [None, "", "test", {}, [], 0, -10, True, False],
                "valid": ["1234", 1234123],
            },
            "verification_id": {
                "invalid": [None, "", -1, 0, 3.14, 100, True, False],
                "valid": ["test", "123", "kjahfdlakjhfdlkajmhfd"],
            },
        }
        for field in cases:
            data = self.correct_data.copy()
            for item in cases[field]["invalid"]:
                data.update({field: item})
                (ok, errors) = self.api._validate(data, mode="verify_pin")
                self.assertFalse(ok, "'%s' is invalid" % field)

            for item in cases[field]["valid"]:
                data.update({field: item})
                (ok, errors) = self.api._validate(data, mode="verify_pin")
                self.assertTrue(ok)
                self.assertNotIn(field, errors)
