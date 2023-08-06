# -*- coding: utf-8 -*-
#
# Main entry point for quorra
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import os
import sys
import argparse

from . import __version__


# args
# ----
parser = argparse.ArgumentParser()
# parser.add_argument('-o', '--option', help='Arbitrary option -- uncomment and update to use.', default=None)
subparsers = parser.add_subparsers()


# version
# -------
parser_version = subparsers.add_parser('version')
parser_version.set_defaults(func=lambda x: sys.stderr.write(__version__))


# exec
# ----
def main():
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

