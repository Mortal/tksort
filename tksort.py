#!/usr/bin/env python3

import re
import sys

prefixes = dict(zip('GBOTK', (1, 2, 3, 1, -1)))

TITLE = re.compile(
    r'''
    (?P<best>CERM|FORM|INKA|KASS|NF|PR|SEKR|VC)
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
    re.I | re.X)


def tk_parse(s):
    pref = 0
    fu = 0
    title = ''
    for mo in TITLE.finditer(s):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'prefix':
            pref += prefixes[value.upper()]
        elif kind == 'multiprefix':
            pref += prefixes[value[0]] * int(value[1:])
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


def tk_key(s):
    p = tk_parse(s)
    if p:
        return (0, p, s)
    else:
        return (1, s)


def main():
    for line in sorted(sys.stdin.readlines(), key=tk_key):
        sys.stdout.write(line)


if __name__ == "__main__":
    main()
