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

"""ECS Generator - Main Entry Point.

This is the main orchestrator for the ECS artifact generation process. It coordinates
the entire pipeline from loading YAML schemas to generating all output artifacts.

Pipeline Overview:

    1. **Schema Processing** (schema/ modules):
       - Load schemas from YAML files or git ref
       - Clean and validate field definitions
       - Perform field reuse across fieldsets
       - Apply optional subset/exclude filters

    2. **OTel Validation** (generators/otel.py):
       - Validate OTel semantic conventions mappings
       - Enrich fields with OTel stability information

    3. **Intermediate Files** (generators/intermediate_files.py):
       - Generate ecs_flat.yml (flat field dictionary)
       - Generate ecs_nested.yml (nested by fieldset)

    4. **Artifact Generation** (generators/ modules):
       - CSV field reference (csv_generator.py)
       - Elasticsearch templates (es_template.py)
       - Beats field definitions (beats.py)
       - Markdown documentation (markdown_fields.py)

Command-Line Usage:

    Basic generation:
    ```bash
    python scripts/generator.py --semconv-version v1.24.0
    ```

    From specific git version:
    ```bash
    python scripts/generator.py --ref v8.10.0 --semconv-version v1.24.0
    ```

    With custom schemas:
    ```bash
    python scripts/generator.py \\
        --include custom/schemas/ \\
        --semconv-version v1.24.0
    ```

    Generate subset only:
    ```bash
    python scripts/generator.py \\
        --subset schemas/subsets/minimal.yml \\
        --semconv-version v1.24.0
    ```

    Strict validation:
    ```bash
    python scripts/generator.py \\
        --strict \\
        --semconv-version v1.24.0
    ```

Key Features:
    - **Git Reference Support**: Generate from any ECS version tag
    - **Custom Schema Merging**: Add custom fields to ECS
    - **Subset Filtering**: Generate artifacts for specific field subsets
    - **Exclude Filtering**: Remove deprecated fields for testing
    - **Strict Mode**: Enforce stricter validation rules
    - **Intermediate-Only Mode**: Generate only intermediate files (fast iteration)
    - **Experimental Support**: Include experimental schemas with +exp version tag

Output Structure:

    generated/
    ├── ecs/
    │   ├── ecs_flat.yml           # Flat field dictionary
    │   ├── ecs_nested.yml         # Nested by fieldset
    │   └── subset/                # Per-subset intermediate files
    ├── elasticsearch/
    │   ├── composable/            # Modern composable templates
    │   │   ├── template.json
    │   │   └── component/*.json
    │   └── legacy/                # Legacy single template
    │       └── template.json
    ├── beats/
    │   └── fields.ecs.yml         # Beats field definitions
    └── csv/
        └── fields.csv             # CSV field reference

    docs/reference/
    ├── fields/                    # Field documentation pages
    └── otel/                      # OTel alignment docs

Environment Requirements:
    - Python 3.7+
    - Git repository (for --ref support)
    - OTel semantic conventions version specified

Exit Codes:
    - 0: Success
    - Non-zero: Error during generation

See Also:
    - scripts/docs/schema-pipeline.md: Complete pipeline documentation
    - scripts/docs/README.md: All module documentation index
    - USAGE.md: User guide for running generators
    - CONTRIBUTING.md: Development guidelines
"""

import argparse
import os
from typing import (
    Optional,
)

from generators import markdown_fields
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
from ecs_types import (
    FieldEntry
)


def main() -> None:
    """Main entry point for ECS artifact generation.

    Orchestrates the complete pipeline:
    1. Parse command-line arguments
    2. Determine ECS version (from git ref or local)
    3. Setup output directories
    4. Run schema processing pipeline:
       - Load schemas (from git ref or filesystem)
       - Clean and validate
       - Finalize (perform reuse)
       - Apply filters (subset/exclude)
       - Validate OTel mappings
    5. Generate intermediate files (flat & nested YAML)
    6. Generate all artifacts:
       - CSV field reference
       - Elasticsearch templates (composable & legacy)
       - Beats field definitions
       - Markdown documentation (optional)

    Pipeline Stages:

        Schema Processing:
        - loader.load_schemas(): Load from YAML or git
        - cleaner.clean(): Validate and normalize
        - finalizer.finalize(): Perform field reuse
        - subset_filter.filter(): Apply subset (if specified)
        - exclude_filter.exclude(): Remove excluded fields (if specified)

        Validation:
        - otel.OTelGenerator(): Validate OTel mappings

        Intermediate:
        - intermediate_files.generate(): Create ecs_flat.yml & ecs_nested.yml

        Artifacts:
        - csv_generator.generate(): CSV field reference
        - es_template.generate(): Composable Elasticsearch template
        - es_template.generate_legacy(): Legacy Elasticsearch template
        - beats.generate(): Beats field definitions
        - markdown_fields.generate(): Documentation (optional)

    Early Exit Conditions:
        - --intermediate-only: Stop after generating intermediate files
        - Custom schemas/subsets without --force-docs: Skip markdown generation

    Version Handling:
        - Reads from 'version' file or git ref
        - Appends '+exp' if experimental schemas included
        - Used to tag all generated artifacts

    Output Directories:
        - Default: generated/ and docs/reference/
        - Custom: {args.out}/generated/ and {args.out}/docs/reference/

    Raises:
        KeyError: If --semconv-version not provided
        Various exceptions from pipeline stages on validation errors

    Example Execution:
        >>> # From command line:
        >>> # python scripts/generator.py --semconv-version v1.24.0
        Running generator. ECS version 8.11.0
        Loading schemas from local files
        # ... pipeline output ...

    Note:
        Markdown docs are skipped when using custom schemas/subsets unless
        --force-docs is specified, since custom fields may not have proper
        documentation structure.
    """
    args = argument_parser()

    if not args.semconv_version:
        raise KeyError("OTel Semantic Conventions version has not been provided as a config option '--semconv-version'")

    ecs_generated_version: str = read_version(args.ref)
    print('Running generator. ECS version ' + ecs_generated_version)

    # default location to save files
    out_dir = 'generated'
    docs_dir = 'docs/reference'
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
    otel_generator.validate_otel_mapping(fields)

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
    markdown_fields.generate(nested, docs_only_nested, ecs_generated_version,
                             args.semconv_version, otel_generator, docs_dir)


def argument_parser() -> argparse.Namespace:
    """Parse and return command-line arguments for the generator.

    Configures argument parser with all supported options for controlling
    the ECS generation pipeline.

    Returns:
        Parsed arguments namespace with all configuration options

    Arguments:

        Schema Loading:
        - --ref: Git reference (tag/branch/commit) to load schemas from
                 Example: --ref v8.10.0
                 Note: Also applies to experimental schemas if included

        - --include: Additional schema directories/files to include
                    Can specify multiple times or space-separated
                    Examples:
                      --include custom/schemas/
                      --include experimental/schemas
                      --include custom/field1.yml custom/field2.yml

        Filtering:
        - --subset: Subset definition files to filter included fields
                   Example: --subset schemas/subsets/minimal.yml

        - --exclude: Exclude definition files to remove fields
                    Example: --exclude excludes/deprecated.yml
                    Useful for testing deprecation impact

        Output:
        - --out: Custom output directory (default: current directory)
                Generated files go to {out}/generated/
                Docs go to {out}/docs/reference/

        Elasticsearch Templates:
        - --template-settings: JSON file with composable template settings
                              Overrides index_patterns, priority, settings

        - --template-settings-legacy: JSON file with legacy template settings

        - --mapping-settings: JSON file with mapping settings
                             Overrides date_detection, dynamic_templates

        Validation & Control:
        - --strict: Enable strict validation mode
                   Warnings become errors
                   Enforces description length limits
                   Required for CI/CD

        - --intermediate-only: Generate only intermediate files
                             Skip artifact generation
                             Useful for debugging pipeline

        - --force-docs: Generate markdown docs even with custom schemas
                       By default, docs skipped with --include/--subset/--exclude
                       Use this to override and generate anyway

        - --semconv-version: OTel Semantic Conventions version (REQUIRED)
                           Example: --semconv-version v1.24.0
                           Used for OTel mapping validation

    Special Handling:
        - Empty --include from Makefile is cleaned up (converted to empty list)
        - This allows Makefile to pass --include ${VAR} even when VAR is empty

    Example Usage:
        >>> # Standard generation
        >>> args = argument_parser()
        >>> # python generator.py --semconv-version v1.24.0

        >>> # With all options
        >>> # python generator.py \\
        >>> #   --ref v8.10.0 \\
        >>> #   --include custom/schemas/ \\
        >>> #   --subset subsets/minimal.yml \\
        >>> #   --strict \\
        >>> #   --semconv-version v1.24.0

    Note:
        --semconv-version is required. The main() function will raise KeyError
        if not provided.
    """
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
    """Read ECS version string from file or git reference.

    Determines the ECS version to use for generated artifacts. Version can
    come from either:
    - Local 'version' file (default)
    - Git ref's 'version' file (when --ref specified)

    Args:
        ref: Optional git reference (tag/branch/commit) to load version from

    Returns:
        ECS version string (e.g., '8.11.0')

    Side Effects:
        Prints message indicating version source (local files vs git ref)

    Version Sources:
        - ref=None: Reads from './version' file in current directory
        - ref='v8.10.0': Reads from 'version' file in that git ref

    Processing:
        - Reads version file content
        - Strips trailing whitespace/newlines
        - Returns clean version string

    Example:
        >>> # Reading from local file
        >>> version = read_version()
        Loading schemas from local files
        >>> print(version)
        8.11.0

        >>> # Reading from git tag
        >>> version = read_version('v8.10.0')
        Loading schemas from git ref v8.10.0
        >>> print(version)
        8.10.0

    Note:
        Main() appends '+exp' to the version if experimental schemas are
        included via --include experimental/schemas.

    Used By:
        - main(): To determine version for all generated artifacts
        - All generators: Version appears in metadata, headers, filenames
    """
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
