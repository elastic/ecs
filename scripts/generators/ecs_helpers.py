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

"""ECS Generator Helper Utilities.

Shared utilities for dictionary operations, file I/O, git access, list manipulation,
and field introspection. Used across all ECS generator scripts.

See scripts/docs/ecs-helpers.md for detailed documentation.
"""

import glob
import os
import yaml
import git
import pathlib
from typing import (
    Any,
    Dict,
    List,
    Optional,
    OrderedDict,
    Set,
    Union,
)
import warnings

from collections import OrderedDict
from copy import deepcopy
from ecs_types import (
    Field,
    FieldEntry,
    FieldNestedEntry,
)

# Dictionary helpers


def dict_copy_keys_ordered(dct: Field, copied_keys: List[str]) -> Field:
    """Copy specified keys in order. Keys not in source are skipped."""
    ordered_dict = OrderedDict()
    for key in copied_keys:
        if key in dct:
            ordered_dict[key] = dct[key]
    return ordered_dict


def dict_copy_existing_keys(source: Field, destination: Field, keys: List[str]) -> None:
    """Copy keys from source to destination if they exist in source."""
    for key in keys:
        if key in source:
            destination[key] = source[key]


def dict_sorted_by_keys(dct: FieldNestedEntry, sort_keys: List[str]) -> List[FieldNestedEntry]:
    """Sort dictionary values by one or more keys, returning sorted list."""
    if not isinstance(sort_keys, list):
        sort_keys = [sort_keys]

    tuples: List[List[Union[int, str, FieldNestedEntry]]] = []

    for key in dct:
        nested = dct[key]

        sort_criteria = []
        for sort_key in sort_keys:
            sort_criteria.append(nested[sort_key])
        sort_criteria.append(nested)
        tuples.append(sort_criteria)

    return list(map(lambda t: t[-1], sorted(tuples)))


def ordered_dict_insert(
    dct: Field,
    new_key: str, new_value: Union[str, bool],
    before_key: Optional[str] = None,
    after_key: Optional[str] = None
) -> None:
    """Insert key-value pair before or after specified key in ordered dict."""
    output = OrderedDict()
    inserted: bool = False
    for key, value in dct.items():
        if not inserted and before_key is not None and key == before_key:
            output[new_key] = new_value
            inserted = True
        output[key] = value
        if not inserted and after_key is not None and key == after_key:
            output[new_key] = new_value
            inserted = True
    if not inserted:
        output[new_key] = new_value
    dct.clear()
    for key, value in output.items():
        dct[key] = value


def safe_merge_dicts(a: Dict[Any, Any], b: Dict[Any, Any]) -> Dict[Any, Any]:
    """Merge two dicts, raising ValueError on duplicate keys."""
    c = deepcopy(a)
    for key in b:
        if key not in c:
            c[key] = b[key]
        else:
            raise ValueError('Duplicate key found when merging dictionaries: {0}'.format(key))
    return c


def fields_subset(subset, fields):
    """Extract a subset of fields based on subset specification.

    Recursively filters fields based on a subset specification, retaining
    only the fieldsets and fields specified in the subset definition.
    Used to generate partial ECS schemas (e.g., for specific use cases).

    Args:
        subset: Dictionary specifying which fieldsets/fields to include
        fields: Complete fields dictionary to filter

    Returns:
        Filtered fields dictionary containing only specified fields

    Raises:
        ValueError: If unsupported options found in subset specification

    Subset specification format:
        {
            'fieldset_name': {
                'fields': '*' | {'field1': {...}, 'field2': {...}}
            }
        }

    Behavior:
        - Missing 'fields' key = include all fields in fieldset
        - 'fields': '*' = include all fields in fieldset
        - 'fields': {...} = recursively apply subset to nested fields

    Example:
        >>> subset = {
        ...     'http': {'fields': '*'},  # All HTTP fields
        ...     'user': {'fields': {      # Only specific user fields
        ...         'name': {},
        ...         'email': {}
        ...     }}
        ... }
        >>> filtered = fields_subset(subset, all_fields)
        # Returns only http.* and user.name, user.email
    """
    retained_fields = {}
    allowed_options = ['fields']
    for key, val in subset.items():
        for option in val:
            if option not in allowed_options:
                raise ValueError('Unsupported option found in subset: {}'.format(option))
        # A missing fields key is shorthand for including all subfields
        if 'fields' not in val or val['fields'] == '*':
            retained_fields[key] = fields[key]
        elif isinstance(val['fields'], dict):
            # Copy the full field over so we get all the options, then replace the 'fields' with the right subset
            retained_fields[key] = fields[key]
            retained_fields[key]['fields'] = fields_subset(val['fields'], fields[key]['fields'])
    return retained_fields


def yaml_ordereddict(dumper, data):
    """YAML representer for OrderedDict that preserves key order.

    Custom YAML dumper function that serializes OrderedDict while maintaining
    the order of keys. Registered with PyYAML to automatically handle OrderedDict
    instances during yaml.dump().

    Args:
        dumper: YAML dumper instance
        data: OrderedDict to represent

    Returns:
        YAML MappingNode with keys in original order

    Note:
        Primarily for Python 2 compatibility. Python 3.7+ dicts maintain
        insertion order by default, making this less critical.
    """
    # YAML representation of an OrderedDict will be like a dictionary, but
    # respecting the order of the dictionary.
    # Almost sure it's unndecessary with Python 3.
    value = []
    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        value.append((node_key, node_value))
    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


# Register the representer globally
yaml.add_representer(OrderedDict, yaml_ordereddict)


def dict_clean_string_values(dict: Dict[Any, Any]) -> None:
    """Remove leading/trailing whitespace from all string values in dictionary.

    Cleans up string values by stripping whitespace, useful for normalizing
    field definitions loaded from YAML where formatting might vary.

    Args:
        dict: Dictionary to clean (modified in place)

    Note:
        - Only string values are modified
        - Non-string values (numbers, bools, nested dicts) are left unchanged
        - Modifies dictionary in place

    Example:
        >>> data = {'name': '  field  ', 'type': 'keyword', 'level': '  core  '}
        >>> dict_clean_string_values(data)
        >>> data
        {'name': 'field', 'type': 'keyword', 'level': 'core'}
    """
    for key in dict:
        value = dict[key]
        if isinstance(value, str):
            dict[key] = value.strip()


# File helpers


YAML_EXT = {'yml', 'yaml'}


def is_yaml(path: str) -> bool:
    """Check if a file path has a YAML extension.

    Determines if a file path ends with .yml or .yaml extension.

    Args:
        path: File path to check

    Returns:
        True if path has YAML extension, False otherwise

    Example:
        >>> is_yaml('schemas/http.yml')
        True
        >>> is_yaml('output.json')
        False
        >>> is_yaml('file.test.yaml')
        True
    """
    return set(path.split('.')[1:]).intersection(YAML_EXT) != set()


def safe_list(o: Union[str, List[str]]) -> List[str]:
    """Convert string or list to list, splitting on comma if needed.

    Normalizes input to a list format, useful for handling flexible
    function arguments that can be either strings or lists.

    Args:
        o: String (comma-separated) or list of strings

    Returns:
        List of strings

    Example:
        >>> safe_list(['a', 'b', 'c'])
        ['a', 'b', 'c']
        >>> safe_list('a,b,c')
        ['a', 'b', 'c']
        >>> safe_list('single')
        ['single']
    """
    if isinstance(o, list):
        return o
    else:
        return o.split(',')


def glob_yaml_files(paths: List[str]) -> List[str]:
    """Find all YAML files matching given paths, wildcards, or directories.

    Flexible file finder that handles:
    - Direct file paths (schemas/http.yml)
    - Wildcards (schemas/*.yml)
    - Directories (schemas/ -> all YAML files in dir)
    - Comma-separated strings ('path1,path2')

    Args:
        paths: String or list of paths/wildcards/directories

    Returns:
        Sorted list of matching YAML file paths

    Example:
        >>> glob_yaml_files(['schemas/http.yml', 'schemas/user.yml'])
        ['schemas/http.yml', 'schemas/user.yml']

        >>> glob_yaml_files(['schemas/'])
        ['schemas/agent.yml', 'schemas/base.yml', ...]

        >>> glob_yaml_files('schemas/*.yml')
        ['schemas/agent.yml', 'schemas/base.yml', ...]
    """
    all_files: List[str] = []
    for path in safe_list(paths):
        if is_yaml(path):
            all_files.extend(glob.glob(path))
        else:
            for t in YAML_EXT:
                all_files.extend(glob.glob(os.path.join(path, '*.' + t)))
    return sorted(all_files)


def get_tree_by_ref(ref: str) -> git.objects.tree.Tree:
    """Get git tree object for a specific reference (branch, tag, commit).

    Retrieves the file tree from the current repository at a specific git
    reference, allowing generators to load schemas from any point in history.

    Args:
        ref: Git reference (branch name, tag, commit SHA)

    Returns:
        Git tree object representing repository contents at that reference

    Example:
        >>> tree = get_tree_by_ref('v8.10.0')
        >>> tree['schemas']['http.yml']  # Access file from that version
    """
    repo: git.repo.base.Repo = git.Repo(os.getcwd())
    commit: git.objects.commit.Commit = repo.commit(ref)
    return commit.tree


def path_exists_in_git_tree(tree: git.objects.tree.Tree, file_path: str) -> bool:
    """Check if a path exists in a git tree object.

    Tests whether a file or directory exists in a git tree without raising
    an exception.

    Args:
        tree: Git tree object to check
        file_path: Path relative to tree root

    Returns:
        True if path exists in tree, False otherwise

    Example:
        >>> tree = get_tree_by_ref('main')
        >>> path_exists_in_git_tree(tree, 'schemas/http.yml')
        True
        >>> path_exists_in_git_tree(tree, 'nonexistent.yml')
        False
    """
    try:
        _ = tree[file_path]
    except KeyError:
        return False
    return True


def usage_doc_files() -> List[str]:
    """Get list of usage documentation files for fieldsets.

    Scans the docs/reference directory for usage documentation files
    following the pattern ecs-{fieldset}-usage.md.

    Returns:
        List of usage doc filenames (e.g., ['ecs-http-usage.md'])

    Note:
        Returns empty list if docs/reference directory doesn't exist.
        Used by markdown generator to link to usage docs when available.
    """
    usage_docs_dir: str = os.path.join(os.path.dirname(__file__), '../../docs/reference')
    usage_docs_path: pathlib.PosixPath = pathlib.Path(usage_docs_dir)
    if usage_docs_path.is_dir():
        return [x.name for x in usage_docs_path.glob('ecs-*-usage.md') if x.is_file()]
    return []


def ecs_files() -> List[str]:
    """Get list of ECS schema files to load.

    Returns sorted list of all YAML files in the schemas directory.
    This is the primary source of ECS field definitions.

    Returns:
        Sorted list of schema file paths

    Example:
        >>> ecs_files()
        ['schemas/agent.yml', 'schemas/base.yml', 'schemas/http.yml', ...]
    """
    schema_glob: str = os.path.join(os.path.dirname(__file__), '../../schemas/*.yml')
    return sorted(glob.glob(schema_glob))


def make_dirs(path: str) -> None:
    """Create directory and all parent directories if they don't exist.

    Safe wrapper around os.makedirs that handles existing directories
    gracefully and provides clear error messages on failure.

    Args:
        path: Directory path to create

    Raises:
        OSError: If directory creation fails (with descriptive message)

    Note:
        Uses exist_ok=True, so won't fail if directory already exists.

    Example:
        >>> make_dirs('generated/elasticsearch/composable/component')
        # Creates all missing parent directories
    """
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print('Unable to create output directory: {}'.format(e))
        raise e


def yaml_dump(
    filename: str,
    data: Dict[str, FieldNestedEntry],
    preamble: Optional[str] = None
) -> None:
    """Write data to a YAML file with optional preamble text.

    Serializes dictionary to YAML format with human-friendly formatting.
    Optionally prepends text (e.g., copyright header, comments).

    Args:
        filename: Path to output file
        data: Dictionary to serialize
        preamble: Optional text to write before YAML content

    Note:
        - Uses default_flow_style=False for readable multi-line format
        - Supports Unicode characters
        - Overwrites existing file

    Example:
        >>> yaml_dump('output.yml', {'name': 'test'}, '# Auto-generated\\n')
        # Creates file with comment header followed by YAML
    """
    with open(filename, 'w') as outfile:
        if preamble:
            outfile.write(preamble)
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)


def yaml_load(filename: str) -> Set[str]:
    """Load and parse a YAML file.

    Reads a YAML file and parses it into Python data structures using
    safe_load (prevents arbitrary code execution).

    Args:
        filename: Path to YAML file

    Returns:
        Parsed YAML content (typically dict or list)

    Note:
        Uses yaml.safe_load for security (no arbitrary code execution).

    Example:
        >>> data = yaml_load('schemas/http.yml')
        >>> data['name']
        'http'
    """
    with open(filename) as f:
        return yaml.safe_load(f.read())

# List helpers


def list_subtract(original: List[Any], subtracted: List[Any]) -> List[Any]:
    """Remove all elements of one list from another.

    Returns a new list containing elements from original that are not
    in subtracted. Useful for filtering lists.

    Args:
        original: List to subtract from
        subtracted: Elements to remove

    Returns:
        New list with subtracted elements removed

    Example:
        >>> list_subtract([1, 2, 3, 4, 5], [2, 4])
        [1, 3, 5]
        >>> list_subtract(['a', 'b', 'c'], ['b'])
        ['a', 'c']
    """
    return [item for item in original if item not in subtracted]


def list_extract_keys(lst: List[Field], key_name: str) -> List[str]:
    """Extract values for a specific key from a list of dictionaries.

    Builds a list of values by extracting the same key from each dictionary
    in the input list. Useful for converting list of objects to list of
    specific attribute values.

    Args:
        lst: List of dictionaries
        key_name: Key to extract from each dictionary

    Returns:
        List of values for the specified key

    Example:
        >>> fields = [
        ...     {'name': 'http', 'group': 2},
        ...     {'name': 'user', 'group': 1}
        ... ]
        >>> list_extract_keys(fields, 'name')
        ['http', 'user']
    """
    acc = []
    for d in lst:
        acc.append(d[key_name])
    return acc


# Helpers for the deeply nested fields structure


def is_intermediate(field: FieldEntry) -> bool:
    """Check if a field is an intermediate structural field (not a real data field).

    Intermediate fields exist only to provide hierarchical structure in schemas.
    They don't represent actual data fields and should be excluded from most
    output formats.

    Args:
        field: Field entry to check

    Returns:
        True if field is intermediate, False otherwise

    Example:
        >>> field = {'field_details': {'intermediate': True, 'name': 'request'}}
        >>> is_intermediate(field)
        True
        # 'http.request' is just structure, not a field

        >>> field = {'field_details': {'name': 'method', 'type': 'keyword'}}
        >>> is_intermediate(field)
        False
        # 'http.request.method' is an actual field
    """
    return ('intermediate' in field['field_details'] and field['field_details']['intermediate'])


def remove_top_level_reusable_false(ecs_nested: Dict[str, FieldNestedEntry]) -> Dict[str, FieldNestedEntry]:
    """Filter out fieldsets that should not appear at the root level.

    Returns a copy of ecs_nested excluding fieldsets with reusable.top_level=false.
    These fieldsets are meant to be used only in specific reuse locations, not
    at the event root.

    Args:
        ecs_nested: Dictionary of nested fieldsets

    Returns:
        Filtered dictionary excluding non-root fieldsets

    Example:
        >>> nested = {
        ...     'http': {'reusable': {'top_level': True}},
        ...     'geo': {'reusable': {'top_level': False}},  # Only for reuse
        ...     'user': {}  # No reusable setting = included
        ... }
        >>> filtered = remove_top_level_reusable_false(nested)
        >>> 'geo' in filtered
        False
        >>> 'http' in filtered and 'user' in filtered
        True
    """
    components: Dict[str, FieldNestedEntry] = {}
    for (fieldset_name, fieldset) in ecs_nested.items():
        if fieldset.get('reusable', None):
            if not fieldset['reusable']['top_level']:
                continue
        components[fieldset_name] = fieldset
    return components


# Warning helper


def strict_warning(msg: str) -> None:
    """Issue a warning that would be an error in strict mode.

    Generates a warning for issues that are tolerated in normal mode but would
    cause an exception when the generator is run with --strict flag. This allows
    schema developers to gradually fix issues without blocking the build.

    Args:
        msg: Custom warning message describing the issue

    Note:
        - Uses stacklevel=3 to show warning at caller's call site
        - Automatically adds boilerplate about strict mode
        - Warning will be converted to exception with --strict flag

    Example:
        >>> strict_warning("Field 'user.name' is missing description")
        UserWarning: Field 'user.name' is missing description

        This will cause an exception when running in strict mode.
        Warning check:
        ...
    """
    warn_message: str = f"{msg}\n\nThis will cause an exception when running in strict mode.\nWarning check:"
    warnings.warn(warn_message, stacklevel=3)
