import argparse

import schema_reader
from generators import intermediate_files
from generators import csv_generator
from generators import es_template


def main():
    args = argument_parser()

    version = read_version()
    print "Running generator. ECS version " + version

    (ecs_nested, ecs_flat) = schema_reader.load_ecs()

    intermediate_files.generate(ecs_nested, ecs_flat)
    if args.intermediate_only:
        exit

    csv_generator.generate(ecs_flat, version)
    es_template.generate(ecs_flat, version)


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--intermediate-only', action='store_true',
                        help='generate intermediary files only')

    return parser.parse_args()


def read_version(file='version'):
    with open(file, 'r') as infile:
        return infile.read().rstrip()


if __name__ == '__main__':
    main()
