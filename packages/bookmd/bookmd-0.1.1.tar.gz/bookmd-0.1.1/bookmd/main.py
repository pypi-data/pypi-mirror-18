# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

from os import getcwd, mkdir
from os.path import join, exists

import click

from .douban import query_books_with_retry
from .utils import (
    extract_isbns_from_directory, load_toml, dump_toml,
    replace_all_dsl,
    load_file, write_file,
    generate_list, generate_table,
)


click.disable_unicode_literals_warning = True


ISBN_DIRNAME = 'isbn'
BOOK_DATABASE = '.bookmd-db'
BOOK_TOML = 'bookmd.toml'


def dirpath(dirname):
    return join(getcwd(), dirname)


def database_path(name):
    return join(dirpath(BOOK_DATABASE), name)


@click.command()
def init():
    # directories.
    for path in map(lambda dirname: dirpath(dirname),
                    [ISBN_DIRNAME, BOOK_DATABASE]):
        if not exists(path):
            mkdir(path)

    # files.
    TOML_PATH = database_path(BOOK_TOML)
    if not exists(TOML_PATH):
        dump_toml(TOML_PATH, {})


@click.command()
def query():
    ISBN_DIRPATH = dirpath(ISBN_DIRNAME)
    TOML_PATH = database_path(BOOK_TOML)

    isbns = extract_isbns_from_directory(ISBN_DIRPATH)
    isbn2book = load_toml(TOML_PATH)

    new_isbns = filter(
        lambda isbn: isbn not in isbn2book,
        isbns,
    )
    ret = query_books_with_retry(new_isbns)
    not_found_isbns, request_error_isbns, new_isbn2book = ret

    if not_found_isbns:
        raise RuntimeError('not_found_isbns')
    if request_error_isbns:
        raise RuntimeError('request_error_isbns')

    isbn2book.update(new_isbn2book)
    dump_toml(TOML_PATH, isbn2book)


@click.command()
@click.argument('form')
@click.option('--keys', default=None)
@click.argument('dst', type=click.Path())
def template(form, keys, dst):
    TOML_PATH = database_path(BOOK_TOML)
    isbn2book = load_toml(TOML_PATH)

    FORM_GENERATOR = {
        'list': generate_list,
        'table': generate_table,
    }

    if form not in FORM_GENERATOR:
        raise RuntimeError('invalid form.')

    write_file(dst, FORM_GENERATOR[form](isbn2book, keys))


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dst', type=click.Path())
def transform(src, dst):
    TOML_PATH = database_path(BOOK_TOML)

    text = load_file(src)
    isbn2book = load_toml(TOML_PATH)

    processed = replace_all_dsl(text, isbn2book)

    write_file(dst, processed)


@click.group()
def entry_point():
    pass


entry_point.add_command(init)
entry_point.add_command(query)
entry_point.add_command(template)
entry_point.add_command(transform)
