import argparse
import glob
import os
import yaml
import time

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

    ecs_version = read_version(args.ref)
    print('Running generator. ECS version ' + ecs_version)

    # default location to save files
    out_dir = 'generated'
    docs_dir = 'docs'
    if args.out:
        default_dirs = False
        out_dir = os.path.join(args.out, out_dir)
        docs_dir = os.path.join(args.out, docs_dir)
    else:
        default_dirs = True

    ecs_helpers.make_dirs(out_dir)
    ecs_helpers.make_dirs(docs_dir)

    # To debug issues in the gradual building up of the nested structure, insert
    # statements like this after any step of interest.
    # ecs_helpers.yaml_dump('ecs.yml', fields)

    fields = loader.load_schemas(ref=args.ref, included_files=args.include)
    cleaner.clean(fields, strict=args.strict)
    finalizer.finalize(fields)
    fields = subset_filter.filter(fields, args.subset, out_dir)
    nested, flat = intermediate_files.generate(fields, os.path.join(out_dir, 'ecs'), default_dirs)

    if args.intermediate_only:
        exit()

    csv_generator.generate(flat, ecs_version, out_dir)
    es_template.generate(flat, ecs_version, out_dir, args.template_settings, args.mapping_settings)
    beats.generate(nested, ecs_version, out_dir)
    if args.include or args.subset:
        exit()

    asciidoc_fields.generate(nested, ecs_version, docs_dir)


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--intermediate-only', action='store_true',
                        help='generate intermediary files only')
    parser.add_argument('--include', nargs='+',
                        help='include user specified directory of custom field definitions')
    parser.add_argument('--subset', nargs='+',
                        help='render a subset of the schema')
    parser.add_argument('--out', action='store', help='directory to store the generated files')
    parser.add_argument('--ref', action='store', help='git reference to use when building schemas')
    parser.add_argument('--template-settings', action='store',
                        help='index template settings to use when generating elasticsearch template')
    parser.add_argument('--mapping-settings', action='store',
                        help='mapping settings to use when generating elasticsearch template')
    parser.add_argument('--strict', action='store_true',
                        help='enforce stricter checking at schema cleanup')
    args = parser.parse_args()
    # Clean up empty include of the Makefile
    if args.include and [''] == args.include:
        args.include.clear()
    return args


def read_version(ref=None):
    if ref:
        print('Loading schemas from git ref ' + ref)
        tree = ecs_helpers.get_tree_by_ref(ref)
        return tree['version'].data_stream.read().decode('utf-8').rstrip()
    else:
        print('Loading schemas from local files')
        with open('version', 'r') as infile:
            return infile.read().rstrip()


if __name__ == '__main__':
    main()
