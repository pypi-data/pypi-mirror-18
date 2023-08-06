# -*- coding: utf-8 -*-

import responses

from test import utils

from messente.api import credit
from messente.api import Response
from messente.api.error import ConfigurationError


api = credit.CreditAPI(
    user="test",
    password="test",
    urls=utils.TEST_URL
)


@responses.activate
def test_invalid_credentials():
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, "ERROR 101"),
    )

    r = api.get_balance()
    assert r.status == "ERROR"
    assert r.error_code == 101
    assert r.error_msg


@responses.activate
def test_get_balance():
    value = 123.45678
    text = "OK %s" % value
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.get_balance()

    assert isinstance(r, Response)
    assert isinstance(r, credit.CreditResponse)

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "OK"
    assert r.get_raw_text() == text
    assert r.get_result() == str(value)


@responses.activate
def test_server_failure():
    value = "FAILED 209"
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, value),
    )

    r = api.get_balance()

    assert r.error_code == 209
    assert r.status == "FAILED"
    assert r.error_msg
    assert r.get_raw_text() == value
