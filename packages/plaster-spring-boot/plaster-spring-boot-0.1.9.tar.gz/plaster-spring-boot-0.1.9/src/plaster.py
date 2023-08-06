#!/usr/bin/python

import argparse
import os
import sys
from argparse import RawTextHelpFormatter

import src.data.settings as settings
import src.generation.generator as generator
from data.strings import Docs
from data.version import __version__
from domain.field import Field

generators = {
    'g': generator,
    'generate': generator
}


def main():
    parser = argparse.ArgumentParser(
        prog='plaster',
        description='Generate files for Spring Boot',
        formatter_class=RawTextHelpFormatter)

    # Positional Arguments
    parser.add_argument('-v', '--version', help=Docs.version, action='version', version=__version__)
    parser.add_argument('-k', '--key', nargs='?', help=Docs.key)

    parser.add_argument('mode', choices=Docs.generation_mode_choices, help=Docs.generation_mode)
    parser.add_argument('type', choices=Docs.generation_type_choices, help=Docs.generation_type)
    parser.add_argument('model', metavar='model_name', help=Docs.model)
    parser.add_argument('fields', nargs='*', help=Docs.fields)

    args = parser.parse_args()

    if not os.path.isfile('./pom.xml'):
        print 'Not on the root level of a maven project - cannot generate'
        sys.exit(-1)

    gen_type = args.mode
    gen_sub_type = args.type
    gen_name = args.model
    gen_kwargs = args.fields

    settings.load()
    if args.key:
        name, field_type = args.key.split(':')
        settings.ID = Field(name, field_type)

    error = generators[gen_type].perform(gen_sub_type, gen_name, gen_kwargs)

    if error:
        print error


if __name__ == '__main__':
    main()
