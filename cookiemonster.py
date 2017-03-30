#!/usr/bin/env python

import argparse
import cookielib
import re

import browsercookie


def filter_cookiejar(cookiejar, out_cookiejar, domain, name, path, value):
    for cookie in cookiejar:
        if domain is not None:
            if domain.startswith('~'):
                if not re.search(domain[1:], cookie.domain):
                    continue
            elif domain != cookie.domain:
                continue
        if name is not None:
            if name.startswith('~'):
                if not re.search(name[1:], cookie.name):
                    continue
            elif name != cookie.name:
                continue
        if path is not None:
            if path.startswith('~'):
                if not re.search(path[1:], cookie.path):
                    continue
            elif path != cookie.path:
                continue
        if value is not None:
            if value.startswith('~'):
                if not re.search(value[1:], cookie.value):
                    continue
            elif value != cookie.value:
                continue

        out_cookiejar.set_cookie(cookie)

    return out_cookiejar


def main():
    parser = argparse.ArgumentParser(description='Browser cookie inspector')
    parser.add_argument(
        "-d", "--domain",
        help="Print only cookies with matching domain. "
             "If first char is ~, then treat as regexp.",
    )
    parser.add_argument(
        "-n", "--name",
        help="Print only cookies with matching name. "
             "If first char is ~, then treat as regexp.",
    )
    parser.add_argument(
        "--path",
        help="Print only cookies with matching path. "
             "If first char is ~, then treat as regexp.",
    )
    parser.add_argument(
        "--value",
        help="Print only cookies with matching value. "
             "If first char is ~, then treat as regexp.",
    )
    parser.add_argument(
        "--ignore-expires", action='store_true',
        help="Print matching cookies even if they're expired",
    )
    parser.add_argument(
        "--format",
        choices=['netscape', 'lwp', 'json', 'value-only'],
        default='netscape',
        help="Print matching cookies even if they're expired",
    )
    args = parser.parse_args()

    cookiejar = browsercookie.load()
    if args.format == 'lwp':
        out_cookiejar = cookielib.LWPCookieJar()
    else:
        out_cookiejar = cookielib.MozillaCookieJar()

    filter_cookiejar(cookiejar, out_cookiejar,
                     args.domain, args.name, args.path, args.value)

    if args.format == 'json':
        print(json.dumps([cookie.__dict__ for cookie in out_cookiejar],
                         indent=4))
    elif args.format in ('netscape', 'lwp'):
        out_cookiejar.save(filename='/dev/stdout',
                           ignore_expires=args.ignore_expires)
    elif args.format == 'value-only':
        for cookie in out_cookiejar:
            print(cookie.value)


if __name__ == "__main__":
    main()
