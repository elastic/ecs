import os
import yaml
import copy
from generators import ecs_helpers

# This script has a few entrypoints. The code related to each entrypoint is grouped
# together between comments.
#
# merge_schema_fields()
#   Merge ECS field sets with custom field sets
# assemble_reusables()
#   Puts in place all of the reusable fields in the structure
# generate_nested_flat()
#   Finalize the intermediate representation of all fields. Fills field defaults,
#   performs field nestings, and precalculates many values used by various generators.

# Merge ECS field sets with custom field sets


def merge_schema_fields(a, b):
    """Merge ECS field sets with custom field sets"""
    for key in b:
        if key not in a:
            a[key] = b[key]
        else:
            a_type = a[key].get('field_details', {}).get('type', 'object')
            b_type = b[key].get('field_details', {}).get('type', 'object')
            if a_type != b_type:
                raise ValueError('Schemas unmergeable: type {} does not match type {}'.format(a_type, b_type))
            elif a_type not in ['object', 'nested']:
                print('Warning: dropping field {}, already defined'.format(key))
                continue
            # reusable should only be found at the top level of a fieldset
            if 'reusable' in b[key]:
                a[key].setdefault('reusable', {})
                a[key]['reusable']['top_level'] = a[key]['reusable'].get(
                    'top_level', False) or b[key]['reusable']['top_level']
                a[key]['reusable'].setdefault('expected', [])
                a[key]['reusable']['expected'].extend(b[key]['reusable']['expected'])
            if 'fields' in b[key]:
                a[key].setdefault('fields', {})
                merge_schema_fields(a[key]['fields'], b[key]['fields'])

# Finalize the intermediate representation of all fields.


def generate_nested_flat(fields_intermediate):
    for field_name, field in fields_intermediate.items():
        nestings = find_nestings(field['fields'], field_name + ".")
        nestings.sort()
        if len(nestings) > 0:
            field['nestings'] = nestings
    fields_nested = generate_partially_flattened_fields(fields_intermediate)
    fields_flat = generate_fully_flattened_fields(fields_intermediate)
    return (fields_nested, fields_flat)


def assemble_reusables(fields_nested):
    # This happens as a second pass, so that all fieldsets have their
    # fields array replaced with a fields dictionary.
    for schema_name in fields_nested:
        schema = fields_nested[schema_name]
        duplicate_reusable_fieldsets(schema, fields_nested)
    cleanup_fields_recursive(fields_nested, "")
    resolve_self_nestings(fields_nested)


def duplicate_reusable_fieldsets(schema, fields_nested):
    """Copies reusable field definitions to their expected places"""
    # Note: across this schema reader, functions are modifying dictionaries passed
    # as arguments, which is usually a risk of unintended side effects.
    # Here it simplifies the nesting of 'group' under 'user',
    # which is in turn reusable in a few places.
    if 'reusable' in schema:
        resolve_reusable_shorthands(schema)
        for new_nesting in schema['reusable']['expected']:
            nest_at = new_nesting['at']
            nest_as = new_nesting['as']
            split_flat_name = nest_at.split('.')
            top_level = split_flat_name[0]
            if nest_at == schema['name']:
                schema.setdefault('self_nestings', [])
                schema['self_nestings'].append(nest_as)
            else:
                # List field set names expected under another field set.
                # E.g. host.nestings = [ 'geo', 'os', 'user' ]
                nesting_destination = fields_nested[top_level]['fields']
                for level in split_flat_name[1:]:
                    nesting_destination = nesting_destination.get(level, None)
                    if not nesting_destination:
                        raise ValueError('Field {} in path {} not found in schema'.format(level, nest_at))
                    if nesting_destination.get('reusable', None):
                        raise ValueError(
                            'Reusable fields cannot be put inside other reusable fields except when the destination reusable is at the top level')
                    nesting_destination = nesting_destination.setdefault('fields', {})
                nesting_destination[nest_as] = schema


def resolve_reusable_shorthands(schema):
    """
    Replace single word reuse shorthands from the schema YAMLs with the explicit {at: , as:} notation.

    When marking "user" as reusable under "destination" with the shorthand entry
    `- destination`, this is expanded to the complete entry
    `- { "at": "destination", "as": "user" }`.
    The field set is thus nested at `destination.user.*`, with fields such as `destination.user.name`.

    The dictionary notation enables nesting a field set as a different name.
    An example is nesting "process" fields to capture parent process details
    at `process.parent.*`.
    The dictionary notation `- { "at": "process", "as": "parent" }` will yield
    fields such as `process.parent.pid`.
    """
    if 'reusable' in schema:
        reuse_entries = []
        for reuse_entry in schema['reusable']['expected']:
            if type(reuse_entry) is dict:
                if 'at' in reuse_entry and 'as' in reuse_entry:
                    explicit_entry = reuse_entry
                else:
                    raise ValueError("When specifying reusable expected locations " +
                                     "with the dictionary notation, keys 'as' and 'at' are required. " +
                                     "Got {}.".format(reuse_entry))
            else:
                explicit_entry = {'at': reuse_entry, 'as': schema['name']}
            explicit_entry['full'] = explicit_entry['at'] + '.' + explicit_entry['as']
            reuse_entries.append(explicit_entry)
        schema['reusable']['expected'] = reuse_entries


def resolve_self_nestings(fields):
    '''Replace self-nestings with independent copies of the field definitions in the intermediate structure.'''
    for (name, fieldset) in fields.items():
        if 'self_nestings' not in fieldset:
            continue
        fieldset_copy = copy.deepcopy(fieldset)
        fieldset_copy.pop('self_nestings')

        def func(nesting, field_details):
            field_details['original_fieldset'] = nesting[0]
        recurse_fields(func, fieldset_copy, [name])

        for nest_as in fieldset['self_nestings']:
            fieldset['fields'][nest_as] = {'fields': fieldset_copy['fields']}
        fieldset.pop('self_nestings')
    cleanup_fields_recursive(fields, '')


# def recurse_fields(field_func, fields, field_nesting=[]):
#     # fieldset attributes at same level, not nested under 'field_details'
#     is_fieldset = (fields.get('type', None) == 'group' and
#                   type(fields.get('fields', None)) == dict and
#                   [] == field_nesting)
#     if is_fieldset:
#         if 'root' in fields:
#             current_nesting = []
#         else:
#             current_nesting = [fields['name']]
#         fields = fields['fields']
#     else:
#         current_nesting = [fields['name']]

#     for (name, nested) in fields.items():
#         # if 'root' in nested: # should only be "base" fields
#         #     current_nesting = field_nesting
#         # else:
#         #     current_nesting = field_nesting + [name]

#         # Both 'fields' and 'field_details' can be present (e.g. when type=object like dns.answers)
#         if 'field_details' in nested:   # it's a field!
#             field_func(current_nesting, nested['field_details'])
#         if 'fields' in nested:          # it has nested fields!
#             recurse_fields(field_func, nested['fields'], current_nesting)


def find_nestings(fields, prefix):
    """Recursively finds all reusable fields in the fields dictionary."""
    nestings = []
    for field_name, field in fields.items():
        if 'reusable' in field:
            nestings.append(prefix + field_name)
        if 'fields' in field:
            nestings.extend(find_nestings(field['fields'], prefix + field_name + '.'))
    return nestings


def generate_partially_flattened_fields(fields_nested):
    flat_fields = {}
    for (name, field) in fields_nested.items():
        # assigning field.copy() adds all the top level schema fields, has to be a copy since we're about
        # to reassign the 'fields' key and we don't want to modify fields_nested
        flat_fields[name] = field.copy()
        flat_fields[name]['fields'] = flatten_fields(field['fields'], "")
    return flat_fields


def generate_fully_flattened_fields(fields_nested):
    flattened = flatten_fields(remove_non_root_reusables(fields_nested), "")
    return flattened


def remove_non_root_reusables(fields_nested):
    fields = {}
    for (name, field) in fields_nested.items():
        if 'reusable' not in field or ('reusable' in field and field['reusable']['top_level']):
            fields[name] = field
    return fields


def flatten_fields(fields, key_prefix):
    flat_fields = {}
    for (name, field) in fields.items():
        new_key = key_prefix + name
        if 'field_details' in field:
            flat_fields[new_key] = field['field_details'].copy()
        if 'fields' in field:
            new_prefix = new_key + "."
            if 'root' in field and field['root']:
                new_prefix = ""
            flat_fields.update(flatten_fields(field['fields'], new_prefix))
    return flat_fields
