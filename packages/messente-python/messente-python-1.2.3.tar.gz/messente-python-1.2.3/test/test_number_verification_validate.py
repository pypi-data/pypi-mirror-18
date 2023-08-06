# -*- coding: utf-8 -*-

import unittest
import time
from messente.api import number_verification


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.api = number_verification.NumberVerificationAPI(
            urls="https://test.example.com"
        )

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
        (ok, errors) = self.api._validate(
            self.correct_data,
            mode="send_pin"
        )
        self.assertTrue(ok)
        self.assertDictEqual(errors, {})

    def test_validation_errors(self):
        data = {
            "template": "test",
            "max_tries": "abc",
            "retry_delay": "xxx",
            "validity": "zzz",
        }
        (ok, errors) = self.api._validate(data, mode="send_pin")
        self.assertFalse(ok)
        self.assertIsInstance(errors, dict)

        expected = {
            "to": "Required 'to'",
            "template": "Invalid 'template'",
            "max_tries": "Invalid 'max_tries'",
            "retry_delay": "Invalid 'retry_delay'",
            "validity": "Invalid 'validity'",
        }

        self.assertEqual(sorted(expected.keys()), sorted(errors.keys()))
        for field in expected:
            self.assertIn(field, errors)
            self.assertEqual(errors[field], expected[field])

    def test_required_fields(self):
        fields = ["to"]
        for f in fields:
            expected = {f: "Required '%s'" % f}
            data = self.correct_data.copy()
            data.update({f: None})
            (ok, errors) = self.api._validate(data, mode="send_pin")
            self.assertFalse(ok)
            self.assertDictEqual(errors, expected)
            del data[f]
            (ok, errors) = self.api._validate(data, mode="send_pin")
            self.assertDictEqual(errors, expected)

    def test_field_values(self):
        cases = {
            "to": {
                "invalid": [
                    "", None, {}, [], 0, "abc",
                    "+3721234567a1231",
                    "+3721234567890123",
                    "+372-123-456-789-0123",
                ],
                "valid": [
                    "+3721234567890",
                    " + 372 123 234 345 ",
                    "12345678912345",
                    "+12345678912345-",
                    "+-372-123-456 789 123",
                ],
            },
            "template": {
                "invalid": ["", "missing <pin> upper", -1, 3.14, True, False],
                "valid": [None, "Test <PIN>"],
            },
            "max_tries": {
                "invalid": ["", "asd", -1, 0, True, False],
                "valid": [None, 2, 100],
            },
            "retry_delay": {
                "invalid": ["", "asd", -1, True, False],
                "valid": [None, 2, 100],
            },
            "validity": {
                "invalid": ["", "asd", -1, 3.14, 1801, True, False],
                "valid": [None, 0, 100, 1800],
            },
        }
        for field in cases:
            data = self.correct_data.copy()
            for item in cases[field]["invalid"]:
                data.update({field: item})
                (ok, errors) = self.api.validate(
                    data, mode="send_pin", fatal=False
                )
                self.assertFalse(ok, "'%s' is invalid" % field)

            for item in cases[field]["valid"]:
                data.update({field: item})
                (ok, errors) = self.api.validate(
                    data, mode="send_pin", fatal=False
                )
                self.assertTrue(ok)
                self.assertNotIn(field, errors)
