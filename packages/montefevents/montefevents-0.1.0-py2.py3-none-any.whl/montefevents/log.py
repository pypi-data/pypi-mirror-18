# -*- coding: utf-8 -*-

from __future__ import unicode_literals


__author__ = "Begon Jean-Michel <jm.begon@gmail.com>"

import sys
import logging


def get_warn_log(name=None):
    if name is None:
        name = __name__
    splits = name.split(".")
    return logging.getLogger(".".join([splits[0], "error"] + splits[1:]))

def get_info_log(name=None):
    if name is None:
        name = __name__
    splits = name.split(".")
    return logging.getLogger(".".join([splits[0], "info"] + splits[1:]))


def std_log():
    basename = __name__.split(".")[0]
    frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Warn +
    warn_log = get_warn_log(basename)
    hdlr = logging.StreamHandler(sys.stderr)
    hdlr.setFormatter(frmt)
    warn_log.addHandler(hdlr)
    warn_log.setLevel(logging.WARN)
    # Info
    info_log = get_info_log(basename)
    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setFormatter(frmt)
    info_log.addHandler(hdlr)
    info_log.setLevel(logging.INFO)


