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

"""Field Visitor Module.

This module provides utilities for traversing deeply nested field structures using
the Visitor pattern. It enables performing operations on all fields/fieldsets in a
schema tree without needing to write recursive traversal code repeatedly.

The Visitor Pattern:
    The visitor pattern separates algorithms (visitor functions) from the data
    structure they operate on. This allows:
    - Multiple operations without modifying the field structure
    - Consistent traversal order across different operations
    - Clean separation of concerns
    - Reusable traversal logic

Common Use Cases:
    - Validation: Check all fields meet requirements (cleaner.py)
    - Transformation: Modify field properties (finalizer.py)
    - Accumulation: Collect fields into flat structures (intermediate_files.py)
    - Enrichment: Add calculated properties to fields (finalizer.py)
    - Analysis: Generate statistics about schema structure

Visitor Functions:
    1. visit_fields(): Call different functions for fieldsets vs fields
    2. visit_fields_with_path(): Track nesting path during traversal
    3. visit_fields_with_memo(): Pass accumulator through traversal

Structure Assumptions:
    All visitor functions expect the deeply nested structure created by loader.py:
    - Fieldsets have 'schema_details', 'field_details', and 'fields' keys
    - Regular fields have 'field_details' and optionally 'fields' keys
    - Intermediate fields have 'field_details' with intermediate=True

Example Usage:
    >>> # Count all fields
    >>> count = {'total': 0}
    >>> def counter(details, memo):
    ...     memo['total'] += 1
    >>> visit_fields_with_memo(fields, counter, count)
    >>> print(count['total'])

    >>> # Validate all fields
    >>> def validator(details):
    ...     if 'type' not in details['field_details']:
    ...         raise ValueError('Missing type')
    >>> visit_fields(fields, field_func=validator)

See also: scripts/docs/schema-pipeline.md for pipeline documentation
"""

from typing import (
    Callable,
    Dict,
    List,
    Optional,
)

from ecs_types import (
    Field,
    FieldDetails,
    FieldEntry,
)


def visit_fields(
    fields: Dict[str, FieldEntry],
    fieldset_func: Optional[Callable[[FieldEntry], None]] = None,
    field_func: Optional[Callable[[FieldDetails], None]] = None
) -> None:
    """Recursively visit all fieldsets and fields, calling appropriate functions.

    Traverses the deeply nested field structure and invokes different callback
    functions for fieldsets (which have schema_details) vs regular fields.
    This allows different processing logic for different node types.

    Args:
        fields: Deeply nested field dictionary to traverse
        fieldset_func: Optional function to call for each fieldset.
                      Receives dict with 'schema_details', 'field_details', 'fields'
        field_func: Optional function to call for each field.
                   Receives dict with 'field_details' and optionally 'fields'

    Traversal Order:
        - Depth-first traversal (process parent before children)
        - Processes current node first, then recursively processes children
        - For each node: call appropriate function, then recurse into 'fields'

    Node Identification:
        - Fieldset: Has 'schema_details' key (top-level schemas only)
        - Field: Has 'field_details' key but no 'schema_details'

    Example:
        >>> def validate_fieldset(details):
        ...     if 'title' not in details['schema_details']:
        ...         raise ValueError('Missing title')
        >>>
        >>> def validate_field(details):
        ...     if 'type' not in details['field_details']:
        ...         raise ValueError('Missing type')
        >>>
        >>> visit_fields(fields,
        ...             fieldset_func=validate_fieldset,
        ...             field_func=validate_field)

    Use Cases:
        - cleaner.py: Validates and normalizes fieldsets and fields separately
        - finalizer.py: Sets original_fieldset on reused fields
        - Any operation needing different logic for fieldsets vs fields

    Note:
        Both callback functions are optional. You can provide just one if you
        only need to process fieldsets or fields.
    """
    for (_, details) in fields.items():
        if fieldset_func and 'schema_details' in details:
            fieldset_func(details)
        elif field_func and 'field_details' in details:
            field_func(details)
        if 'fields' in details:
            visit_fields(details['fields'],
                         fieldset_func=fieldset_func,
                         field_func=field_func)


def visit_fields_with_path(
    fields: Dict[str, FieldEntry],
    func: Callable[[FieldDetails], None],
    path: Optional[List[str]] = []
) -> None:
    """Recursively visit all fields, passing the nesting path to the callback.

    Traverses the deeply nested structure and calls the provided function for
    each field and fieldset, passing both the details and the path array showing
    where in the hierarchy the field is located.

    Args:
        fields: Deeply nested field dictionary to traverse
        func: Callback function receiving (details, path)
              - details: Dict with 'field_details' and optionally 'fields'
              - path: List of field names from root to current location
        path: Current path (used internally during recursion, start with [])

    Path Building:
        - Root fieldsets (root=true): Don't add to path
        - Other fieldsets/fields: Add their name to path
        - Path represents dotted field name: ['http', 'request'] = 'http.request'

    Traversal Order:
        - Depth-first traversal
        - Process current node first, then recurse into children

    Example:
        >>> def show_path(details, path):
        ...     field_name = details['field_details'].get('name', 'unknown')
        ...     dotted_path = '.'.join(path + [field_name])
        ...     print(f"Field: {dotted_path}")
        >>>
        >>> visit_fields_with_path(fields, show_path)
        Field: http
        Field: http.request
        Field: http.request.method
        Field: http.request.bytes

    Use Cases:
        - finalizer.py: Calculate flat_name using path
        - Any operation needing to know field's full path
        - Building dotted field names during transformation

    Note:
        Root fieldsets don't add to the path because their fields appear at
        the root level of events (e.g., '@timestamp', not 'base.@timestamp').
    """
    for (name, details) in fields.items():
        if 'field_details' in details:
            func(details, path)
        if 'fields' in details:
            if 'schema_details' in details and details['schema_details']['root']:
                new_nesting = []
            else:
                new_nesting = [name]
            visit_fields_with_path(details['fields'], func, path + new_nesting)


def visit_fields_with_memo(
    fields: Dict[str, FieldEntry],
    func: Callable[[FieldEntry, Field], None],
    memo: Optional[Dict[str, Field]] = None
) -> None:
    """Recursively visit all fields, passing an accumulator (memo) to the callback.

    Traverses the deeply nested structure and calls the provided function for
    each field and fieldset, passing both the details and a memo object that
    can be used to accumulate results or state during traversal.

    Args:
        fields: Deeply nested field dictionary to traverse
        func: Callback function receiving (details, memo)
              - details: Dict with 'field_details' and optionally 'fields'
              - memo: Accumulator object passed through all calls
        memo: Accumulator object (can be dict, list, or any mutable object)

    Memo Pattern:
        The memo object is passed to every callback and can be modified in place
        to accumulate results. Common memo types:
        - Dict: Accumulate fields by name
        - List: Collect fields meeting criteria
        - Counter dict: Track statistics

    Traversal Order:
        - Depth-first traversal
        - Process current node first, then recurse into children
        - Same memo object passed to all callbacks

    Example:
        >>> # Accumulate all keyword fields
        >>> keyword_fields = {}
        >>> def collect_keywords(details, memo):
        ...     field = details['field_details']
        ...     if field.get('type') == 'keyword':
        ...         memo[field['flat_name']] = field
        >>>
        >>> visit_fields_with_memo(fields, collect_keywords, keyword_fields)
        >>> len(keyword_fields)
        450  # Number of keyword fields found

    Use Cases:
        - intermediate_files.py: Accumulate fields into flat dictionary
        - Collecting fields for analysis or statistics
        - Building indexes or lookup tables during traversal
        - Any operation needing to build results while traversing

    Note:
        The memo is mutable and shared across all callbacks. Be careful not
        to accidentally mutate it in unexpected ways.
    """
    for (name, details) in fields.items():
        if 'field_details' in details:
            func(details, memo)
        if 'fields' in details:
            visit_fields_with_memo(details['fields'], func, memo)
