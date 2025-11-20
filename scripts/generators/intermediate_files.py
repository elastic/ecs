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

"""Intermediate File Generator.

This module generates standardized intermediate representations of ECS schemas
that serve as the foundation for all other output formats. It produces two
key representations:

1. **Flat Format** (ecs_flat.yml): Single-level dictionary of all fields
   - Keys: Full dotted field names (e.g., 'http.request.method')
   - Values: Complete field definitions with metadata
   - Used by: CSV generator, some template generators
   - Excludes: Non-root reusable fieldsets (top_level=false)

2. **Nested Format** (ecs_nested.yml): Hierarchical grouping by fieldset
   - Keys: Fieldset names (e.g., 'http', 'user', 'process')
   - Values: Fieldset metadata plus nested 'fields' dictionary
   - Used by: Markdown generator, Elasticsearch templates, Beats
   - Includes: All fieldsets regardless of top_level setting

These intermediate formats provide a stable, normalized interface between
schema processing and artifact generation. This separation allows:
- Multiple generators to consume the same standardized data
- Schema evolution without breaking downstream generators
- Easy debugging of the transformation pipeline

Key Components:
    - generate(): Main entry point producing both formats
    - generate_flat_fields(): Creates flat field dictionary
    - generate_nested_fields(): Creates nested fieldset hierarchy
    - Visitor pattern: Used for efficient field traversal

Output Files:
    - generated/ecs/ecs.yml: Raw processed schemas (debugging only)
    - generated/ecs/ecs_flat.yml: Flat field representation
    - generated/ecs/ecs_nested.yml: Nested fieldset representation

See also: scripts/docs/intermediate-files.md for detailed documentation
"""

import copy
from os.path import join
from typing import (
    Dict,
    Tuple,
)

from schema import visitor
from generators import ecs_helpers
from ecs_types import (
    Field,
    FieldEntry,
    FieldNestedEntry,
)


def generate(
    fields: Dict[str, FieldEntry],
    out_dir: str,
    default_dirs: bool
) -> Tuple[Dict[str, FieldNestedEntry], Dict[str, Field]]:
    """Generate all intermediate file representations from processed schemas.
    
    This is the main entry point for intermediate file generation. It orchestrates
    the creation of both flat and nested representations and saves them to YAML
    files. These files serve as the normalized interface for all downstream
    generators.
    
    Args:
        fields: Processed field entries from schema loader/cleaner/finalizer
        out_dir: Output directory path (typically 'generated/ecs')
        default_dirs: If True, also save raw ecs.yml for debugging
    
    Returns:
        Tuple of (nested, flat) dictionaries:
        - nested: Fieldsets organized hierarchically with metadata
        - flat: All fields in single-level dictionary by dotted name
    
    Generates files:
        - {out_dir}/ecs_flat.yml: Flat field representation
        - {out_dir}/ecs_nested.yml: Nested fieldset representation
        - {out_dir}/ecs.yml: Raw fields (only if default_dirs=True)
    
    Note:
        Creates output directory if it doesn't exist.
        The returned dictionaries are also used directly by some generators
        without reading back from the YAML files.
    
    Example:
        >>> from schema import loader, cleaner, finalizer
        >>> fields = loader.load_schemas()
        >>> cleaner.clean(fields)
        >>> finalizer.finalize(fields)
        >>> nested, flat = generate(fields, 'generated/ecs', True)
        >>> len(flat)  # Number of fields in flat representation
        850
        >>> len(nested)  # Number of fieldsets
        45
    """
    ecs_helpers.make_dirs(join(out_dir))

    # Should only be used for debugging ECS development
    if default_dirs:
        ecs_helpers.yaml_dump(join(out_dir, 'ecs.yml'), fields)
    flat: Dict[str, Field] = generate_flat_fields(fields)
    nested: Dict[str, FieldNestedEntry] = generate_nested_fields(fields)

    ecs_helpers.yaml_dump(join(out_dir, 'ecs_flat.yml'), flat)
    ecs_helpers.yaml_dump(join(out_dir, 'ecs_nested.yml'), nested)
    return nested, flat


def generate_flat_fields(fields: Dict[str, FieldEntry]) -> Dict[str, Field]:
    """Generate flat field representation mapping dotted names to field definitions.
    
    Creates a single-level dictionary where every field (including nested ones)
    is represented by its full dotted name as the key. This format is useful for:
    - Quick field lookups by name
    - CSV generation
    - Simple iteration over all fields
    
    Args:
        fields: Processed field entries from schema pipeline
    
    Returns:
        Dictionary mapping field flat_names to field definitions:
        {
            'http.request.method': {
                'name': 'method',
                'flat_name': 'http.request.method',
                'type': 'keyword',
                'description': '...',
                ...
            },
            ...
        }
    
    Processing steps:
        1. Filter out non-root reusable fieldsets (top_level=false)
        2. Use visitor pattern to traverse all fields
        3. Accumulate fields in flat dictionary
        4. Remove internal-only attributes
    
    Note:
        - Excludes intermediate fields (used only for nesting)
        - Excludes fieldsets marked with top_level=false
        - Each field appears only once by its canonical flat_name
    
    Example:
        >>> flat = generate_flat_fields(fields)
        >>> flat['http.request.method']['type']
        'keyword'
        >>> list(flat.keys())[:3]
        ['@timestamp', 'agent.build.original', 'agent.ephemeral_id']
    """
    filtered: Dict[str, FieldEntry] = remove_non_root_reusables(fields)
    flattened: Dict[str, Field] = {}
    visitor.visit_fields_with_memo(filtered, accumulate_field, flattened)
    return flattened


def accumulate_field(details: FieldEntry, memo: Field) -> None:
    """Visitor callback that accumulates field definitions in a flat dictionary.
    
    This function is called by the visitor pattern for each field encountered
    during traversal. It extracts the field definition, cleans it, and adds
    it to the memo dictionary using the flat_name as the key.
    
    Args:
        details: Field entry containing field_details and possibly schema_details
        memo: Dictionary being accumulated with field definitions (modified in place)
    
    Behavior:
        - Skips schema-level entries (fieldset definitions)
        - Skips intermediate fields (used only for structure, not actual fields)
        - Deep copies field details to avoid mutation
        - Removes internal attributes not needed in output
        - Adds field to memo dictionary by flat_name
    
    Note:
        This is a callback function used with visitor.visit_fields_with_memo().
        It modifies the memo dictionary in place rather than returning a value.
    
    Example:
        >>> memo = {}
        >>> field_entry = {
        ...     'field_details': {
        ...         'flat_name': 'http.request.method',
        ...         'name': 'method',
        ...         'type': 'keyword',
        ...         'node_name': 'method',  # Will be removed
        ...         'intermediate': False   # Will be removed
        ...     }
        ... }
        >>> accumulate_field(field_entry, memo)
        >>> 'http.request.method' in memo
        True
        >>> 'node_name' in memo['http.request.method']
        False
    """
    if 'schema_details' in details or ecs_helpers.is_intermediate(details):
        return
    field_details: Field = copy.deepcopy(details['field_details'])
    remove_internal_attributes(field_details)

    flat_name = field_details['flat_name']
    memo[flat_name] = field_details


def generate_nested_fields(fields: Dict[str, FieldEntry]) -> Dict[str, FieldNestedEntry]:
    """Generate nested fieldset representation with hierarchical structure.
    
    Creates a dictionary where each fieldset is a top-level entry containing:
    - Fieldset metadata (name, title, description, group, etc.)
    - Schema details (reusability, nesting information)
    - Nested 'fields' dictionary with all fields in that fieldset
    
    This format preserves the logical grouping of fields by fieldset and
    includes metadata about how fieldsets relate to each other (reuse,
    nesting, etc.). Used by most generators including markdown docs.
    
    Args:
        fields: Processed field entries from schema pipeline
    
    Returns:
        Dictionary mapping fieldset names to fieldset definitions:
        {
            'http': {
                'name': 'http',
                'title': 'HTTP',
                'group': 2,
                'description': '...',
                'reusable': {...},
                'fields': {
                    'http.request.method': {...},
                    'http.response.status_code': {...},
                    ...
                }
            },
            ...
        }
    
    Processing steps:
        1. For each fieldset, merge field_details and schema_details
        2. Remove internal attributes (node_name, dashed_name, etc.)
        3. Use visitor to accumulate all fields in the fieldset
        4. Store fields in nested 'fields' dictionary
        5. Clean up conditional attributes (root=false removed)
    
    Note:
        - Includes ALL fieldsets, even those with top_level=false
        - Consumers of this format should check top_level flag themselves
        - Each fieldset's fields are in a flat dict (not hierarchical)
        - The "nesting" refers to grouping by fieldset, not field hierarchy
    
    Example:
        >>> nested = generate_nested_fields(fields)
        >>> nested['http']['title']
        'HTTP'
        >>> len(nested['http']['fields'])
        25
        >>> list(nested.keys())[:3]
        ['agent', 'as', 'base']
    """
    nested: Dict[str, FieldNestedEntry] = {}
    # Flatten each field set, but keep all resulting fields nested under their
    # parent/host field set.
    for (name, details) in fields.items():
        fieldset_details = {
            **copy.deepcopy(details['field_details']),
            **copy.deepcopy(details['schema_details'])
        }

        fieldset_details.pop('node_name')
        if 'reusable' in fieldset_details:
            fieldset_details['reusable'].pop('order')

        # TODO Temporarily removed to simplify initial rewrite review
        fieldset_details.pop('dashed_name')
        fieldset_details.pop('flat_name')
        if False == fieldset_details['root']:
            fieldset_details.pop('root')

        fieldset_fields = {}
        visitor.visit_fields_with_memo(details['fields'], accumulate_field, fieldset_fields)
        fieldset_details['fields'] = fieldset_fields

        nested[name] = fieldset_details
    return nested


# Helper functions


def remove_internal_attributes(field_details: Field) -> None:
    """Remove internal-only attributes from field definitions before output.
    
    Certain attributes are used during schema processing but aren't relevant
    in the final intermediate file outputs. This function removes them to
    keep the output files clean and focused on user-facing information.
    
    Args:
        field_details: Field definition dictionary (modified in place)
    
    Attributes removed:
        - node_name: Internal identifier used during tree traversal
        - intermediate: Flag for structural fields (not actual data fields)
    
    Note:
        Modifies the field_details dictionary in place.
        Uses pop() with None default to safely handle missing keys.
    
    Example:
        >>> field = {
        ...     'name': 'method',
        ...     'flat_name': 'http.request.method',
        ...     'type': 'keyword',
        ...     'node_name': 'method',      # Internal
        ...     'intermediate': False        # Internal
        ... }
        >>> remove_internal_attributes(field)
        >>> 'node_name' in field
        False
        >>> 'name' in field
        True
    """
    field_details.pop('node_name', None)
    field_details.pop('intermediate', None)


def remove_non_root_reusables(fields_nested: Dict[str, FieldEntry]) -> Dict[str, FieldEntry]:
    """Filter out fieldsets marked as non-root reusable (top_level=false).
    
    Some fieldsets are designed only to be reused in specific locations (via
    the reuse mechanism) and should never appear at the root level of events.
    For example, 'geo' might only be valid under 'client.geo', 'server.geo',
    etc., but not as standalone 'geo.*' fields at the event root.
    
    This filtering is ONLY applied to the flat representation, where having
    non-root fields at the top level would be confusing and incorrect. The
    nested representation keeps all fieldsets so consumers have complete
    information about each fieldset definition.
    
    Args:
        fields_nested: Complete dictionary of field entries
    
    Returns:
        Filtered dictionary containing only:
        - Fieldsets without 'reusable' metadata (always included)
        - Fieldsets with reusable.top_level=true
        
        Excludes:
        - Fieldsets with reusable.top_level=false
    
    Note:
        This implements an allow-list approach: fieldsets are included by
        default unless explicitly marked as non-root.
    
    Example:
        >>> fields = {
        ...     'http': {'schema_details': {}},  # No reusable - included
        ...     'geo': {'schema_details': {
        ...         'reusable': {'top_level': False}  # Excluded
        ...     }},
        ...     'user': {'schema_details': {
        ...         'reusable': {'top_level': True}  # Included
        ...     }}
        ... }
        >>> filtered = remove_non_root_reusables(fields)
        >>> 'http' in filtered
        True
        >>> 'geo' in filtered
        False
        >>> 'user' in filtered
        True
    """
    fields: Dict[str, FieldEntry] = {}
    for (name, field) in fields_nested.items():
        if 'reusable' not in field['schema_details'] or field['schema_details']['reusable']['top_level']:
            fields[name] = field
    return fields
