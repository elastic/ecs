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

"""Schema Loader Module.

This module is the entry point for the ECS schema processing pipeline. It loads
schema definitions from YAML files (either from filesystem or git) and transforms
them into a deeply nested structure that can be processed by downstream stages.

Loading Sources:
    1. **ECS Core Schemas**: From schemas/*.yml directory
    2. **Experimental Schemas**: From experimental/schemas/ (optional)
    3. **Custom Schemas**: User-provided schema files (optional)
    4. **Git References**: Load schemas from specific git tags/branches

The loading process:
    - Reads raw YAML schema files (arrays of fieldset definitions)
    - Transforms flat dotted field names into nested structures
    - Merges multiple schema sources together safely
    - Creates intermediate parent fields automatically (e.g., 'http.request')
    - Preserves minimal structure for downstream processing

Output Structure:
    The deeply nested structure returned looks like:

    {
        'schema_name': {
            'schema_details': {    # Fieldset-level metadata
                'reusable': {...},
                'root': bool,
                'group': int,
                'title': str
            },
            'field_details': {     # Field properties for the fieldset itself
                'name': str,
                'description': str,
                'type': 'group'
            },
            'fields': {            # Nested fields within this fieldset
                'field_name': {
                    'field_details': {...},
                    'fields': {...}  # Recursive nesting
                }
            }
        }
    }

Key Concepts:
    - **Deeply Nested**: Dotted names like 'http.request.method' become nested dicts
    - **Intermediate Fields**: Auto-created parent fields (e.g., 'http.request')
    - **Schema Merging**: Custom schemas can extend or override ECS schemas
    - **Minimal Defaults**: Only sets bare minimum; cleaner.py fills in rest

This module does NOT:
    - Validate field definitions (handled by cleaner.py)
    - Perform field reuse (handled by finalizer.py)
    - Calculate final field names (handled by finalizer.py)
    - Apply defaults beyond structure (handled by cleaner.py)

See also: scripts/docs/schema-pipeline.md for complete pipeline documentation
"""

import copy
import git
import glob
from typing import (
    Any,
    Dict,
    List,
    Optional,
)
import yaml

from generators import ecs_helpers
from ecs_types import (
    Field,
    FieldEntry,
    FieldNestedEntry,
    MultiField,
    SchemaDetails,
)


EXPERIMENTAL_SCHEMA_DIR = 'experimental/schemas'


def load_schemas(
    ref: Optional[str] = None,
    included_files: Optional[List[str]] = []
) -> Dict[str, FieldEntry]:
    """Load ECS schemas from filesystem or git, optionally including custom schemas.

    This is the main entry point for schema loading. It orchestrates loading from
    multiple sources and merges them into a unified deeply nested structure.

    Args:
        ref: Optional git reference (tag/branch/commit) to load schemas from.
             If None, loads from current filesystem.
        included_files: Optional list of additional schema files or directories
                       to include (e.g., custom schemas, experimental schemas)

    Returns:
        Dictionary mapping schema names to their deeply nested field structures.
        Each schema has 'schema_details', 'field_details', and 'fields' keys.

    Loading Order:
        1. Load ECS core schemas (from git ref or filesystem)
        2. If ref specified + experimental requested: Load experimental from git
        3. Load any remaining custom schema files from filesystem
        4. Merge all sources together (custom can override ECS)

    Raises:
        ValueError: If schema file has missing 'name' attribute
        KeyError: If git ref doesn't contain expected schema directory

    Note:
        - Experimental schemas are only loaded from git if --ref is specified
        - Custom schemas are always loaded from filesystem (not git)
        - Merging allows custom schemas to extend/override ECS definitions

    Example:
        >>> # Load current ECS schemas
        >>> fields = load_schemas()
        >>> len(fields)  # Number of fieldsets
        45

        >>> # Load from specific version with custom schemas
        >>> fields = load_schemas(ref='v8.10.0',
        ...                       included_files=['custom/myfields.yml'])
    """
    # ECS fields (from git ref or not)
    schema_files_raw: Dict[str, FieldNestedEntry] = load_schemas_from_git(
        ref) if ref else load_schema_files(ecs_helpers.ecs_files())
    fields: Dict[str, FieldEntry] = deep_nesting_representation(schema_files_raw)

    # Custom additional files
    if included_files and len(included_files) > 0:
        print('Loading user defined schemas: {0}'.format(included_files))
        # If --ref provided and --include loading experimental schemas
        if ref and EXPERIMENTAL_SCHEMA_DIR in included_files:
            exp_schema_files_raw: Dict[str, FieldNestedEntry] = load_schemas_from_git(
                ref, target_dir=EXPERIMENTAL_SCHEMA_DIR)
            exp_fields: Dict[str, FieldEntry] = deep_nesting_representation(exp_schema_files_raw)
            fields = merge_fields(fields, exp_fields)
            included_files.remove(EXPERIMENTAL_SCHEMA_DIR)
        # Remaining additional custom files (never from git ref)
        custom_files: List[str] = ecs_helpers.glob_yaml_files(included_files)
        custom_fields: Dict[str, FieldEntry] = deep_nesting_representation(load_schema_files(custom_files))
        fields = merge_fields(fields, custom_fields)
    return fields


def load_schema_files(files: List[str]) -> Dict[str, FieldNestedEntry]:
    """Load multiple schema YAML files from filesystem and merge them.

    Args:
        files: List of file paths to YAML schema files

    Returns:
        Dictionary mapping schema names to their raw (not yet nested) definitions

    Raises:
        ValueError: If duplicate schema names are found across files

    Note:
        Uses safe_merge_dicts to prevent accidental overwrites.
    """
    fields_nested: Dict[str, FieldNestedEntry] = {}
    for f in files:
        new_fields: Dict[str, FieldNestedEntry] = read_schema_file(f)
        fields_nested = ecs_helpers.safe_merge_dicts(fields_nested, new_fields)
    return fields_nested


def load_schemas_from_git(
    ref: str,
    target_dir: Optional[str] = 'schemas'
) -> Dict[str, FieldNestedEntry]:
    """Load schema files from a specific git reference.

    Checks out the specified git reference and reads all YAML files from the
    target directory without checking out files to the filesystem.

    Args:
        ref: Git reference (tag, branch, or commit SHA) to load from
        target_dir: Directory path within the git tree (default: 'schemas')

    Returns:
        Dictionary mapping schema names to their raw (not yet nested) definitions

    Raises:
        KeyError: If target directory doesn't exist in the git ref
        ValueError: If duplicate schema names are found

    Note:
        Reads files directly from git objects without filesystem checkout.

    Example:
        >>> schemas = load_schemas_from_git('v8.10.0')
        >>> schemas = load_schemas_from_git('main', target_dir='experimental/schemas')
    """
    tree: git.objects.tree.Tree = ecs_helpers.get_tree_by_ref(ref)
    fields_nested: Dict[str, FieldNestedEntry] = {}

    # Handles case if target dir doesn't exists in git ref
    if ecs_helpers.path_exists_in_git_tree(tree, target_dir):
        for blob in tree[target_dir].blobs:
            if blob.name.endswith('.yml'):
                new_fields: Dict[str, FieldNestedEntry] = read_schema_blob(blob, ref)
                fields_nested = ecs_helpers.safe_merge_dicts(fields_nested, new_fields)
    else:
        raise KeyError(f"Target directory './{target_dir}' not present in git ref '{ref}'!")
    return fields_nested


def read_schema_file(file_name: str) -> Dict[str, FieldNestedEntry]:
    """Read and parse a single YAML schema file from filesystem.

    Args:
        file_name: Path to YAML schema file

    Returns:
        Dictionary with schema name as key, schema definition as value

    Raises:
        ValueError: If schema is missing 'name' attribute
        yaml.YAMLError: If file contains invalid YAML

    Example:
        >>> schemas = read_schema_file('schemas/http.yml')
        >>> 'http' in schemas
        True
    """
    with open(file_name) as f:
        raw: List[FieldNestedEntry] = yaml.safe_load(f.read())
    return nest_schema(raw, file_name)


def read_schema_blob(
    blob: git.objects.blob.Blob,
    ref: str
) -> Dict[str, FieldNestedEntry]:
    """Read and parse a YAML schema from a git blob object.

    Args:
        blob: Git blob object containing YAML schema content
        ref: Git reference being loaded (for error messages)

    Returns:
        Dictionary with schema name as key, schema definition as value

    Raises:
        ValueError: If schema is missing 'name' attribute
        yaml.YAMLError: If blob contains invalid YAML

    Note:
        Constructs friendly file name for error messages: "http.yml (git ref v8.10.0)"
    """
    content: str = blob.data_stream.read().decode('utf-8')
    raw: List[FieldNestedEntry] = yaml.safe_load(content)
    file_name: str = "{} (git ref {})".format(blob.name, ref)
    return nest_schema(raw, file_name)


def nest_schema(raw: List[FieldNestedEntry], file_name: str) -> Dict[str, FieldNestedEntry]:
    """Transform raw schema array into dictionary keyed by schema name.

    Schema YAML files contain an array (list) of schema definitions. This
    function converts that array into a dictionary for easier access, using
    each schema's 'name' attribute as the key.

    Args:
        raw: List of schema definitions from YAML file
        file_name: Name of source file (for error messages)

    Returns:
        Dictionary mapping schema names to their definitions:
        {'http': {...}, 'user': {...}}

    Raises:
        ValueError: If any schema is missing the mandatory 'name' attribute

    Note:
        Most schema files contain exactly one schema, but multiple schemas
        per file are supported.

    Example:
        >>> raw = [{'name': 'http', 'title': 'HTTP', 'fields': [...]}]
        >>> nested = nest_schema(raw, 'http.yml')
        >>> nested
        {'http': {'name': 'http', 'title': 'HTTP', 'fields': [...]}}
    """
    fields: Dict[str, FieldNestedEntry] = {}
    for schema in raw:
        if 'name' not in schema:
            raise ValueError("Schema file {} is missing mandatory attribute 'name'".format(file_name))
        fields[schema['name']] = schema
    return fields


def deep_nesting_representation(fields: Dict[str, FieldNestedEntry]) -> Dict[str, FieldEntry]:
    """Transform flat schema definitions into deeply nested field structures.

    Takes schemas with flat field arrays and converts them into the deeply nested
    structure used by the rest of the pipeline. This involves:
    - Separating schema-level metadata from field-level metadata
    - Converting dotted field names into nested dictionaries
    - Creating intermediate parent fields automatically

    Args:
        fields: Dictionary of raw schema definitions with flat field arrays

    Returns:
        Dictionary mapping schema names to deeply nested structures with:
        - schema_details: Fieldset-level metadata (root, group, reusable, title)
        - field_details: Field properties for the fieldset itself
        - fields: Recursively nested field definitions

    Structure Transformation:
        Input (flat):
        {
            'http': {
                'name': 'http',
                'title': 'HTTP',
                'fields': [
                    {'name': 'request.method', 'type': 'keyword'},
                    {'name': 'response.status_code', 'type': 'long'}
                ]
            }
        }

        Output (deeply nested):
        {
            'http': {
                'schema_details': {'title': 'HTTP', ...},
                'field_details': {'name': 'http', ...},
                'fields': {
                    'request': {
                        'field_details': {'intermediate': True, ...},
                        'fields': {
                            'method': {
                                'field_details': {'type': 'keyword', ...}
                            }
                        }
                    }
                }
            }
        }

    Note:
        - Schema-level keys (root, group, reusable, title) go to schema_details
        - Everything else becomes field_details
        - Intermediate fields are auto-created for nesting paths
    """
    deeply_nested: Dict[str, FieldEntry] = {}
    for (name, flat_schema) in fields.items():

        # We destructively select what goes into schema_details and child fields.
        # The rest is 'field_details'.
        flat_schema = flat_schema.copy()
        flat_schema['node_name'] = flat_schema['name']

        # Schema-only details. Not present on other nested field groups.
        schema_details: SchemaDetails = {}
        for schema_key in ['root', 'group', 'reusable', 'title']:
            if schema_key in flat_schema:
                schema_details[schema_key] = flat_schema.pop(schema_key)

        nested_schema = nest_fields(flat_schema.pop('fields', []))
        # Re-assemble new structure
        deeply_nested[name] = {
            'schema_details': schema_details,
            # What's still in flat_schema is the field_details for the field set itself
            'field_details': flat_schema,
            'fields': nested_schema['fields']
        }
    return deeply_nested


def nest_fields(field_array: List[Field]) -> Dict[str, Dict[str, FieldEntry]]:
    """Convert flat array of fields with dotted names into nested structure.

    Takes a flat array of field definitions (where 'name' can contain dots like
    'request.method') and builds a nested dictionary structure. Automatically
    creates intermediate parent fields as needed.

    Args:
        field_array: List of field definitions with potentially dotted names

    Returns:
        Dictionary with 'fields' key containing nested field structure

    Field Nesting Logic:
        1. Split dotted names: 'request.method' -> ['request', 'method']
        2. Create intermediate fields for parents: 'request' becomes type='object'
        3. Mark intermediate fields so they can be identified later
        4. Preserve explicitly defined object/nested fields (not intermediate)
        5. Place leaf field at deepest nesting level

    Example:
        Input:
        [
            {'name': 'method', 'type': 'keyword'},
            {'name': 'request.method', 'type': 'keyword'},
            {'name': 'request.bytes', 'type': 'long'}
        ]

        Output:
        {
            'fields': {
                'method': {
                    'field_details': {'name': 'method', 'type': 'keyword'}
                },
                'request': {
                    'field_details': {
                        'name': 'request',
                        'type': 'object',
                        'intermediate': True  # Auto-created
                    },
                    'fields': {
                        'method': {...},
                        'bytes': {...}
                    }
                }
            }
        }

    Note:
        - Intermediate fields get type='object' and intermediate=True
        - Explicitly defined object/nested fields keep intermediate=False
        - node_name is set for all fields (used internally for tracking)
    """
    schema_root: Dict[str, Dict[str, FieldEntry]] = {'fields': {}}
    for field in field_array:
        nested_levels: List[str] = field['name'].split('.')
        parent_fields: List[str] = nested_levels[:-1]
        leaf_field: str = nested_levels[-1]
        # "nested_schema" is a cursor we move within the schema_root structure we're building.
        # Here we reset the cursor for this new field.
        nested_schema = schema_root['fields']

        current_path = []
        for idx, level in enumerate(parent_fields):
            nested_schema.setdefault(level, {})
            # Where nested fields will live
            nested_schema[level].setdefault('fields', {})

            # Make type:object explicit for intermediate parent fields
            nested_schema[level].setdefault('field_details', {})
            field_details = nested_schema[level]['field_details']
            field_details['node_name'] = level
            # Respect explicitly defined object fields
            if 'type' in field_details and field_details['type'] in ['object', 'nested']:
                field_details.setdefault('intermediate', False)
            else:
                field_details.setdefault('type', 'object')
                field_details.setdefault('name', '.'.join(parent_fields[:idx + 1]))
                field_details.setdefault('intermediate', True)

            # moving the nested_schema cursor deeper
            current_path.extend([level])
            nested_schema = nested_schema[level]['fields']
        nested_schema.setdefault(leaf_field, {})
        # Overwrite 'name' with the leaf field's name. The flat_name is already computed.
        field['node_name'] = leaf_field
        nested_schema[leaf_field]['field_details'] = field
    return schema_root


def array_of_maps_to_map(array_vals: List[MultiField]) -> Dict[str, MultiField]:
    """Convert array of multi-field definitions to dictionary keyed by name.

    Args:
        array_vals: List of multi-field definitions, each with a 'name' key

    Returns:
        Dictionary mapping multi-field names to their definitions

    Note:
        If duplicate names exist, the last one wins (useful for overrides).
    """
    ret_map: Dict[str, MultiField] = {}
    for map_val in array_vals:
        name: str = map_val['name']
        # if multiple name fields exist in the same custom definition this will take the last one
        ret_map[name] = map_val
    return ret_map


def map_of_maps_to_array(map_vals: Dict[str, MultiField]) -> List[MultiField]:
    """Convert dictionary of multi-fields back to sorted array.

    Args:
        map_vals: Dictionary of multi-field definitions

    Returns:
        Sorted list of multi-field definitions (sorted by name)
    """
    ret_list: List[MultiField] = []
    for key in map_vals:
        ret_list.append(map_vals[key])
    return sorted(ret_list, key=lambda k: k['name'])


def dedup_and_merge_lists(list_a: List[MultiField], list_b: List[MultiField]) -> List[MultiField]:
    """Merge two multi-field lists, removing duplicates and preferring list_b.

    When the same multi-field name appears in both lists, the definition from
    list_b takes precedence. This allows custom schemas to override ECS defaults.

    Args:
        list_a: First list of multi-field definitions (lower priority)
        list_b: Second list of multi-field definitions (higher priority)

    Returns:
        Merged and sorted list of unique multi-field definitions

    Example:
        >>> list_a = [{'name': 'text', 'type': 'text'}]
        >>> list_b = [{'name': 'keyword', 'type': 'keyword'}]
        >>> dedup_and_merge_lists(list_a, list_b)
        [{'name': 'keyword', ...}, {'name': 'text', ...}]  # Sorted by name
    """
    list_a_map: Dict[str, MultiField] = array_of_maps_to_map(list_a)
    list_a_map.update(array_of_maps_to_map(list_b))
    return map_of_maps_to_array(list_a_map)


def merge_fields(a: Dict[str, FieldEntry], b: Dict[str, FieldEntry]) -> Dict[str, FieldEntry]:
    """Recursively merge two field dictionaries, with b taking precedence.

    Performs deep merging of field structures, allowing custom schemas to extend
    or override ECS definitions. Handles special cases for arrays (normalize,
    multi_fields) and nested structures.

    Args:
        a: Base field dictionary (typically ECS fields)
        b: Override field dictionary (typically custom fields)

    Returns:
        New deeply nested field dictionary with merged content

    Merge Behavior:
        - New fieldsets in b: Added to result
        - Existing fieldsets: Merged recursively
        - field_details: b values override a values
        - normalize arrays: Concatenated (a + b)
        - multi_fields arrays: Merged with deduplication (b takes precedence)
        - schema_details: Merged with special handling for reusable settings
        - Nested fields: Merged recursively

    Special Cases:
        1. normalize: Arrays are concatenated, allowing additions
        2. multi_fields: Deduplicated merge (custom can override ECS multi-fields)
        3. reusable.expected: Arrays concatenated (adds new reuse locations)
        4. reusable.top_level: Last value wins (can change reusability)

    Example:
        >>> ecs = {
        ...     'user': {
        ...         'field_details': {'name': 'user', 'type': 'group'},
        ...         'fields': {
        ...             'name': {'field_details': {'type': 'keyword'}}
        ...         }
        ...     }
        ... }
        >>> custom = {
        ...     'user': {
        ...         'fields': {
        ...             'email': {'field_details': {'type': 'keyword'}}
        ...         }
        ...     }
        ... }
        >>> merged = merge_fields(ecs, custom)
        # Result has both user.name (from ECS) and user.email (from custom)

    Note:
        - Deep copies inputs to avoid mutation
        - Safe for merging experimental, custom, and ECS schemas
        - Used by load_schemas() to combine multiple schema sources
    """
    a = copy.deepcopy(a)
    b = copy.deepcopy(b)
    for key in b:
        if key not in a:
            a[key] = b[key]
            continue
        # merge field details
        if 'normalize' in b[key]['field_details']:
            a[key].setdefault('field_details', {})
            a[key]['field_details'].setdefault('normalize', [])
            a[key]['field_details']['normalize'].extend(b[key]['field_details'].pop('normalize'))
        if 'multi_fields' in b[key]['field_details']:
            a[key].setdefault('field_details', {})
            a[key]['field_details'].setdefault('multi_fields', [])
            a[key]['field_details']['multi_fields'] = dedup_and_merge_lists(
                a[key]['field_details']['multi_fields'], b[key]['field_details']['multi_fields'])
            # if we don't do this then the update call below will overwrite a's field_details, with the original
            # contents of b, which undoes our merging the multi_fields
            del b[key]['field_details']['multi_fields']
        a[key]['field_details'].update(b[key]['field_details'])
        # merge schema details
        if 'schema_details' in b[key]:
            asd = a[key]['schema_details']
            bsd = b[key]['schema_details']
            if 'reusable' in b[key]['schema_details']:
                asd.setdefault('reusable', {})
                if 'top_level' in bsd['reusable']:
                    asd['reusable']['top_level'] = bsd['reusable']['top_level']
                else:
                    asd['reusable'].setdefault('top_level', True)
                if 'order' in bsd['reusable']:
                    asd['reusable']['order'] = bsd['reusable']['order']
                asd['reusable'].setdefault('expected', [])
                asd['reusable']['expected'].extend(bsd['reusable']['expected'])
                bsd.pop('reusable')
            asd.update(bsd)
        # merge nested fields
        if 'fields' in b[key]:
            a[key].setdefault('fields', {})
            a[key]['fields'] = merge_fields(a[key]['fields'], b[key]['fields'])
    return a


def load_yaml_file(file_name):
    """Load and parse a YAML file.

    Args:
        file_name: Path to YAML file

    Returns:
        Parsed YAML content (typically dict or list)
    """
    with open(file_name) as f:
        return yaml.safe_load(f.read())


def warn(message: str) -> None:
    """Print a warning message (overridable for testing).

    Args:
        message: Warning message to display

    Note:
        This function exists to enable silent tests (can be mocked).
    """
    print(message)


def eval_globs(globs):
    """Expand glob patterns to actual file paths.

    Args:
        globs: Array of glob patterns or file names

    Returns:
        Array of actual file paths matching the patterns

    Note:
        Directories ending with '/' are converted to 'dir/*'
        Warns if a pattern matches no files.
    """
    all_files = []
    for g in globs:
        if g.endswith('/'):
            g += '*'
        new_files = glob.glob(g)
        if len(new_files) == 0:
            warn("{} did not match any files".format(g))
        else:
            all_files.extend(new_files)
    return all_files


def load_definitions(file_globs):
    """Load subset or exclude definition files.

    Args:
        file_globs: List of file paths or glob patterns

    Returns:
        List of loaded YAML definition objects

    Note:
        Used by subset_filter.py and exclude_filter.py to load their configs.
    """
    sets = []
    for f in ecs_helpers.glob_yaml_files(file_globs):
        raw = load_yaml_file(f)
        sets.append(raw)
    return sets
