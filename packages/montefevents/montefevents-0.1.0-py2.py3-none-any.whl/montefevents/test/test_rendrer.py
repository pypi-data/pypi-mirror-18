# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__author__ = "Begon Jean-Michel <jm.begon@gmail.com>"

from nose.tools import assert_is_instance

from email.mime.text import MIMEText

from datetime import datetime

from montefevents import Seminar, Decision, SMTPRenderer

def _basic_seminar():
    return Seminar("test seminar", "test speaker",
                   datetime(2016, 12, 6, 15, 10, 00),
                   "test location", "test contact", "test abstract")


def test_smtprenderer():
    rendrer = SMTPRenderer()
    mime = rendrer(_basic_seminar(), Decision.ANNOUNCE)
    assert_is_instance(mime, MIMEText)
    mime = rendrer(_basic_seminar(), Decision.REMIND)
    assert_is_instance(mime, MIMEText)
