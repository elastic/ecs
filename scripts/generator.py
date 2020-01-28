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

    if args.schema:
        print('Schemas parameter: {}'.format(args.schema))
        schemas_dir = args.schema
    else:
        schemas_dir = [schema_reader.ECS_CORE_DIR]
        print('Using default schemas directory: {}'.format(schemas_dir[0]))

    schema_files = get_glob_files(schemas_dir, ('*.yml', '*.yaml'))
    if args.exclude:
        print('Exclude parameter: {}'.format(args.exclude))
        schema_files = set(schema_files) - set(get_glob_files(schemas_dir, [args.exclude]))

    print('Loading schema files: [{}]'.format(', '.join(schema_files)))
    if args.validate:
        print('Validating against ecs core')
        ecs_core_files = get_glob_files([schema_reader.ECS_CORE_DIR], ('*.yml', '*.yaml'))
        # put the ecs core files first so conflicts can be presented correctly
        ecs_core_files.extend(schema_files)
        schema_files = ecs_core_files
    nested, flat = schema_reader.load_schemas(schema_files, args.validate)

    if args.validate:
        print('Validation finished, no errors')
        exit()
    # default location to save files
    out_dir = 'generated'
    docs_dir = 'docs'
    if args.out:
        out_dir = os.path.join(args.out, out_dir)
        docs_dir = os.path.join(args.out, docs_dir)

    ecs_helpers.make_dirs(out_dir)
    ecs_helpers.make_dirs(docs_dir)

    intermediate_files.generate(nested, flat, out_dir)
    if args.intermediate_only:
        exit()

    csv_generator.generate(flat, ecs_version, out_dir)
    es_template.generate(flat, ecs_version, out_dir)
    beats.generate(nested, ecs_version, out_dir)
    asciidoc_fields.generate(nested, flat, ecs_version, docs_dir)


def get_glob_files(paths, file_types):
    all_files = []
    for path in paths:
        schema_files_with_glob = []
        for t in file_types:
            schema_files_with_glob.extend(glob.glob(os.path.join(path, t)))
        # this preserves the ordering of how the schema flags are included, the last schema directory on the commandline
        # will have the ability to override the previous schema definitions
        all_files.extend(sorted(schema_files_with_glob))

    return all_files


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--intermediate-only', action='store_true',
                        help='generate intermediary files only')
    parser.add_argument('--schema', action='append', help='directory to use for schemas')
    parser.add_argument('--exclude', action='store',
                        help='a glob pattern to exclude certain schema files')
    parser.add_argument('--out', action='store', help='directory to store the generated files')
    parser.add_argument('--validate', action='store_true',
                        help='validate schemas against ecs core, no files will be generated')
    return parser.parse_args()


def read_version(file='version'):
    with open(file, 'r') as infile:
        return infile.read().rstrip()


if __name__ == '__main__':
    main()
