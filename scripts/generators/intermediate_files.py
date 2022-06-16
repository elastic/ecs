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

import copy
from os.path import join
from typing import (
    Dict,
    Tuple,
)

from schema import visitor
from generators import ecs_helpers
from _types import (
    Field,
    FieldEntry,
    FieldNestedEntry,
)


def generate(
    fields: Dict[str, FieldEntry],
    out_dir: str,
    default_dirs: bool
) -> Tuple[Dict[str, FieldNestedEntry], Dict[str, Field]]:
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
    """Generate ecs_flat.yml"""
    filtered: Dict[str, FieldEntry] = remove_non_root_reusables(fields)
    flattened: Dict[str, Field] = {}
    visitor.visit_fields_with_memo(filtered, accumulate_field, flattened)
    return flattened


def accumulate_field(details: FieldEntry, memo: Field) -> None:
    """Visitor function that accumulates all field details in the memo dict"""
    if 'schema_details' in details or ecs_helpers.is_intermediate(details):
        return
    field_details: Field = copy.deepcopy(details['field_details'])
    remove_internal_attributes(field_details)

    flat_name = field_details['flat_name']
    memo[flat_name] = field_details


def generate_nested_fields(fields: Dict[str, FieldEntry]) -> Dict[str, FieldNestedEntry]:
    """Generate ecs_nested.yml"""
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
    """Remove attributes only relevant to the deeply nested structure, but not to ecs_flat/nested.yml."""
    field_details.pop('node_name', None)
    field_details.pop('intermediate', None)


def remove_non_root_reusables(fields_nested: Dict[str, FieldEntry]) -> Dict[str, FieldEntry]:
    """
    Remove field sets that have top_level=false from the root of the field definitions.

    This attribute means they're only meant to be in the "reusable/expected" locations
    and not at the root of user's events.

    This is only relevant for the 'flat' field representation. The nested one
    still needs to keep all field sets at the root of the YAML file, as it
    the official information about each field set. It's the responsibility of
    users consuming ecs_nested.yml to skip the field sets with top_level=false.
    """
    fields: Dict[str, FieldEntry] = {}
    for (name, field) in fields_nested.items():
        if 'reusable' not in field['schema_details'] or field['schema_details']['reusable']['top_level']:
            fields[name] = field
    return fields
