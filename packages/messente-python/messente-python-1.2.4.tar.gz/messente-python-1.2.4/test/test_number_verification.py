# -*- coding: utf-8 -*-

import responses

from test import utils

from messente.api import number_verification
from messente.api import Response
from messente.api.error import ConfigurationError


api = number_verification.NumberVerificationAPI(
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

    r = api.send_pin({}, validate=False)
    assert r.status == "ERROR"
    assert r.error_code == 101
    assert r.error_msg


@responses.activate
def test_server_failure():
    text = "FAILED 209"
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.send_pin(dict(to="+37212345678"))

    assert isinstance(r, Response)
    assert isinstance(r, number_verification.NumberVerificationResponse)

    assert r.error_code == 209
    assert r.error_msg
    assert r.status == "FAILED"
    assert r.get_raw_text() == text
    assert r.get_result() == text
    assert r.get_verification_id() == ""
    assert not r.is_verified()


@responses.activate
def test_send_pin():
    verification_id = "vid00000001111111"
    text = "OK %s" % verification_id
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.send_pin(dict(to="+37212345678"))

    assert isinstance(r, Response)
    assert isinstance(r, number_verification.NumberVerificationResponse)

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "OK"
    assert r.get_raw_text() == text
    assert r.get_result() == text
    assert r.get_verification_id() == verification_id
    assert not r.is_verified()


@responses.activate
def test_verify_verified():
    text = "VERIFIED"
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.send_pin(dict(to="+37212345678"))

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "VERIFIED"
    assert r.get_raw_text() == text
    assert r.get_verification_id() == ""
    assert r.is_verified()

    v_id = "qwerty"
    r = api.verify_pin(dict(pin="1234", verification_id=v_id))

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "VERIFIED"
    assert r.get_raw_text() == text
    assert r.get_verification_id() == ""
    assert not r.is_throttled()
    assert not r.is_expired()
    assert not r.is_invalid()
    assert r.is_verified()


@responses.activate
def test_verify_invalid():
    text = "INVALID"
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    v_id = "qwerty"
    r = api.verify_pin(dict(pin="1234", verification_id=v_id))

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "INVALID"
    assert r.get_raw_text() == text
    assert r.get_verification_id() == ""
    assert not r.is_verified()
    assert not r.is_throttled()
    assert not r.is_expired()
    assert r.is_invalid()


@responses.activate
def test_verify_expired():
    text = "EXPIRED"
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    v_id = "qwerty"
    r = api.verify_pin(dict(pin="1234", verification_id=v_id))

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "EXPIRED"
    assert r.get_raw_text() == text
    assert r.get_verification_id() == ""
    assert not r.is_verified()
    assert not r.is_throttled()
    assert not r.is_invalid()
    assert r.is_expired()


@responses.activate
def test_verify_throttled():
    text = "THROTTLED"
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    v_id = "qwerty"
    r = api.verify_pin(dict(pin="1234", verification_id=v_id))

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "THROTTLED"
    assert r.get_raw_text() == text
    assert r.get_verification_id() == ""
    assert not r.is_verified()
    assert not r.is_invalid()
    assert not r.is_expired()
    assert r.is_throttled()


@responses.activate
def test_verify_pin_error():
    text = "ERROR 110"
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    v_id = "qwerty"
    r = api.verify_pin(dict(pin="1234", verification_id=v_id))

    assert r.error_code == 110
    assert r.error_msg
    assert r.status == "ERROR"
    assert r.get_raw_text() == text
    assert r.get_verification_id() == ""
    assert not r.is_verified()
    assert not r.is_invalid()
    assert not r.is_expired()
    assert not r.is_throttled()
