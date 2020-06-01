import argparse
import glob
import os
# import pdb
import yaml

from generators import asciidoc_fields
from generators import beats
from generators import csv_generator
from generators import es_template
from generators import ecs_helpers
from generators import intermediate_files

from schema import loader
from schema import cleaner
from schema import finalizer
from schema import subset_filter


def main():
    args = argument_parser()

    ecs_version = read_version()
    print('Running generator. ECS version ' + ecs_version)

    fields = loader.load_schemas(args.include)
    # ecs_helpers.yaml_dump('_notes/nest-as/ecs_intermediate-loaded.yml', fields)

    cleaner.clean(fields)
    # ecs_helpers.yaml_dump('_notes/nest-as/ecs_intermediate-cleaned.yml', fields)

    finalizer.finalize(fields)
    # ecs_helpers.yaml_dump('_notes/nest-as/ecs_intermediate-final.yml', fields)

    fields = subset_filter.filter(fields, args.subset)
    # ecs_helpers.yaml_dump('_notes/nest-as/ecs_intermediate-filtered.yml', fields)

    # default location to save files
    out_dir = 'generated'
    docs_dir = 'docs'
    if args.out:
        out_dir = os.path.join(args.out, out_dir)
        docs_dir = os.path.join(args.out, docs_dir)

    ecs_helpers.make_dirs(out_dir)
    ecs_helpers.make_dirs(docs_dir)

    nested, flat = intermediate_files.generate(fields, out_dir)
    if args.intermediate_only:
        exit()

    print('up to here for now')
    exit()

    csv_generator.generate(flat, ecs_version, out_dir)
    es_template.generate(flat, ecs_version, out_dir)
    beats.generate(nested, ecs_version, out_dir)
    if args.include or args.subset:
        exit()
    asciidoc_fields.generate(fields, ecs_version, docs_dir)


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--intermediate-only', action='store_true',
                        help='generate intermediary files only')
    parser.add_argument('--include', nargs='+',
                        help='include user specified directory of custom field definitions')
    parser.add_argument('--subset', nargs='+',
                        help='render a subset of the schema')
    parser.add_argument('--out', action='store', help='directory to store the generated files')
    args = parser.parse_args()
    # Clean up empty include of the Makefile
    if args.include and [''] == args.include:
        args.include.clear()
    return args


def read_version(file='version'):
    with open(file, 'r') as infile:
        return infile.read().rstrip()


if __name__ == '__main__':
    main()
