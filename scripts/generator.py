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
    print('Running generator. ECS version ' + ecs_version)

    # Load the default schemas
    print('Loading default schemas')
    (nested, flat) = schema_reader.load_schemas()

    # Maybe load user specified directory of schemas
    if args.include:

        print('Loading user defined schemas: {0}'.format(args.include))

        (custom_nested, custom_flat) = schema_reader.load_schemas(get_yaml_files(args.include))

        # Merge without allowing user schemas to overwrite default schemas
        nested = ecs_helpers.safe_merge_dicts(nested, custom_nested)
        flat = ecs_helpers.safe_merge_dicts(flat, custom_flat)

    if args.use_case_dir:
        print('Loading use case directory: {}'.format(args.use_case_dir))
        use_cases_nested, use_cases_flat = schema_reader.load_use_case_files(
            get_yaml_files(args.use_case_dir), nested['base'])

        # Merge and allow user schemas to overwrite default schemas
        nested = schema_reader.merge_dict_overwrite(nested, use_cases_nested)
        flat = schema_reader.merge_dict_overwrite(flat, use_cases_flat)

    intermediate_files.generate(nested, flat)
    if args.intermediate_only:
        exit()

    csv_generator.generate(flat, ecs_version)
    es_template.generate(flat, ecs_version)
    beats.generate(nested, ecs_version)
    asciidoc_fields.generate(nested, flat, ecs_version)


def get_yaml_files(path):
    file_types = ('*.yml', '*.yaml')
    all_files = []
    for t in file_types:
        all_files.extend(glob.glob(os.path.join(path, t)))

    return sorted(all_files)


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--intermediate-only', action='store_true',
                        help='generate intermediary files only')
    parser.add_argument('--include', action='store',
                        help='include user specified directory of custom field definitions')
    parser.add_argument('--use-case-dir', action='store',
                        help='include user specified directory of custom use-case style field definitions')
    return parser.parse_args()


def read_version(file='version'):
    with open(file, 'r') as infile:
        return infile.read().rstrip()


if __name__ == '__main__':
    main()
