# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

from bookmd.utils import replace_all_dsl, extract_default_template


def test_simple():
    isbn2book = {
        '123': {
            'a': 'test 1',
            'b': {
                'c': 'nested',
            }
        },
        '234': {
            'a': 'test 2',
        }
    }

    text = (
        'mark 1 {{ isbn = "123" template = "{a} {b[c]} " }}'
        'mark 2 {{ isbn = "234" template = "{a}" }}'
    )

    ret = replace_all_dsl(text, isbn2book)
    assert ret == 'mark 1 test 1 nested mark 2 test 2'


def test_extract_default_template():
    text = (
        'faefajeifajeig '
        '<!--  bookmd-default-template  : "abc"-->'
        'afjeaifajeif'
    )
    assert 'abc' == extract_default_template(text)
    assert extract_default_template('afjeifjaeif') is None
