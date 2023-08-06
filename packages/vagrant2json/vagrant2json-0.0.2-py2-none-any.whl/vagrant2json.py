#!/usr/bin/env python

from collections import namedtuple
from itertools import izip_longest, ifilter, imap, takewhile, izip
from json import dump
from sys import stdin, stdout
from argparse import ArgumentParser, FileType
from pprint import PrettyPrinter

__author__ = 'Samuel Marks'
__version__ = '0.0.2'

pp = PrettyPrinter(indent=4).pprint

GlobalStatus = namedtuple('GlobalStatus', ['id', 'name', 'provider', 'state', 'directory'])


def _build_parser():
    """
    CLI arguments built out

    :return: ``ArgumentParser`` instance
    :rtype: ``ArgumentParser`` instance
    """
    parser = ArgumentParser(description='Convert Vagrant `--machine-readable` output to JSON',
                            usage='E.g.: `vagrant global-status --machine-readable | python -m vagrant2json`')
    parser.add_argument('infile', nargs='?', type=FileType('r'), default=stdin, help='[stdin]')
    parser.add_argument('outfile', nargs='?', type=FileType('w'), default=stdout, help='[stdout]')
    parser.add_argument('--ugly', action='store_true', help='Compress JSON output [False]')
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    return parser


def parse_global_status(io):
    """
    Parse global status output

    :keyword io: IO containing the output of: `vagrant global-status --machine-readable`.
    :type io: ``IO`` (e.g.: ``StringIO``, ``stdin``)

    :return: List of global statuses
    :rtype: ``List`` of ``GlobalStatus``
    """
    return (lambda get_last_col: (
        lambda headers: tuple(
            imap(lambda a: GlobalStatus(*a), izip_longest(
                *[(ifilter(lambda r: r is not None and not r.endswith('\\n"vagrant destroy 1a2b3c4d'),
                           imap(get_last_col, io)))] * len(headers))))
    )(tuple(ifilter(None, imap(get_last_col, takewhile(lambda c: c[-5] != '-', io))))))(
        lambda row: (lambda r: r if r else None)(row[row.rfind(',') + 1:-2].rstrip()))


def to_list_of_dict(namedtuples):
    """
    Converts a iterable of namedtuple tuples into a list of dictionaries

    :keyword namedtuples: iterable of namedtuple tuples
    :type namedtuples: ``list``, ``tuple`` or anything with `__iter__` defined and containing namedtuple tuples

    :return: List of dictionaries
    :rtype: ``List`` of ``dict``
    """
    return map(lambda named_tuple: dict(izip(named_tuple._fields, named_tuple)), namedtuples)


if __name__ == '__main__':
    args = _build_parser().parse_args()
    dump(to_list_of_dict(parse_global_status(args.infile)), args.outfile, ensure_ascii=False, check_circular=False,
         allow_nan=False,
         **({'sort_keys': True, 'indent': 4} if not args.ugly else {'separators': (',', ':')}))
    if not args.ugly:
        args.outfile.write('\n')
    args.outfile.close()
