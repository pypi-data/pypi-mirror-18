# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__author__ = "Begon Jean-Michel <jm.begon@gmail.com>"

from nose.tools import assert_equal, assert_true, assert_false
from nose.tools import assert_is_instance

from datetime import datetime

from montefevents import Seminar


def _basic_seminar():
    return Seminar("test seminar", "test speaker",
                   datetime(2016, 12, 6, 15, 10, 00),
                   "test location", "test contact", "test abstract")

def _tba_seminar():
    return Seminar("TBA", "test speaker",
                   datetime(2016, 12, 6, 15, 10, 00),
                   "test location", "test contact", "test abstract")


def test_create_seminar():
    try:
        _basic_seminar()
        _tba_seminar()
        assert_true(True)
    except:
        assert_true(False)

def test_repr():
    assert_is_instance(repr(_basic_seminar()), str)


def test_str():
    assert_is_instance(str(_basic_seminar()), str)

def test_dates():
    seminar = _basic_seminar()
    delta0 = datetime(2016, 12, 6, 10, 20, 00)
    delta7 = datetime(2016, 12, 13, 15, 20, 00)
    delta20 = datetime(2016, 12, 26, 15, 20, 00)
    delta_1 = datetime(2016, 12, 5, 15, 20, 00)
    assert_equal(seminar.how_many_days_before(delta0), 0)
    assert_equal(seminar.how_many_days_before(delta7), -7)
    assert_equal(seminar.how_many_days_before(delta20), -20)
    assert_equal(seminar.how_many_days_before(delta_1), +1)

def test_date_as_str():
    assert_equal(_basic_seminar().date_as_str(), 'Tuesday, December 06, 15:10')



def test_is_filled():
    sem = _basic_seminar()
    tba = _tba_seminar()
    assert_true(sem.is_filled())
    assert_false(tba.is_filled())







