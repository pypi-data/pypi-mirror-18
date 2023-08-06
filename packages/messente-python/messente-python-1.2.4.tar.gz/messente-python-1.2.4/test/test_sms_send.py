# -*- coding: utf-8 -*-

import responses

from test import utils

from messente.api import sms
from messente.api import Response
from messente.api.error import ConfigurationError
from messente.api.error import InvalidMessageError


def mk_sms_data(data=None):
    sms_data = {
        "to": "+372123456789",
        "text": "test"
    }
    sms_data.update(data or {})
    return sms_data


@responses.activate
def test_invalid_credentials():
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, "ERROR 101"),
    )

    api = sms.SmsAPI(urls=utils.TEST_URL)
    r = api.send(mk_sms_data(), validate=False)
    assert isinstance(r, Response)
    assert isinstance(r, sms.SmsResponse)
    assert r.status == "ERROR"
    assert r.error_code == 101
    assert r.error_msg


@responses.activate
def test_send():
    sms_id = "sms-001"
    text = "OK %s" % sms_id
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    api = sms.SmsAPI(urls=utils.TEST_URL)
    r = api.send(mk_sms_data())

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "OK"
    assert r.get_raw_text() == text
    assert r.get_sms_id() == sms_id


def test_send_invalid():
    api = sms.SmsAPI(urls=utils.TEST_URL)
    raised = False
    try:
        r = api.send({})
    except InvalidMessageError:
        raised = True
    assert raised


@responses.activate
def test_send_no_validate():
    sms_id = "sms-001"
    text = "OK %s" % sms_id
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    api = sms.SmsAPI(urls=utils.TEST_URL)
    r = api.send({}, validate=False)
    # OK if no exception was raised
    assert True


@responses.activate
def test_cancel():
    text = "OK DELETED"
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    api = sms.SmsAPI(urls=utils.TEST_URL)
    r = api.cancel("sms-id")

    assert isinstance(r, Response)
    assert isinstance(r, sms.CancelSmsResponse)

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "OK"
    assert r.get_raw_text() == text
    assert r.get_result() == text
