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

"""Schema Exclude Filter Module.

This module explicitly removes specified fieldsets and fields from schemas.
It's the inverse of subset filtering - while subsets specify what to INCLUDE,
excludes specify what to REMOVE.

Exclude filters run after subset filters in the pipeline and are used for:
    - **Deprecation testing**: Remove fields to test impact before actual removal
    - **Impact analysis**: See what breaks when fields are removed
    - **Custom deployments**: Remove unwanted fieldsets entirely
    - **Security**: Exclude fields with sensitive data
    - **Performance testing**: Remove expensive fields to measure impact

Exclude Definition Format:
    Excludes are defined as YAML arrays of fieldsets/fields to remove:

    ```yaml
    - name: http
      fields:
        - name: request.referrer  # Remove specific field
        - name: response.body     # Remove another field

    - name: geo
      fields:
        - name: location  # Remove nested field
    ```

Removal Behavior:
    - Specified fields: Removed from schema
    - Parent fields: Removed if all children removed (except 'base')
    - Nested removal: Can remove deeply nested fields
    - 'base' protection: Never auto-remove base fieldset

Exclude vs Subset:
    - Subset: Whitelist approach (specify what to keep)
    - Exclude: Blacklist approach (specify what to remove)
    - Can use both: Subset first (include only X), then exclude (remove Y from X)

Example:
    >>> from schema import loader, cleaner, finalizer, exclude_filter
    >>> fields = loader.load_schemas()
    >>> cleaner.clean(fields)
    >>> finalizer.finalize(fields)
    >>> filtered = exclude_filter.exclude(
    ...     fields,
    ...     ['excludes/deprecated.yml']
    ... )
    # specified fields removed from schema

Common Use Case - Testing Deprecation:
    Before removing a field from ECS, create an exclude file and test:
    1. Generate schemas with field excluded
    2. Run test suite to find breakages
    3. Update affected code
    4. Finally remove field from actual schemas

See also: scripts/docs/schema-pipeline.md for pipeline documentation
"""

from typing import (
    Dict,
    List,
)

from schema import loader
from ecs_types import (
    Field,
    FieldEntry,
    FieldNestedEntry,
)


def exclude(fields: Dict[str, FieldEntry], exclude_file_globs: List[str]) -> Dict[str, FieldEntry]:
    """Remove specified fields from schema.

    Main entry point for exclude filtering. Loads exclude definitions and
    removes matching fields from the field dictionary.

    Args:
        fields: Complete field dictionary (typically after subset filtering)
        exclude_file_globs: List of paths/globs to exclude definition YAML files

    Returns:
        Modified field dictionary with excluded fields removed

    Side Effects:
        Modifies fields dictionary in place (also returns it)

    Processing:
        1. Load exclude definition files
        2. For each exclude list, traverse and remove specified fields
        3. Auto-remove parent fields if all children removed (except 'base')

    Example:
        >>> fields = exclude(all_fields, ['excludes/deprecated.yml'])
        # Fields specified in deprecated.yml are removed
    """
    excludes: List[FieldNestedEntry] = load_exclude_definitions(exclude_file_globs)

    if excludes:
        fields = exclude_fields(fields, excludes)

    return fields


def long_path(path_as_list: List[str]) -> str:
    """Convert path array to dotted string.

    Args:
        path_as_list: Array of path components

    Returns:
        Dot-joined path string

    Example:
        >>> long_path(['http', 'request', 'method'])
        'http.request.method'
    """
    return '.'.join([e for e in path_as_list])


def pop_field(
    fields: Dict[str, FieldEntry],
    node_path: List[str],
    path: List[str],
    removed: List[str]
) -> str:
    """Recursively remove a field at specified path.

    Traverses nested field structure and removes the field at the end of the
    path. Auto-removes parent fields if they become empty (except 'base').

    Args:
        fields: Field dictionary to modify
        node_path: Remaining path components to traverse
        path: Complete original path (for error messages)
        removed: List of already removed paths (to avoid duplicate errors)

    Returns:
        Flat name of removed field

    Raises:
        ValueError: If path not found and not already removed

    Behavior:
        - Leaf field: Remove it
        - Parent field: Recurse to child, then remove parent if empty
        - 'base' exception: Never auto-remove base fieldset even if empty

    Note:
        Modifies fields dict in place. Tracks removed paths to handle
        parent removal gracefully.
    """
    if node_path[0] in fields:
        if len(node_path) == 1:
            flat_name: str = long_path(path)
            fields.pop(node_path[0])
            return flat_name
        else:
            inner_field: str = node_path.pop(0)
            if 'fields' in fields[inner_field]:
                popped: str = pop_field(fields[inner_field]['fields'], node_path, path, removed)
                # if object field with no remaining fields and not 'base', pop it
                if fields[inner_field]['fields'] == {} and inner_field != 'base':
                    fields.pop(inner_field)
                return popped
            else:
                raise ValueError(
                    '--exclude specified, but no path to field {} found'.format(long_path(path)))
    else:
        this_long_path: str = long_path(path)
        # Check in case already removed parent
        if not any([this_long_path.startswith(long_path) for long_path in removed if long_path != None]):
            raise ValueError('--exclude specified, but no field {} found'.format(this_long_path))


def exclude_trace_path(
    fields: Dict[str, FieldEntry],
    item: List[Field],
    path: List[str],
    removed: List[str]
) -> None:
    """Traverse and remove fields specified in exclude list.

    Processes an array of field specifications from an exclude definition,
    removing each one and tracking what was removed.

    Args:
        fields: Field dictionary to modify
        item: List of field specifications to remove
        path: Current path prefix
        removed: List tracking removed field paths

    Raises:
        ValueError: If exclude item has 'fields' (nested excludes not supported)

    Note:
        Exclude definitions specify fields to remove, not nested structures.
        Each item should be a leaf field path, not a container with sub-fields.
    """
    for list_item in item:
        node_path: List[str] = path.copy()
        # cater for name.with.dots
        for name in list_item['name'].split('.'):
            node_path.append(name)
        if not 'fields' in list_item:
            parent: str = node_path[0]
            removed.append(pop_field(fields, node_path, node_path.copy(), removed))
            # if parent field has no remaining fields and not 'base', pop it
            if parent != 'base' and parent in fields and len(fields[parent]['fields']) == 0:
                fields.pop(parent)
        else:
            raise ValueError('--exclude specified, can\'t parse fields in file {}'.format(item))


def exclude_fields(fields: Dict[str, FieldEntry], excludes: List[FieldNestedEntry]) -> Dict[str, FieldEntry]:
    """Apply all exclude definitions to field dictionary.

    Iterates through exclude definitions and removes matching fields.

    Args:
        fields: Field dictionary to modify
        excludes: List of exclude definition documents

    Returns:
        Modified field dictionary (also modified in place)

    Processing:
        For each exclude document:
        - For each fieldset item in document:
          - Remove specified fields from that fieldset
          - Clean up empty parents
    """
    if excludes:
        for ex_list in excludes:
            for item in ex_list:
                exclude_trace_path(fields, item['fields'], [item['name']], [])
    return fields


def load_exclude_definitions(file_globs: List[str]) -> List[FieldNestedEntry]:
    """Load exclude definition files from filesystem.

    Args:
        file_globs: List of file paths or glob patterns

    Returns:
        List of parsed exclude definition documents

    Raises:
        ValueError: If file_globs specified but no files found

    Note:
        Returns empty list if file_globs is empty/None (no exclusions).
    """
    if not file_globs:
        return []
    excludes: List[FieldNestedEntry] = loader.load_definitions(file_globs)
    if not excludes:
        raise ValueError('--exclude specified, but no exclusions found in {}'.format(file_globs))
    return excludes
