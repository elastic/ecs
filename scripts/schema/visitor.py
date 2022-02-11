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

from typing import (
    Callable,
    Dict,
    List,
    Optional,
)

from .types import (
    Field,
    FieldDetails,
    FieldEntry,
)

def visit_fields(
    fields: Dict[str, FieldEntry],
    fieldset_func: Optional[Callable[[FieldEntry], None]] = None,
    field_func: Optional[Callable[[FieldDetails], None]] = None
) -> None:
    """
    This function navigates the deeply nested tree structure and runs provided
    functions on each fieldset or field encountered (both optional).

    The argument 'fields' should be at the named field grouping level:
    {'name': {'schema_details': {}, 'field_details': {}, 'fields': {}}

    The 'fieldset_func(details)' provided will be called for each field set,
    with the dictionary containing their details ({'schema_details': {}, 'field_details': {}, 'fields': {}).

    The 'field_func(details)' provided will be called for each field, with the dictionary
    containing the field's details ({'field_details': {}, 'fields': {}).
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
    """
    This function navigates the deeply nested tree structure and runs the provided
    function on all fields and field sets.

    The 'func' provided will be called for each field,
    with the dictionary containing their details ({'field_details': {}, 'fields': {})
    as well as the path array leading to the location of the field in question.
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
    """
    This function navigates the deeply nested tree structure and runs the provided
    function on all fields and field sets.

    The 'func' provided will be called for each field,
    with the dictionary containing their details ({'field_details': {}, 'fields': {})
    as well as the 'memo' you pass in.
    """
    for (name, details) in fields.items():
        if 'field_details' in details:
            func(details, memo)
        if 'fields' in details:
            visit_fields_with_memo(details['fields'], func, memo)
