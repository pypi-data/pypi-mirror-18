#!/usr/bin/env python

"""script2package: turn a python script into a python package"""

import argparse
import os.path
from script2package import *

def generate_skeleton(script=None, base="package"):
    """Generates a package skeleton within current working directory.

    :param script: file path to the script of interest
    :param base: name of the base folder for package generation
    :param config: setuptools configuration
    :param setup_cfg: path to the setup.cfg file
    :return: this function returns nothing
    """
    import os
    from os.path import basename, splitext
    from shutil import copyfile, rmtree
    if script is None:
        print("Script file must be provided within `generate_skeleton`!")
        raise

    base_script = basename(script)
    name, ext = splitext(base_script)
    if not ext.endswith("py"):
        print("Script file %s does not appear to be a python script!" % script)
        raise

    # create folder layout
    try:
        rmtree(base)
    except:
        pass

    os.makedirs('{base}/{name}'.format(base=base, name=name))

    # create the setup.py
    with open('{base}/setup.py'.format(base=base), 'w') as f:
        setup_py = """#!/usr/bin/env python

from setuptools import setup

setup(
    setup_requires=['d2to1'],
    d2to1=True
)"""
        f.write(setup_py)

    # copy setup.cfg and readme.md if applicable
    # will have to extend to other files in future
    if os.path.isfile(os.path.join(os.path.dirname(script), 'setup.cfg')):
        copyfile(os.path.join(os.path.dirname(script), 'setup.cfg'),
                 '{base}/setup.cfg'.format(base=base))
    else:
        # we have to generate the file
        with open('{base}/setup.cfg'.format(base=base), 'w') as f:
            setup_cfg = """
[metadata]
name = {name}
""".format(name=name)
            f.write(setup_cfg)
    if os.path.isfile(os.path.join(os.path.dirname(script), 'readme.md')):
        copyfile(os.path.join(os.path.dirname(script), 'readme.md'),
                 '{base}/readme.md'.format(base=base))

    # create __init__.py
    with open('{base}/{name}/__init__.py'.format(base=base, name=name), 'w') as f:
        f.write("""{script}""".format(script=open(script, 'r').read()))

    # create __init__.py: this is redundant but needed for cli tools??
    # have to have an option to turn this on or off
    with open('{base}/{name}/__main__.py'.format(base=base, name=name), 'w') as f:
        f.write("""{script}""".format(script=open(script, 'r').read()))

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
