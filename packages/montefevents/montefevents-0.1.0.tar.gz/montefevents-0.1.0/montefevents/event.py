# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__author__ = "Begon Jean-Michel <jm.begon@gmail.com>"


from abc import ABCMeta



class Event(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, date):
        self.name = name
        self.date = date

    def get_date(self):
        return self.date

    def get_name(self):
        return self.name

    def how_many_days_before(self, date):
        return (self.date.date() - date.date()).days

    def date_as_str(self):
        return self.date.strftime("%A, %B %d, %H:%M")

    def is_filled(self):
        return self.name.strip().lower() != "tba"



# TODO mailto / site of contact
class Seminar(Event):
    """
    A seminar event.

    Constructor parameters
    ----------------------
    name : str
        The name of the event
    speaker : str
        Speaker's name
    date : `datetime`
        The date and the hour of the event
    location : str
        The location of the event
    contact : str
        A contact name
    abstract : str
        The abstract of the seminar
    """

    def __init__(self, name, speaker, date, location, contact, abstract):
        super(self.__class__, self).__init__(name, date)
        self.speaker = speaker
        self.location = location
        self.contact = contact
        self.abstract = abstract

    def __repr__(self):
        return "{cls}('{name}', '{speaker}', {date}, " \
               "'{location}', '{contact}', " \
               "'{abstract}')".format(cls=self.__class__.__name__,
                                    name=self.name,
                                    speaker=self.speaker, date=repr(self.date),
                                    location=self.location,
                                    contact=self.contact,
                                    abstract=self.abstract)
    def __str__(self):
        return "{cls}({name}, {speaker}, {date}, " \
               "{location}, {contact}".format(cls=self.__class__.__name__,
                                                name=self.name,
                                                speaker=self.speaker,
                                                date=str(self.date),
                                                location=self.location,
                                                contact=self.contact)









