# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from nose.tools import assert_true, assert_false, assert_raises, assert_greater
from nose.tools import assert_less_equal

from datetime import datetime, timedelta

from montefevents import Seminar, Sender, Policy
from montefevents.notification import Channel
from montefevents.data import DataSource

def _monday12():
    return datetime(2016, 12, 12, 15, 10, 00)  # Monday


class NOPChannel(Channel):

    def __init__(self, debug=False):
        self.debug = debug

    def preview(self, event, decision):
        assert_true(self.debug)

    def send(self, event, decision):
        assert_false(self.debug)

class BuggyChannel(Channel):

    def __init__(self):
        self.err_count = 0

    def preview(self, event, decision):
        self.err_count += 1
        raise ValueError("BuggyChannel")

    def send(self, event, decision):
        return self.preview(event, decision)

class PseudoDataSource(DataSource):

    def get_next_seminars(self):
        deltas = range(-10, 10)
        seminars = []
        for delta in deltas:
            seminar = Seminar("test seminar", "test speaker",
                   _monday12() + timedelta(days=delta),
                   "test location", "test contact", "test abstract")
            seminars.append(seminar)
        return seminars


def test_sender():
    sender = Sender(Policy(_monday12()), NOPChannel())
    try:
        sender(PseudoDataSource())
        assert_true(True)
    except Exception as ex:
        assert_true(False, "Got exception {}".format(repr(ex)))

def test_debug():
    sender = Sender(Policy(_monday12()), NOPChannel(True), debug=True)
    sender(PseudoDataSource())

def test_fail_fast_false():
    bc = BuggyChannel()
    sender = Sender(Policy(_monday12()), bc, fail_fast=False)
    try:
        sender(PseudoDataSource())
        assert_true(True)
    except Exception as ex:
        assert_true(False, "Got exception {}".format(repr(ex)))
    assert_greater(bc.err_count, 1)

def test_fail_fast_true():
    bc = BuggyChannel()
    sender = Sender(Policy(_monday12()), bc, fail_fast=True)
    assert_raises(Exception, sender, PseudoDataSource())
    assert_less_equal(bc.err_count, 1)





