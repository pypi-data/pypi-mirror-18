# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__author__ = "Begon Jean-Michel <jm.begon@gmail.com>"



from datetime import datetime
try:
    # Python 2
    from urllib2 import URLError, HTTPError
    from urllib2 import urlopen
except ImportError:
    # Python 3+
    from urllib.error import URLError, HTTPError
    from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from abc import ABCMeta, abstractmethod
import re
try:
    # Python 2
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser

from .event import Seminar
from .log import get_warn_log



__BASE_URL__ = "http://www.montefiore.ulg.ac.be"
__SEMINAR_SUFFIX__ = "/seminars"



class JSONParser(object):

    def _parse_date(self, date_as_text):
        return datetime.strptime(date_as_text, "%B %d, %Y (%A) %H:%M")

    def _remove_duplicate_eol(self, abstract):
        tmp = re.sub("( *(\r\n)+ *)+", "\r\n", abstract)
        return tmp.replace("\r\n", "\r\n\r\n")

    def _parse_contact(self, contact):
        return contact.replace("\\", "")

    def _html2str(self, dictionary):
        parser = HTMLParser()
        return {k:parser.unescape(v) for k,v in dictionary.items()}


    def __call__(self, jdict):
        if 'Seminar' not in jdict:
            get_warn_log(__name__).warn("Not a seminar: %s"%str(jdict))
        jdict = self._html2str(jdict)
        # Parse date
        date = self._parse_date(jdict["Time"])
        # Remove duplicate end of lines
        abstract = self._remove_duplicate_eol(jdict["Abstract"])
        # Parse contact
        contact = self._parse_contact(jdict["Contact"])
        return Seminar(name=jdict["Seminar"], speaker=jdict["Speaker"],
                       date=date, location=jdict["Location"],
                       contact=contact, abstract=abstract)




class DataSource(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_next_seminars(self):
        pass


    def __iter__(self):
        return iter(self.get_next_seminars())





class MontefioreGetter(DataSource):

    def __init__(self, parser=JSONParser(), base_url=__BASE_URL__,
                 seminar_suffix=__SEMINAR_SUFFIX__, fail_fast=False):
        self.base_url = base_url
        self.seminar_suffix = seminar_suffix
        self.parser = parser
        self.fail_fast = fail_fast


    def _get_link_list(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        title_div = [x for x in soup.find_all("div")
                        if x.has_attr("seminar-title")]
        links = [x.find("a") for x in title_div]
        return [x.attrs["href"] for x in links if x is not None and
                            x.has_attr("href")]

    def _get_json(self, link):
        try:
            return json.loads(urlopen(self.base_url+link+"?json").read())
        except Exception as e:
            if self.fail_fast:
                raise
            errcls = e.__class__.__name__
            reason = e.message
            get_warn_log().warn("Could not load json at {link}. "
                "The reason is: {reason} ({errcls})".format(link=link,
                                                            reason=reason,
                                                            errcls=errcls))
            return None

    def _parse(self, jdict):
        try:
            return self.parser(jdict)
        except Exception as ex:
            if self.fail_fast:
                raise
            errcls = ex.__class__.__name__
            get_warn_log().warn("Could not parse event {jdict}. "
                "The reason is: {reason} ({errcls})".format(jdict=unicode(jdict),
                                                            reason=ex.message,
                                                            errcls=errcls))
            return None


    def get_next_seminars(self):
        url = self.base_url+self.seminar_suffix
        # No need to close: http://stackoverflow.com/questions/1522636/should-i-call-close-after-urllib-urlopen
        # No need to catch exception. In this case the program should crash
        page = urlopen(url).read()
        links = self._get_link_list(page)
        jsons = [self._get_json(link) for link in links]
        seminars = [self._parse(jdict) for jdict in jsons if jdict is not None]
        return [x for x in seminars if x is not None]




