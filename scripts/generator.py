import yaml
import argparse

import schema_reader
from generators import csv_generator
from generators import es_template

def intermediate_files():
    (ecs_nested, ecs_fields) = schema_reader.load_ecs()
    with open('generated/ecs/fields_flat.yml', 'w') as outfile:
        yaml.dump(ecs_fields, outfile, default_flow_style=False)
    with open('generated/ecs/fields_nested.yml', 'w') as outfile:
        yaml.dump(ecs_nested, outfile, default_flow_style=False)
    return (ecs_nested, ecs_fields)

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--intermediate-only', action='store_true',
            help='generate intermediary files only')

    return parser.parse_args()

if __name__ == '__main__':
    args = argument_parser()

    (ecs_nested, ecs_flat) = intermediate_files()

    if args.intermediate_only:
        exit

    csv_generator.generate(ecs_flat)
    es_template.generate(ecs_flat)
