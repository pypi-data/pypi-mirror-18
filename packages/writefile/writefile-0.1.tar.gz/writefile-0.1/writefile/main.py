#!/usr/bin/env python

import os
import sys
import errno
import argparse


BUFSIZE = 2**20


def main(args=sys.argv[1:]):
    """
    Write stdin to a given path, creating directories as necessary.
    """
    opts = parse_args(args)
    ensure_dir_exists(os.path.dirname(os.path.abspath(opts.PATH)))

    with file(opts.PATH, 'w') as f:
        buf = sys.stdin.read(BUFSIZE)
        while buf:
            f.write(buf)
            buf = sys.stdin.read(BUFSIZE)


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)

    p.add_argument(
        'PATH',
        help='The PATH to write.',
    )

    return p.parse_args(args)


def ensure_dir_exists(path):
    try:
        os.makedirs(path)
    except os.error as e:
        if e.errno != errno.EEXIST:
            raise


if __name__ == '__main__':
    main()
