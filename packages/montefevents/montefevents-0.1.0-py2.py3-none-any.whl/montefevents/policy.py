# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__author__ = "Begon Jean-Michel <jm.begon@gmail.com>"

from datetime import datetime


class Decision(object):
    IGNORE = "IGNORE"
    ANNOUNCE = "ANNOUNCE"
    REMIND = "REMIND"

class Policy(object):
    def __init__(self, ref_date=datetime.today()):
        self.ref_date = ref_date

    def __call__(self, event):
        if not event.is_filled():
            return Decision.IGNORE
        n_days = event.how_many_days_before(self.ref_date)
        if 0 <= n_days < 7:
            if n_days == 0:
                return Decision.REMIND
            if self.ref_date.weekday() == 0:
                return Decision.ANNOUNCE
        return Decision.IGNORE
