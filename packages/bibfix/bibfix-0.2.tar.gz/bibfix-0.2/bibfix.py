#!/usr/bin/env python3
import argparse
import re
import sys

import bibtexparser


def main():

    parser = argparse.ArgumentParser(
        description='Fixes unescaped acronyms in titles in bibtex files '
                    'by automatically detecting them and optionally parsing '
                    'them from a specification file.')

    parser.add_argument(
        '-e', '--encoding',
        default='utf-8',
        help='Encoding to use for parsing and writing the bib files')

    parser.add_argument(
        '-i', '--include',
        help='A file with strings to additionally escape. '
             'Each line marks a single string to protect with curly braces')

    parser.add_argument(
        '-a', '--abbrev',
        action='store_true',
        default=False,
        help='Abbreviate common conference and journal title parts.')

    parser.add_argument(
        '-x', '--execute',
        type=argparse.FileType(),
        help='Specifies a python file with custom transformation to apply to '
             'each entry. For this purpose, a single function '
             'transform(entry) needs to be defined. This is performed after '
             'all other transformation and therefore allows to clean up '
             'errors.')

    parser.add_argument(
        'infile',
        metavar='INFILE',
        help='The bibtex file to process')
    parser.add_argument(
        'outfile',
        metavar='OUTFILE',
        help='The bibtex file to write to or - for stdout.')

    args = parser.parse_args()

    # prepare -x argument
    if args.execute:
        exec_globals = {}
        eval(compile(args.execute.read(), args.execute.name, 'exec'),
             exec_globals)
        globals()['transform'] = exec_globals['transform']

    parser = bibtexparser.bparser.BibTexParser()
    parser.ignore_nonstandard_types = False
    parser.homogenise_fields = False
    with open(args.infile, encoding=args.encoding) as infile:
        database = bibtexparser.load(infile, parser=parser)

    if args.include:
        with open(args.include, encoding=args.encoding) as include_file:
            includes = include_file.readlines()
            includes = [s.strip() for s in includes if s.strip()]
        for entry in database.entries:
            for pattern in includes:
                entry['title'] = entry['title'].replace(
                    pattern, '{' + pattern + '}')

    acro_re = re.compile(r'(\w*[A-Z]\w*[A-Z]\w*)')
    for entry in database.entries:
        entry['title'] = acro_re.sub(r'{\1}', entry['title'])

    conf_replacements = [
        ('Proceedings of the', 'Proc.'),
        ('Proceedings', 'Proc.'),
        ('International Conference on', 'Int. Conf.'),
        ('International', 'Int.'),
        ('Conference', 'Conf.'),
        ('Symposium', 'Symp.'),
    ]

    journal_replacements = [
        ('International', 'Int.'),
    ]

    # abbreviation
    if args.abbrev:
        for entry in database.entries:
            if entry['ENTRYTYPE'] == 'inproceedings':
                for source, target in conf_replacements:
                    entry['booktitle'] = entry['booktitle'].replace(
                        source, target)
            if entry['ENTRYTYPE'] == 'article':
                for source, target in journal_replacements:
                    entry['journal'] = entry['journal'].replace(
                        source, target)

    if args.execute:
        for entry in database.entries:
            transform(entry)

    if args.outfile == '-':
        bibtexparser.dump(database, sys.stdout)
    else:
        with open(args.outfile, 'w', encoding=args.encoding) as outfile:
            bibtexparser.dump(database, outfile)

if __name__ == "__main__":
    main()
