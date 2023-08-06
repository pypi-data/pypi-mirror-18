# -*- coding: utf-8 -*-

import unittest
import time
import tempfile

from messente.api import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.phone_numbers = {
            "valid": {
                "+372-1-234-5-67-89": "372123456789",
                "+372-1_234  5-6789": "372123456789",
                "++372 1-2345_67_89": "372123456789",
                "+372+1_234-5 67+89": "372123456789",
            },
            "invalid": {
                "+372+1a234-5 6789": "3721a23456789",
                "+372+[1234]-5 6789": "372[1234]56789",
                "abcde": "abcde",
                "": "",
                "żźćńóęł": "żźćńóęł",
                "!@#$%^&*()": "!@#$%^&*()",
                None: "",
            },
        }

    def test_adapt_phone(self):
        for tp in self.phone_numbers:
            for phone in self.phone_numbers[tp]:
                r = utils.adapt_phone_number(phone)
                self.assertEqual(
                    r,
                    self.phone_numbers[tp][phone],
                    "adapt: %s" % r
                )
        invalid_attrs = [True, bool, int, float]
        for attr in invalid_attrs:
            with self.assertRaises(AttributeError):
                utils.adapt_phone_number(attr)

    def test_validate_phone(self):
        for phone in self.phone_numbers["valid"]:
            phone = utils.adapt_phone_number(phone)
            self.assertTrue(
                utils.is_phone_number_valid(phone),
                "adapted is valid: %s" % phone
            )

        for phone in self.phone_numbers["invalid"]:
            self.assertFalse(
                utils.is_phone_number_valid(phone),
                "invalid: %s" % phone
            )
            phone = utils.adapt_phone_number(phone)
            self.assertFalse(
                utils.is_phone_number_valid(phone),
                "adapted is not valid: %s" % phone
            )

    def test_ge_epoch(self):
        self.assertTrue(utils.ge_epoch(time.time() + 2))
        self.assertFalse(utils.ge_epoch(time.time() - 1))

    def test_write_file(self):
        (_, filename) = tempfile.mkstemp()

        contents = ["text1", "content overwritten"]
        for c in contents:
            utils.write_file(filename, c)
            with open(filename, "r") as fh:
                self.assertEqual(fh.read(), c)

    def test_is_int(self):
        self.assertTrue(utils.is_int("123"))
        self.assertTrue(utils.is_int("0"))
        self.assertTrue(utils.is_int("-10"))

        self.assertFalse(utils.is_int("a"))
