# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

__author__ = "Begon Jean-Michel <jm.begon@gmail.com>"


from abc import ABCMeta, abstractmethod
import smtplib

from .policy import Decision
from .renderer import SMTPRenderer
from .log import get_warn_log, get_info_log


class Connection(object):
    """
    Note: coupling with the `with` statement, the connection object will
    be garbagged after the `with`
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def send(self, event):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass


    def __del__(self):
        self.close()



class SMTPConnection(Connection):

    def __init__(self, rendrer, smtp_serv, to_addrs, from_addr, port=25):
        self.rendrer = rendrer
        self.host = smtp_serv
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.port = port
        self.conn = None

    def open(self):
        return self # Lazy open, will be done at send time

    def _open(self):
        self.conn = smtplib.SMTP(self.host, self.port)

    def close(self):
        if self.conn is not None:
            self.conn.quit()
        self.conn = None


    def send(self, event, decision):
        # Build email message
        msg = self.rendrer(event, decision)
        msg['From'] = self.from_addr
        msg['To'] = ", ".join(self.to_addrs)
        # Connect and send
        self._open()
        self.conn.sendmail(self.from_addr, self.to_addrs, msg.as_string())


class SMTPAuthConnection(SMTPConnection):

    def __init__(self, rendrer, smtp_serv, to_addrs, from_addr, username,
                 password, port=465):
        super(self.__class__, self).__init__(rendrer, smtp_serv, to_addrs,
                                             from_addr, port=port)
        self.username = username
        self.password = password

    def _open(self):
        self.conn = smtplib.SMTP(self.host, self.port)
        self.conn.starttls()
        self.conn.login(self.username, self.password)




class Channel(object):
    __metaclass__ = ABCMeta


    def __enter__(self):
        """
        Return an object with a `send` method
        """
        return self

    def __exit__(self, type, value, traceback):
        pass

    @abstractmethod
    def preview(self, event, decision):
        pass


class SMTPChannel(Channel):
    def __init__(self, renderer, smtp_serv, to_addrs, from_addr, username=None,
                 password=None, port=None):
        if not isinstance(renderer, SMTPRenderer):
            raise AttributeError("Renderer must be an instance of class '{}'. "
                                 "Given '{}".format(SMTPRenderer.__name__,
                                                    renderer.__class__.__name__))
        if username is None:
            username = from_addr
        if port is None:
            port = 25 if password is None else 465
        self.renderer = renderer
        self.smtp_serv = smtp_serv
        self.to_addrs = to_addrs
        self.from_addr = from_addr
        self.username = username
        self.password = password
        self.port = port

    def __enter__(self):
        if self.password is None:
            conn = SMTPConnection(self.renderer, self.smtp_serv, self.to_addrs,
                                  self.from_addr, port=self.port)
        else:
            conn = SMTPAuthConnection(self.renderer, self.smtp_serv,
                                      self.to_addrs, self.from_addr,
                                      self.username, self.password,
                                      port=self.port)
        conn.open()
        return conn

    def preview(self, event, decision):
        print("> FROM: ", self.from_addr)
        print("> TO:", ", ".join(self.to_addrs))
        print("> BY:", self.smtp_serv,":", self.port)
        if self.password is not None:
            print("> AUTH:", self.username)
        print("> CONTENT")
        self.renderer.preview(event, decision)





class Sender(object):

    def __init__(self, policy, channel, fail_fast=False,
                 debug=False):
        self.policy = policy
        self.channel = channel
        self.fail_fast = fail_fast
        self.debug = debug

    def __call__(self, datasource):
        warn_log = get_warn_log(__name__)
        info_log = get_info_log(__name__)
        for event in datasource:
            decision = self.policy(event)
            if decision == Decision.IGNORE:
                continue

            if self.debug:
                self.channel.preview(event, decision)
                continue

            try:
                with self.channel as connection:
                    connection.send(event, decision)
                    info_log.info("Event {} sent".format(event.name))

            except Exception as ex:
                if self.fail_fast:
                    raise
                warn_log.error("Could not send event {event}: "
                  "got exception {error}".format(event=event, error=repr(ex)))



