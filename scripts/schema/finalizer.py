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

"""Schema Finalizer Module.

Third stage of the pipeline: loader.py → cleaner.py → finalizer.py → intermediate_files.py

Performs field reuse (composition) and calculates final field names.

Two-phase reuse:
- Phase 1 (foreign): Copy fieldset into a different fieldset. Transitive — if 'group' is in
  'user', then 'destination.user' also gets 'destination.user.group.*'.
- Phase 2 (self-nesting): Copy fieldset into itself (e.g., process → process.parent).
  NOT transitive — 'source.process.parent' does not exist even though process.parent does.

The 'order' attribute controls sequence: order=1 runs before order=2 (default). Within each
order, Phase 1 runs before Phase 2.

After reuse: calculates flat_name, dashed_name, and multi-field flat_names for all fields.
"""

import copy
import re

from schema import visitor


def finalize(fields):
    """Perform reuse and calculate final field names (flat_name, dashed_name)."""
    perform_reuse(fields)
    calculate_final_values(fields)


def order_reuses(fields):
    """Return (foreign_reuses, self_nestings) each as {order: {schema_name: [reuse_entries]}}.

    Foreign reuses go to a different fieldset; self_nestings stay within the same fieldset.
    """
    foreign_reuses = {}
    self_nestings = {}
    for schema_name, schema in fields.items():
        if not 'reusable' in schema['schema_details']:
            continue
        reuse_order = schema['schema_details']['reusable']['order']
        for reuse_entry in schema['schema_details']['reusable']['expected']:
            destination_schema_name = reuse_entry['full'].split('.')[0]
            if destination_schema_name == schema_name:
                # Accumulate self-nestings for phase 2.
                self_nestings.setdefault(reuse_order, {})
                self_nestings[reuse_order].setdefault(destination_schema_name, [])
                self_nestings[reuse_order][destination_schema_name].extend([reuse_entry])
            else:
                # Group foreign reuses by 'order' attribute.
                foreign_reuses.setdefault(reuse_order, {})
                foreign_reuses[reuse_order].setdefault(schema_name, [])
                foreign_reuses[reuse_order][schema_name].extend([reuse_entry])
    return foreign_reuses, self_nestings


def perform_reuse(fields):
    """Execute all field reuse, processing each order level with Phase 1 (foreign) then Phase 2 (self-nesting)."""
    foreign_reuses, self_nestings = order_reuses(fields)

    # Process foreign reuses and self-nestings together, respecting order
    all_orders = sorted(set(list(foreign_reuses.keys()) + list(self_nestings.keys())))

    for order in all_orders:
        # Phase 1: foreign reuse for this order
        if order in foreign_reuses:
            for schema_name, reuse_entries in foreign_reuses[order].items():
                schema = fields[schema_name]
                for reuse_entry in reuse_entries:
                    nest_as = reuse_entry['as']
                    destination_schema_name = reuse_entry['full'].split('.')[0]
                    destination_schema = fields[destination_schema_name]
                    ensure_valid_reuse(schema, destination_schema)

                    new_field_details = copy.deepcopy(schema['field_details'])
                    new_field_details['name'] = nest_as
                    new_field_details['original_fieldset'] = schema_name
                    new_field_details['intermediate'] = True
                    reused_fields = copy.deepcopy(schema['fields'])
                    set_original_fieldset(reused_fields, schema_name)
                    destination_fields = field_group_at_path(reuse_entry['at'], fields)
                    destination_fields[nest_as] = {
                        'field_details': new_field_details,
                        'fields': reused_fields,
                    }
                    append_reused_here(schema, reuse_entry, destination_schema)

        # Phase 2: self-nesting for this order
        if order in self_nestings:
            for schema_name, reuse_entries in self_nestings[order].items():
                schema = fields[schema_name]
                ensure_valid_reuse(schema)
                # Since we're about self-nest more fields within these, make a pristine copy first
                reused_fields = copy.deepcopy(schema['fields'])
                set_original_fieldset(reused_fields, schema_name)
                for reuse_entry in reuse_entries:
                    nest_as = reuse_entry['as']
                    new_field_details = copy.deepcopy(schema['field_details'])
                    new_field_details['name'] = nest_as
                    new_field_details['original_fieldset'] = schema_name
                    new_field_details['intermediate'] = True
                    # to handle multi-level self-nesting
                    if reuse_entry['at'] != schema_name:
                        destination_fields = field_group_at_path(reuse_entry['at'], fields)
                    else:
                        destination_fields = schema['fields']
                    destination_fields[nest_as] = {
                        'field_details': new_field_details,
                        # Make a new copy of the pristine copy
                        'fields': copy.deepcopy(reused_fields),
                    }
                    append_reused_here(schema, reuse_entry, fields[schema_name])


def ensure_valid_reuse(reused_schema, destination_schema=None):
    """Raise ValueError if either schema has root=true (root fieldsets cannot participate in reuse)."""
    if reused_schema['schema_details']['root']:
        msg = "Schema {} has attribute root=true and therefore cannot be reused.".format(
            reused_schema['field_details']['name'])
        raise ValueError(msg)
    elif destination_schema and destination_schema['schema_details']['root']:
        msg = "Schema {} has attribute root=true and therefore cannot have other field sets reused inside it.".format(
            destination_schema['field_details']['name'])
        raise ValueError(msg)


def append_reused_here(reused_schema, reuse_entry, destination_schema):
    """Record reuse metadata on destination_schema: appends to 'nestings' (legacy) and 'reused_here'."""
    # Legacy, too limited
    destination_schema['schema_details'].setdefault('nestings', [])
    destination_schema['schema_details']['nestings'] = sorted(
        destination_schema['schema_details']['nestings'] + [reuse_entry['full']]
    )
    # New roomier way: we could eventually include contextual description here
    destination_schema['schema_details'].setdefault('reused_here', [])
    reused_here_entry = {
        'schema_name': reused_schema['field_details']['name'],
        'full': reuse_entry['full'],
        # Check for a short override, if not present, fall back to the top-level fieldset's short
        'short': reuse_entry['short_override'] if 'short_override' in reuse_entry else reused_schema['field_details']['short']
    }
    # If it exists, bring through the normalization
    if 'normalize' in reuse_entry:
        reused_here_entry['normalize'] = reuse_entry['normalize']
    # Check for beta attribute
    if 'beta' in reuse_entry:
        reused_here_entry['beta'] = reuse_entry['beta']
    destination_schema['schema_details']['reused_here'].extend([reused_here_entry])


def set_original_fieldset(fields, original_fieldset):
    """Recursively stamp all fields with original_fieldset (uses setdefault, preserves nested values)."""
    def func(details):
        # Don't override if already set (e.g. 'group' for user.group.* fields)
        details['field_details'].setdefault('original_fieldset', original_fieldset)
    visitor.visit_fields(fields, field_func=func)


def field_group_at_path(dotted_path, fields):
    """Return the 'fields' dict at the given dotted path. Creates it for object/group/nested types.

    Raises ValueError if path is missing or passes through a non-nestable field type.
    """
    path = dotted_path.split('.')
    nesting = fields
    for next_field in path:
        field = nesting.get(next_field, None)
        if not field:
            raise ValueError("Field {} not found, failed to find {}".format(dotted_path, next_field))
        nesting = field.get('fields', None)
        if not nesting:
            field_type = field['field_details']['type']
            if field_type in ['object', 'group', 'nested']:
                nesting = field['fields'] = {}
            else:
                raise ValueError("Field {} (type {}) already exists and cannot have nested fields".format(
                    dotted_path, field_type))
    return nesting


def calculate_final_values(fields):
    """Calculate flat_name, dashed_name, multi-field names, and OTel mappings for all fields."""
    visitor.visit_fields_with_path(fields, field_finalizer)


def field_finalizer(details, path):
    """Visitor callback: compute flat_name, dashed_name, multi-field flat_names, and resolve otel_reuse."""
    name_array = path + [details['field_details']['node_name']]
    flat_name = '.'.join(name_array)

    if 'original_fieldset' in details['field_details']:
        if 'otel' in details['field_details']:
            details['field_details'].pop('otel')

        if 'otel_reuse' in details['field_details']:
            otel_reuse = details['field_details']['otel_reuse']
            for r_mapping in otel_reuse:
                if 'ecs' in r_mapping and 'mapping' in r_mapping and r_mapping['ecs'] == flat_name:
                    details['field_details']['otel'] = [r_mapping['mapping']]

    if 'otel_reuse' in details['field_details']:
        details['field_details'].pop('otel_reuse')

    details['field_details']['flat_name'] = flat_name
    details['field_details']['dashed_name'] = re.sub('[_\.]', '-', flat_name).replace('@', '')
    if 'multi_fields' in details['field_details']:
        for mf in details['field_details']['multi_fields']:
            mf['flat_name'] = flat_name + '.' + mf['name']
