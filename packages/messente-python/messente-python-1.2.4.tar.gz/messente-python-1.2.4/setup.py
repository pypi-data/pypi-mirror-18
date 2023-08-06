# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name="messente-python",
    version="1.2.4",
    packages=["messente", "messente.api"],
    setup_requires=["future", "six", "requests"],
    install_requires=["future", "six", "requests"],
    author="Messente.com",
    author_email="support@messente.com",
    description="Official Messente.com API library",
    license="Apache License, Version 2",
    keywords="messente sms verification 2FA pincode",
    url="http://messente.com/documentation/",
    test_suite="test",
)
