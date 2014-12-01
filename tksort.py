#!/usr/bin/env python3

import re
import sys
import argparse

prefixes = dict(zip('GBOTK', (1, 2, 3, 1, -1)))

TITLE = re.compile(
    r'''
    (?P<best>BEST|CERM|FORM|INKA|KASS|NF|PR|SEKR|VC)
    |
    (?P<efu>EFU..)
    |
    (?P<fu>FU..)
    |
    (?P<multiprefix>[GBOTK][0-9]+)
    |
    (?P<prefix>[GBOTK])
    |
    (?P<rest>.*)
    ''',
    re.X)


def tk_parse(s, args):
    pref = 0
    fu = 0
    title = ''
    if args.ignore_case:
        s = s.upper()

    for mo in TITLE.finditer(s):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'prefix':
            pref += prefixes[value.upper()]
        elif kind == 'multiprefix':
            pref += prefixes[value[0].upper()] * int(value[1:])
        elif kind == 'efu':
            fu = 2
            title = value
        elif kind == 'fu':
            fu = 1
            title = value
        elif kind == 'best':
            fu = 0
            title = value

    if title:
        return (pref, fu, title)
    else:
        return None


def tk_key(s, args):
    p = tk_parse(s, args)
    if p:
        return (0, p, s)
    else:
        return (1, s)


def tk_min_key(s, args):
    words = s.split()
    return min(
        ((0, p, s)
         for p, word in zip((tk_parse(word, args) for word in words), words)
         if p),
        default=(1, s))


def tk_max_key(s, args):
    words = s.split()
    return max(
        ((0, p, s)
         for p, word in zip((tk_parse(word, args) for word in words), words)
         if p),
        default=(1, s))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--min', action='store_const', dest='key', const=tk_min_key,
        default=tk_key)

    parser.add_argument(
        '--max', action='store_const', dest='key', const=tk_max_key)

    parser.add_argument(
        '-i', '--ignore-case', action='store_true')

    args = parser.parse_args()

    key = lambda s: args.key(s, args)

    for line in sorted(sys.stdin.readlines(), key=key):
        sys.stdout.write(line)


if __name__ == "__main__":
    main()
