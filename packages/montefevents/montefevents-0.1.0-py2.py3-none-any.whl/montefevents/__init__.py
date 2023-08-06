# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
The goal of this package is to provide automatic (email) notification of the
Montefiore unit's seminars.

Classes
=======
The package is organized around several classes. The main ones are:

`Seminar`
---------
The data structure representing a seminar.

`DataSource`
------------
A source from which the events can be gathered.

`Policy`
--------
The class responsible for deciding whether to notify of a given `Event`.

`Sender`
--------
The class which implements the overall logic: gathering, sorting and sending.

`Channel`
---------
The channel through which the notification will be sent.

`Renderer`
----------
A class which transform the event into the apropriate form to be able to go
through the channel.


Logging
=======
Normal information and warning/errors are subject to different loggers so that
they could be dispatched indenpendently.
Namely, information are logger of the form `basename.info*` whereas warning
are handled by logger of the form `basename.error`. The `log` module offers
two methods to handle the names. Respectively, `get_info_log` and `get_warn_log`.
This module also exposed `std_log` which redirect errrors to stderr and info
to stdout.
"""


__author__ = "Begon Jean-Michel <jm.begon@gmail.com>"
__version__ = '0.1.0'



from .event import Event, Seminar
from .policy import Decision, Policy
from .notification import Sender, SMTPChannel
from .data import MontefioreGetter
from .renderer import SMTPRenderer
from .log import get_warn_log, get_info_log, std_log


__all__ = ["Event", "Seminar", "Decision", "Policy", "Sender", "SMTPChannel",
           "MontefioreGetter", "SMTPRenderer", "get_warn_log", "get_info_log",
           "std_log"]

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


