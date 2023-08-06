#!/usr/bin/python

import os
import sys

import data.settings as settings
import generation.generator as generator

generators = {
    'g': generator,
    'generate': generator
}


def main():
    if len(sys.argv) < 2:
        print 'USAGE: plaster <type> [field:type]*'
        sys.exit(-1)
    if not os.path.isfile('./pom.xml'):
        print 'Not on the root level of a maven project - cannot generate'
        sys.exit(-1)

    args = sys.argv[1:]

    gen_type = args[0].lower()
    gen_sub_type = args[1].lower()
    gen_name = args[2].lower()
    gen_kwargs = args[3:]

    settings.load()

    error = generators[gen_type].perform(gen_sub_type, gen_name, gen_kwargs)

    if error:
        print error


if __name__ == '__main__':
    main()
