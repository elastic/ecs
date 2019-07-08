import argparse
import glob
import os
import schema_reader
from generators import intermediate_files
from generators import csv_generator
from generators import es_template
from generators import beats
from generators import asciidoc_fields
from generators import ecs_helpers


def main():
    args = argument_parser()

    ecs_version = read_version()
    print 'Running generator. ECS version ' + ecs_version

    # Load the default schemas
    print 'Loading default schemas'
    (ecs_nested, ecs_flat) = schema_reader.load_ecs(sorted(glob.glob('schemas/*.yml')))

    # Maybe load user specified directory of schemas
    if args.include:
        include_glob = os.path.join(args.include, '*.yml')

        print 'Loading user defined schemas: {0}'.format(include_glob)

        (user_ecs_nested, user_ecs_flat) = schema_reader.load_ecs(sorted(glob.glob(include_glob)))

        # Merge without allowing user schemas to overwrite default schemas
        ecs_nested = ecs_helpers.safe_merge_dicts(ecs_nested, user_ecs_nested)
        ecs_flat = ecs_helpers.safe_merge_dicts(ecs_flat, user_ecs_flat)

    intermediate_files.generate(ecs_nested, ecs_flat)
    if args.intermediate_only:
        exit

    csv_generator.generate(ecs_flat, ecs_version)
    es_template.generate(ecs_flat, ecs_version)
    beats.generate(ecs_nested, ecs_version)
    asciidoc_fields.generate(ecs_nested, ecs_version)


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--intermediate-only', action='store_true',
                        help='generate intermediary files only')
    parser.add_argument('--include', action='store',
                        help='include user specified directory of custom field definitions')
    return parser.parse_args()


def read_version(file='version'):
    with open(file, 'r') as infile:
        return infile.read().rstrip()


if __name__ == '__main__':
    main()
