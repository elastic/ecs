import os
import yaml
import copy
from generators import ecs_helpers

# Loads schemas and perform cleanup of schema attributes


def load_schemas(files=ecs_helpers.ecs_files()):
    """Loads the list of files and performs schema level cleanup"""
    fields_nested = load_schema_files(files)
    make_defaults_explicit(fields_nested)
    return deep_nesting_representation(fields_nested)


def load_schema_files(files):
    fields_nested = {}
    for f in files:
        new_fields = read_schema_file(f)
        fields_nested.update(new_fields)
    return fields_nested


def read_schema_file(file):
    """Read a raw schema yml into a map, removing the wrapping array in each file"""
    with open(file) as f:
        raw = yaml.safe_load(f.read())
    fields = {}
    for field_set in raw:
        fields[field_set['name']] = field_set
    return fields


def make_defaults_explicit(fields_nested):
    """Makes all defaults explicit at the schema and fields level"""
    for schema_name in fields_nested:
        schema = fields_nested[schema_name]
        schema_explicit_defaults(schema)
        field_list_explicit_defaults(schema)


def schema_explicit_defaults(schema):
    ecs_helpers.dict_clean_string_values(schema)
    schema['type'] = 'group'
    schema.setdefault('group', 2)
    schema.setdefault('root', False)
    schema.setdefault('short', schema['description'])
    if "\n" in schema['short']:
        raise ValueError("Short descriptions must be single line.\nFieldset: {}\n{}".format(schema['name'], schema))
    if schema['root']:
        schema['prefix'] = ''
    else:
        schema['prefix'] = schema['name'] + '.'
    schema.setdefault('reusable', {})
    schema['reusable'].setdefault('top_level', True)
    schema['reusable'].setdefault('expected', [])


def field_list_explicit_defaults(schema):
    for field in schema['fields']:
        field_explicit_defaults(field, schema['prefix'])


def field_explicit_defaults(field, prefix):
    ecs_helpers.dict_clean_string_values(field)
    field.setdefault('normalize', [])
    if field['type'] == 'keyword':
        field.setdefault('ignore_above', 1024)
    if field['type'] == 'text':
        field.setdefault('norms', False)
    if field['type'] == 'object':
        field.setdefault('object_type', 'keyword')

    field['flat_name'] = prefix + field['name']
    field['dashed_name'] = field['flat_name'].replace('.', '-').replace('_', '-')

    field.setdefault('short', field['description'])
    if "\n" in field['short']:
        raise ValueError("Short descriptions must be single line.\nField: {}\n{}".format(field['flat_name'], field))
    if 'index' in field and not field['index']:
        field.setdefault('doc_values', False)
    if 'multi_fields' in field:
        multi_field_explicit_defaults(field)


def multi_field_explicit_defaults(parent_field):
    """Sets defaults for each nested field in the multi_fields array"""
    for mf in parent_field['multi_fields']:
        mf.setdefault('name', mf['type'])
        if mf['type'] == 'text':
            mf.setdefault('norms', False)
        mf['flat_name'] = parent_field['flat_name'] + '.' + mf['name']

# This script mostly deals with the nesting structure as it appears in schemas/*.yml.
# Below here we transform this into a deeply nested structure that enables
# schema merging (for --include) and simplifies field reuse.
# From a the original flat structure, we end up with the following structure per schema:

# [schema name]: {
#   'schema_details': { ... }   # details specific only to schemas themselves
#
#   'field_details': { ... }
#   'fields': {

#       [field name]: {
#           'field_details': { ... }
#           'fields': {
#
#               (dotted key names replaced by deep nesting)
#               [field name]: {
#                   'field_details': { ... }
#                   'fields': {
#                   }
#               }
#           }
#       }
#   }

# Schemas at the top level always have all 3 keys populated.
# Leaf fields only have 'field_details' populated.
# Any intermediary field with other fields nested within them have 'fields' populated.
# Note that intermediary fields rarely have 'field_details' populated, but it's supported.
#   Examples of this are 'dns.answers', 'observer.egress' or others.


def deep_nesting_representation(fields):
    deeply_nested = {}
    for (name, flat_schema) in fields.items():
        # We destructively select what goes into schema_details and child fields.
        # The rest is 'field_details'.
        flat_schema = flat_schema.copy()

        # Schema-only details. Not present on field groups.
        schema_details = {
            'root': flat_schema.pop('root'),
            'group': flat_schema.pop('group'),
            'prefix': flat_schema.pop('prefix'),
        }
        if 'reusable' in flat_schema:
            schema_details['reusable'] = flat_schema.pop('reusable')

        nested_schema = nest_fields(flat_schema.pop('fields', []))
        # Re-assemble new structure
        deeply_nested[name] = {
            'schema_details': schema_details,
            'field_details': flat_schema, # What's still in flat_schema is the field_details
            'fields': nested_schema['fields']
        }
    return deeply_nested


def nest_fields(field_array):
    schema_root = { 'fields': {} }
    for field in field_array:
        nested_levels = field['name'].split('.')
        parent_fields = nested_levels[:-1]
        leaf_field = nested_levels[-1]
        # "nested_schema" is a cursor we move within the schema_root structure we're building.
        # Here we reset the cursor for this new field.
        nested_schema = schema_root['fields']

        for level in parent_fields:
            nested_schema.setdefault(level, {})
            nested_schema[level].setdefault('fields', {})
            # moving the nested_schema cursor deeper
            nested_schema = nested_schema[level]['fields']
        nested_schema.setdefault(leaf_field, {})
        # Overwrite 'name' with the leaf field's name. The flat_name is already computed.
        nested_schema[leaf_field]['field_details'] = field
    return schema_root
