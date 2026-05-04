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

Three depth-first traversal helpers for the deeply nested field structure from loader.py:
- visit_fields(): dispatch to fieldset_func or field_func based on node type
- visit_fields_with_path(): pass accumulated path array to callback
- visit_fields_with_memo(): pass shared accumulator to callback
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
    """Depth-first traversal calling fieldset_func for nodes with schema_details, field_func for others."""
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
    """Depth-first traversal passing accumulated path to func(details, path).

    Root fieldsets (root=true) don't add their name to the path.
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
    """Depth-first traversal passing a shared accumulator to func(details, memo)."""
    for (name, details) in fields.items():
        if 'field_details' in details:
            func(details, memo)
        if 'fields' in details:
            visit_fields_with_memo(details['fields'], func, memo)
