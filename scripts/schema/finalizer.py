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
import re

from schema import visitor

# This script takes the fleshed out deeply nested fields dictionary as emitted by
# cleaner.py, and performs field reuse in two phases.
#
# Phase 1 performs field reuse across field sets. E.g. `group` fields should also be under `user`.
# This type of reuse is then carried around if the receiving field set is also reused.
# In other words, user.group.* will be in other places where user is nested:
# source.user.* will contain source.user.group.*

# Phase 2 performs field reuse where field sets are reused within themselves, with a different name.
# Examples are nesting `process` within itself, as `process.parent.*`,
# or nesting `user` within itself at `user.target.*`.
# This second kind of nesting is not carried around everywhere else the receiving field set is reused.
# So `user.target.*` is *not* carried over to `source.user.target*` when we reuse `user` under `source`.


def finalize(fields):
    """Intended entrypoint of the finalizer."""
    perform_reuse(fields)
    calculate_final_values(fields)


def order_reuses(fields):
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
                self_nestings.setdefault(destination_schema_name, [])
                self_nestings[destination_schema_name].extend([reuse_entry])
            else:
                # Group foreign reuses by 'order' attribute.
                foreign_reuses.setdefault(reuse_order, {})
                foreign_reuses[reuse_order].setdefault(schema_name, [])
                foreign_reuses[reuse_order][schema_name].extend([reuse_entry])
    return foreign_reuses, self_nestings


def perform_reuse(fields):
    """Performs field reuse in two phases"""
    foreign_reuses, self_nestings = order_reuses(fields)

    # Phase 1: foreign reuse
    # These are done respecting the reusable.order attribute.
    # This lets us force the order for chained reuses (e.g. group => user, then user => many places)
    for order in sorted(foreign_reuses.keys()):
        for schema_name, reuse_entries in foreign_reuses[order].items():
            schema = fields[schema_name]
            for reuse_entry in reuse_entries:
                # print(order, "{} => {}".format(schema_name, reuse_entry['full']))
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

    # Phase 2: self-nesting
    for schema_name, reuse_entries in self_nestings.items():
        schema = fields[schema_name]
        ensure_valid_reuse(schema)
        # Since we're about self-nest more fields within these, make a pristine copy first
        reused_fields = copy.deepcopy(schema['fields'])
        set_original_fieldset(reused_fields, schema_name)
        for reuse_entry in reuse_entries:
            # print("x {} => {}".format(schema_name, reuse_entry['full']))
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
    """
    Raise if either the reused schema or destination schema have root=true.

    Second param is optional, if testing for a self-nesting (where source=destination).
    """
    if reused_schema['schema_details']['root']:
        msg = "Schema {} has attribute root=true and therefore cannot be reused.".format(
            reused_schema['field_details']['name'])
        raise ValueError(msg)
    elif destination_schema and destination_schema['schema_details']['root']:
        msg = "Schema {} has attribute root=true and therefore cannot have other field sets reused inside it.".format(
            destination_schema['field_details']['name'])
        raise ValueError(msg)


def append_reused_here(reused_schema, reuse_entry, destination_schema):
    """Captures two ways of denoting what field sets are reused under a given field set"""
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
    """Recursively set the 'original_fieldset' attribute for all fields in a group of fields"""
    def func(details):
        # Don't override if already set (e.g. 'group' for user.group.* fields)
        details['field_details'].setdefault('original_fieldset', original_fieldset)
    visitor.visit_fields(fields, field_func=func)


def field_group_at_path(dotted_path, fields):
    """Returns the ['fields'] hash at the dotted_path."""
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
    """
    This function navigates all fields recursively.

    It populates a few more values for the fields, especially path-based values
    like flat_name.
    """
    visitor.visit_fields_with_path(fields, field_finalizer)


def field_finalizer(details, path):
    """This is the function called by the visitor to perform the work of calculate_final_values"""
    name_array = path + [details['field_details']['node_name']]
    flat_name = '.'.join(name_array)
    details['field_details']['flat_name'] = flat_name
    details['field_details']['dashed_name'] = re.sub('[_\.]', '-', flat_name).replace('@', '')
    if 'multi_fields' in details['field_details']:
        for mf in details['field_details']['multi_fields']:
            mf['flat_name'] = flat_name + '.' + mf['name']
