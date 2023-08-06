# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import re
from os import listdir
from os.path import isdir, join
from operator import methodcaller

import pytoml


def load_file(path):
    return open(path, encoding='utf-8').read()


def write_file(path, content):
    with open(path, mode='w', encoding='utf-8') as fout:
        fout.write(content)


def load_directory(path):
    if not isdir(path):
        raise RuntimeError('invalid directory path: {0}'.format(path))

    def join_path(name):
        return join(path, name) if not name.startswith('.') else None

    return filter(
        bool,
        map(join_path, listdir(path)),
    )


def extract_isbns(path):
    text = load_file(path)

    # isbn10 or isbn13.
    ISBN_PATTERN = r'(?<!\d)(\d{10}|\d{13})(?!\d)'
    isbns = re.findall(ISBN_PATTERN, text)

    return isbns


def extract_isbns_from_directory(dir_path):
    isbns = []
    for file_path in load_directory(dir_path):
        isbns.extend(extract_isbns(file_path))
    return set(isbns)


def load_toml(path):
    return pytoml.loads(load_file(path))


def dump_toml(path, obj):
    write_file(path, pytoml.dumps(obj))


def expend_str(text, start):
    n = len(text)

    i = start + 1
    escape = False

    while i < n:
        c = text[i]
        if not escape:
            # stop.
            if c == '"':
                break
            # to escape mode.
            if c == '\\':
                escape = True
        else:
            # to non-escape mode.
            escape = False
        # move to next character.
        i += 1

    if i >= n:
        raise RuntimeError("expend_str")

    return i + 1


def find_dsl(text, offset):
    pattern = re.compile(r'\{\{[ \t]*isbn', flags=re.U)

    if offset >= len(text):
        return None, None

    match = pattern.search(text, offset)
    if match is None:
        return None, None

    n = len(text)
    i = match.start()

    while i < n:
        # stop condition.
        if i + 1 < n and text[i] == text[i + 1] and text[i] == '}':
            return match.start(), i + 1

        if text[i] != '"':
            i += 1
        else:
            i = expend_str(text, i)

    return None, None


def render_dsl(book_dsl, isbn2book, default_template):
    isbn = book_dsl.get('isbn', None)
    template = book_dsl.get('template', None) or default_template

    # check field.
    if isbn is None or template is None:
        raise RuntimeError('missing isbn or template.')

    if isbn not in isbn2book:
        raise RuntimeError('invalid isbn.')

    return template.format(**isbn2book[isbn])


def replace_dsl(text, start, end, isbn2book, default_template):
    # {{......}}
    #   ^ i   ^ end
    i = start + 2
    end -= 1

    toml_stats = []

    while i < end:
        j = i

        # find the begin of ".
        while j < end and text[j] != '"':
            j += 1
        # corner case.
        if j == end:
            break

        j = expend_str(text, j)

        toml_stats.append(text[i:j])
        # inject newline.
        toml_stats.append('\n')

        i = j

    # parse.
    book_dsl = pytoml.loads(''.join(toml_stats).replace('\\', '\\\\'))
    return render_dsl(book_dsl, isbn2book, default_template)


def replace_all_dsl(text, isbn2book):
    n = len(text)
    default_template = extract_default_template(text)

    # find first stat.
    i, j = find_dsl(text, 0)

    if i is None:
        return text

    doc = []
    begin = 0
    while i is not None and i < n:
        # gap.
        doc.append(text[begin:i])
        # process stat.
        doc.append(replace_dsl(text, i, j, isbn2book, default_template))

        # move to next stat.
        begin = j + 1
        i, j = find_dsl(text, begin)

    if begin < n:
        doc.append(text[begin:])

    return ''.join(doc)


def extract_default_template(text):
    DEFAULT_TEMPLATE_PATTERN = (
        # html comment begin.
        r'\<\!\-\-[ \t]*'
        # bookmd-default-template:
        r'bookmd\-default\-template[ \t]*\:'
        # "xxx"
        r'[ \t]*"(.*?)"'
        # html comment end.
        r'[ \t]*\-\-\>'
    )

    match = re.search(DEFAULT_TEMPLATE_PATTERN, text)
    if match is None:
        return None
    else:
        return match.group(1)


def generate_book_dsl(isbn, title):
    return '{{{{ isbn="{isbn}" # {title} }}}}'.format(
        isbn=isbn, title=title,
    )


def generate_default_template(template):
    return '<!-- bookmd-default-template: "{0}" -->'.format(template)


def split_keys(keys, default=''):
    keys = keys or default
    return list(filter(bool, map(methodcaller('strip'), keys.split(','))))


def generate_list(isbn2book, keys):
    keys = split_keys(keys, 'title')

    lines = []

    default_template = generate_default_template(
        '[{0}]({{alt}})'.format(
            ', '.join(map('{{{0}}}'.format, keys)),
        ),
    )
    lines.append(default_template)

    for isbn, book in isbn2book.items():
        book_dsl = generate_book_dsl(
            isbn, book['title'],
        )
        line = '* {0}'.format(book_dsl)

        lines.append(line)

    return '\n'.join(lines)


def generate_table(isbn2book, keys):

    def table_line(cells):
        return '| {0} |'.format(
            ' | '.join(cells),
        )

    def table_bar(cell_size):
        return table_line(['---'] * cell_size)

    def key2dsl(key):
        if key == 'title':
            return '[{title}]({alt})'
        else:
            return '{{{0}}}'.format(key)

    keys = split_keys(keys, 'title,author[0],rating[average]')

    lines = []

    default_template = generate_default_template(
        table_line(map(key2dsl, keys)),
    )
    lines.append(default_template)

    lines.append(
        table_line(keys),
    )
    lines.append(
        table_bar(len(keys)),
    )

    for isbn, book in isbn2book.items():
        book_dsl = generate_book_dsl(
            isbn, book['title'],
        )

        lines.append(book_dsl)

    return '\n'.join(lines)
