# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

__author__ = "Begon Jean-Michel <jm.begon@gmail.com>"


from abc import ABCMeta, abstractmethod
from email.mime.text import MIMEText

from .policy import Decision


__CORE__ = """{header}
________________________________________________________________________________
{core}
________________________________________________________________________________

Looking forward to your active participation,

Regards,

The Montefiore Institute event organizers
"""

__HEADER_ANNOUNCE__ = """You are cordially invited to the following event organized by the Montefiore Institute.
More details can be found at http://www.montefiore.ulg.ac.be/seminars."""

__HEADER_REMIND__ = """A gentle reminder. More details can be found at http://www.montefiore.ulg.ac.be/seminars."""





class Renderer(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def preview(self, event, decision):
        pass

    @abstractmethod
    def render(self, event, decision):
        pass
    def __call__(self, event, decision):
        return self.render(event, decision)

class SMTPRenderer(Renderer):

    def _render_core(self, event):
        abstract = ""
        if len(event.abstract) > 50:
            abstract = "Abstract:\n{abstract}".format(abstract=event.abstract)
        return """Seminar: {title}

Speaker: {speaker}

Time: {time}

Location: {location}

Contact: {contact}

{abstract}""".format(title=event.name, speaker=event.speaker,
                     time=event.date_as_str(), location=event.location,
                     contact=event.contact, abstract=abstract)



    def _raw_render_announce(self, event):
        subject = "[All-montef] Seminar: {}".format(event.name)
        header = __HEADER_ANNOUNCE__
        core  = __CORE__.format(core=self._render_core(event), header=header)
        return subject, core

    def _raw_render_reminder(self, event):
        subject = "[All-montef] Reminder - Seminar: {}".format(event.name)
        header = __HEADER_REMIND__
        core  = __CORE__.format(core=self._render_core(event), header=header)
        return subject, core

    def get_raw(self, event, decision):
        if decision == Decision.ANNOUNCE:
            return self._raw_render_announce(event)
        if decision == Decision.REMIND:
            return self._raw_render_reminder(event)

    def render(self, event, decision):
        subject, content = self.get_raw(event, decision)
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = subject
        return msg


    def preview(self, event, decision):
        subject, content = self.get_raw(event, decision)
        print(subject)
        print("")
        print(content)
        print("")
        print("")


