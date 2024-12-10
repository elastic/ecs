# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import argparse
import os
from typing import (
    Optional,
)

from generators import asciidoc_fields
from generators import beats
from generators import csv_generator
from generators import es_template
from generators import ecs_helpers
from generators import intermediate_files
from generators import otel

from schema import loader
from schema import cleaner
from schema import finalizer
from schema import subset_filter
from schema import exclude_filter
from _types import (
    FieldEntry
)


def main() -> None:
    args = argument_parser()

    if not args.semconv_version:
        raise KeyError("OTel Semantic Conventions version has not been provided as a config option '--semconv-version'")

    ecs_generated_version: str = read_version(args.ref)
    print('Running generator. ECS version ' + ecs_generated_version)

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

    # To debug issues in the gradual building up of the nested structure, insert
    # statements like this after any step of interest.
    # ecs_helpers.yaml_dump('ecs.yml', fields)

    # Detect usage of experimental changes to tweak artifact version label
    if args.include and loader.EXPERIMENTAL_SCHEMA_DIR in args.include:
        ecs_generated_version += "+exp"
        print('Experimental ECS version ' + ecs_generated_version)

    fields: dict[str, FieldEntry] = loader.load_schemas(ref=args.ref, included_files=args.include)
    cleaner.clean(fields, strict=args.strict)
    finalizer.finalize(fields)
    fields, docs_only_fields = subset_filter.filter(fields, args.subset, out_dir)
    fields = exclude_filter.exclude(fields, args.exclude)

    otel_generator = otel.OTelGenerator(args.semconv_version)
    otel_generator.check_otel_attributes_mapping(fields)
    otel_generator.set_otel_attributes_stability_property(fields)

    nested, flat = intermediate_files.generate(fields, os.path.join(out_dir, 'ecs'), default_dirs)

    if args.intermediate_only:
        exit()

    csv_generator.generate(flat, ecs_generated_version, out_dir)
    es_template.generate(nested, ecs_generated_version, out_dir, args.mapping_settings, args.template_settings)
    es_template.generate_legacy(flat, ecs_generated_version, out_dir,
                                args.mapping_settings, args.template_settings_legacy)
    beats.generate(nested, ecs_generated_version, out_dir)
    if (args.include or args.subset or args.exclude) and not args.force_docs:
        exit()

    ecs_helpers.make_dirs(docs_dir)
    docs_only_nested = intermediate_files.generate_nested_fields(docs_only_fields)
    asciidoc_fields.generate(nested, docs_only_nested, ecs_generated_version,
                             args.semconv_version, otel_generator, docs_dir)


def argument_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--ref', action='store', help='Loads fields definitions from `./schemas` subdirectory from specified git reference. \
                                                       Note that "--include experimental/schemas" will also respect this git ref.')
    parser.add_argument('--include', nargs='+',
                        help='include user specified directory of custom field definitions')
    parser.add_argument('--exclude', nargs='+',
                        help='exclude user specified subset of the schema')
    parser.add_argument('--subset', nargs='+',
                        help='render a subset of the schema')
    parser.add_argument('--out', action='store', help='directory to output the generated files')
    parser.add_argument('--template-settings', action='store',
                        help='index template settings to use when generating elasticsearch template')
    parser.add_argument('--template-settings-legacy', action='store',
                        help='legacy index template settings to use when generating elasticsearch template')
    parser.add_argument('--mapping-settings', action='store',
                        help='mapping settings to use when generating elasticsearch template')
    parser.add_argument('--strict', action='store_true',
                        help='enforce strict checking at schema cleanup')
    parser.add_argument('--intermediate-only', action='store_true',
                        help='generate intermediary files only')
    parser.add_argument('--force-docs', action='store_true',
                        help='generate ECS docs even if --subset, --include, or --exclude are set')
    parser.add_argument('--semconv-version', action='store',
                        help='Load OpenTelemetry Semantic Conventions from this specified version')
    args = parser.parse_args()
    # Clean up empty include of the Makefile
    if args.include and [''] == args.include:
        args.include.clear()
    return args


def read_version(ref: Optional[str] = None) -> str:
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
