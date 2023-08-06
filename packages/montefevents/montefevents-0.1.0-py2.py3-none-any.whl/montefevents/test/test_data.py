# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = "Begon Jean-Michel <jm.begon@gmail.com>"


from nose.tools import assert_equal, assert_true

from datetime import datetime
import os


from montefevents import MontefioreGetter
from montefevents.data import JSONParser

#TODO More parsing case


jdict1 = {"Seminar":"Chance-Constrained Convex Mixed-Integer Programs and Beyond","Speaker":"Jesus De Loera (UC Davis)","Time":"December 09, 2016 (Friday) 05:00","Location":"Room R7, Montefiore Institute (B28)","Contact":"Quentin Louveaux (http:\/\/www.montefiore.ulg.ac.be\/~louveaux\/)","Abstract":"Chance-constrained convex mixed integer optimization, a branch of stochastic optimization, concerns convex mixed-integer programming problems in which constraints are imprecisely known but the problems need to be solved with a minimum probability of reliability or certainty. Such problems arise quite naturally in many areas of finance (e.g., portfolio planning where losses should not exceed some risk threshold), telecommunication (services agreements where contracts require network providers to guarantee with high probability that packet losses will not exceed a certain percentage), and facility location (for medical emergency response stations, while requiring high probability of coverage overall possible emergency scenarios). \r\n\r\n\r\n\r\n\r\n \r\nSuch problems are notoriously difficult to solve, because the feasible region is often not convex and the exact probabilities can be hard to compute exactly. We discuss a sampling approach that overcomes those obstacles. We have generalized a 2006 sampling algorithm of Calafiore-Campi’s for continuous variables that reduces the problem to solving deterministic convex mixed integer programming. A new generalization of Helly’s theorem is necessary to rigorously prove the sampling algorithms work as planned. \r\n\r\n\r\n \r\nIf time allows this talk will take a pick on the future of $S$-optimization theory, a powerful generalization of the traditional continuous, integer, and mixed-integer optimization, where now the variables take values in special proper subsets of $\\R^d$. All new theorems are joint work with R. La Haye, D. Oliveros, E. Roldan-Pensado."}
jdict2 = {"Seminar":"The next generation of artificial intelligence","Speaker":"Fran\u00e7ois Van Lishout (ULg - Montefiore)","Time":"November 25, 2016 (Friday) 22:15","Location":"Room R7, Montefiore Institute (B28)","Contact":"Fran\u00e7ois Van Lishout (f.vanlishout@ulg.ac.be)","Abstract":"World of Watson (WoW) is a 4-day conference organized every year in Las Vegas by IBM. I was invited to the 2016 edition by our partner NRB, which is itself an IBM-partner. \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\nThis year\u2019s WoW conference attracted around 17000 participants from all over the world, split into around 200 different rooms. I have put the focus mainly on talks linked with artifical intelligence, in the broad sense. I will try to present within an hour, as much as possible of the incredible things that I discovered there. \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\nTo already give you an idea of what my talk will be about, let me say a few words about Watson. It is an artificial intelligence cognitive computing system created by IBM, that can deal with massive amount of unstructured data and interface with human beings in ways that had never be seen before. It is well know from having won the jeopardy game-show in 2011, but this is not what it was about. It was about the beginning of the next era of computing. \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\nNowadays, Watson is used to improve decision making in health care, financial services and education, to name just three industries among many impacted by this technology. In this sense, Watson can be seen as an extended intelligence, rather than an artificial intelligence, since it\u2019s purpose is to augment human intelligence through the help of machines, rather than replacing humans through machines, …"}



def test_json_parse_date():
    expected = datetime(2016, 12, 9, 11, 0)
    given = JSONParser()._parse_date('December 09, 2016 (Friday) 11:00')
    delta = given - expected
    assert_equal(delta.total_seconds(), 0.0)

def test_remove_eol():
    original = "aaaa\r\n\r\n\r\n\r\n\r\n \r\n bbbb"
    expected = "aaaa\r\n\r\nbbbb"
    given = JSONParser()._remove_duplicate_eol(original)
    assert_equal(expected, given)


def test_weirdchars():
    parser = JSONParser()
    chars = [('Helly\u2019s theore', 'Helly’s theore')]
    for base, expected in chars:
        given = parser._html2str({0: base})
        assert_equal(given[0], expected)


def test_json_parsing():
    parser = JSONParser()
    jdicts = [jdict1, jdict2]
    names = ["Chance-Constrained Convex Mixed-Integer Programs and Beyond",
             "The next generation of artificial intelligence"]
    try:
        for jdict, name in zip(jdicts, names):
            seminar = parser(jdict)
            assert_equal(seminar.name, name)
        assert_true(True)
    except Exception as ex:
        assert_true(False, "Got {}".format(repr(ex)))


def test_montef_link_list():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    seminar_suffix="seminars.html"
    path = os.path.join(dir_path, seminar_suffix)
    ds = MontefioreGetter()
    expected = ['http://www.montefiore.ulg.ac.be/seminar/chance-constrained-convex-mixed-integer-programs-and-beyond/', 'http://www.montefiore.ulg.ac.be/seminar/sound-fields-in-rooms-models-and-applications/']
    given = ds._get_link_list(open(path).read())
    assert_equal(given, expected)


