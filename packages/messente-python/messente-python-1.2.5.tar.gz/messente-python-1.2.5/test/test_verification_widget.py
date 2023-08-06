# -*- coding: utf-8 -*-

import unittest
import hashlib
from messente.api import verification_widget


def test_calculate_signature():
    user = "test"
    password = "test12"
    api = verification_widget.VerificationWidgetAPI(
        username=user,
        password=password,
    )
    data = dict(
        user=user,
        callback_url="http://test.com",
        version=1,
        phone="+372123456789",
        password=password
    )
    plain = "".join(map(lambda k: (k) + str(data[k]), sorted(data)))
    s = (
        "callback_urlhttp://test.compasswordtest12"
        "phone+372123456789usertestversion1"
    )
    expected_md5sum = hashlib.md5(s.encode("utf-8")).hexdigest()
    md5sum = api.calculate_signature(data)
    assert plain == s
    assert md5sum == expected_md5sum
    assert api.verify_signature(md5sum, data)
    assert not api.verify_signature("invalid", data)


def test_validate():
    api = verification_widget.VerificationWidgetAPI()
    (ok, errors) = api._validate({})
    assert not ok
    assert "callback_url" in errors
    assert errors["callback_url"]
    assert "version" in errors
    assert errors["version"]
