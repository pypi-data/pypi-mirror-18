#!/usr/bin/env python

"""script2package: turn a python script into a python package"""

from script2package.util import generate_skeleton
import argparse
import os.path

def main():
    """
    `script2package` will correctly treat any `setup.cfg` files which it comes
    across.

    If it will simply use the default setup settings with the package using
    the name of the script as the name of the package. The filename will be
    automatically sanitized.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('script')
    parser.add_argument('--base', action='store', default='package')
    args = parser.parse_args()

    if args.script is None or not os.path.isfile(args.script):
        print("Please enter a valid python script!")
        raise

    generate_skeleton(args.script, base=args.base)
