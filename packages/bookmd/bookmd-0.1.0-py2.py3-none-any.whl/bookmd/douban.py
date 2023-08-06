# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa


import grequests
from magic_constraints import Union, Sequence, Mapping


_T1 = Union[int, float, str]
_T2 = Sequence[_T1]
_T3 = Mapping[_T1, _T1]

_ValueType = Union[_T1, _T2, _T3]


def extract_isbn_from_url(url):
    return url.rsplit('/', 1)


# json response of douban api.
# return: bool(success), str(isbn13), obj
def process_response(response):
    data = response.json()

    # connection error or timeout.
    if response is None:
        return False, None, None

    # wrong isbn.
    if response.status_code != 200:
        return False, extract_isbn_from_url(data['request']), None

    isbn = data['isbn13']
    book = {
        k: v if isinstance(v, _ValueType) else None
        for k, v in data.items()
    }
    return True, isbn, book


class _ExceptionRecorder(object):

    def __init__(self):
        self.error_isbns = set()

    def __call__(self, request, exception):
        self.error_isbns.add(
            extract_isbn_from_url(request.url),
        )


def query_books(isbns):
    BOOK_API = 'https://api.douban.com/v2/book/isbn/{isbn}'

    urls = map(
        lambda isbn: BOOK_API.format(isbn=isbn),
        isbns,
    )
    responses = (
        grequests.get(url) for url in urls
    )

    exception_handler = _ExceptionRecorder()
    book_queries = map(
        process_response,
        # wait for 10s.
        grequests.map(
            responses,
            exception_handler=exception_handler,
            gtimeout=10,
        ),
    )

    return book_queries, exception_handler


# return (not_found_isbns, request_error_isbns, isbn2book)
def query_books_with_retry(isbns, retry=3):
    isbns = set(isbns)

    not_found_isbns = []
    request_error_isbns = []
    isbn2book = {}

    while isbns and retry > 0:
        book_queries, exception_handler = query_books(isbns)

        for success, isbn, book in book_queries:

            if not success:
                # bad case.
                if isbn is None:
                    # connection problem.
                    pass
                else:
                    # wrong isbn.
                    not_found_isbns.append(isbn)
                    # don't query again.
                    isbns.remove(isbn)
            else:
                # good case.
                isbns.remove(isbn)
                isbn2book[isbn] = book

        retry -= 1

    request_error_isbns = list(isbns)
    return not_found_isbns, request_error_isbns, isbn2book
