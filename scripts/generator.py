import argparse
import glob
import os
import schema_reader
import yaml
from generators import intermediate_files
from generators import csv_generator
from generators import es_template
from generators import beats
from generators import asciidoc_fields
from generators import ecs_helpers


def main():
    args = argument_parser()

    ecs_version = read_version()
    print('Running generator. ECS version ' + ecs_version)

    # Load the default schemas
    print('Loading default schemas')
    intermediate_fields = schema_reader.load_schemas()

    # Maybe load user specified directory of schemas
    if args.include:
        include_glob = os.path.join(args.include, '*.yml')

        print('Loading user defined schemas: {0}'.format(include_glob))

        intermediate_custom = schema_reader.load_schemas(sorted(glob.glob(include_glob)))
        schema_reader.merge_schema_fields(intermediate_fields, intermediate_custom)

    if args.subset:
        subset = {}
        for arg in args.subset:
            for file in glob.glob(arg):
                with open(file) as f:
                    raw = yaml.safe_load(f.read())
                    ecs_helpers.recursive_merge_subset_dicts(subset, raw)
        intermediate_fields = ecs_helpers.fields_subset(subset, intermediate_fields)

    (nested, flat) = schema_reader.generate_nested_flat(intermediate_fields)
    intermediate_files.generate(nested, flat)
    if args.intermediate_only:
        exit()

    csv_generator.generate(flat, ecs_version)
    es_template.generate(flat, ecs_version)
    beats.generate(nested, ecs_version)
    asciidoc_fields.generate(nested, flat, ecs_version)


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--intermediate-only', action='store_true',
                        help='generate intermediary files only')
    parser.add_argument('--include', action='store',
                        help='include user specified directory of custom field definitions')
    parser.add_argument('--subset', nargs='+',
                        help='render a subset of the schema')
    return parser.parse_args()


def read_version(file='version'):
    with open(file, 'r') as infile:
        return infile.read().rstrip()


if __name__ == '__main__':
    main()
