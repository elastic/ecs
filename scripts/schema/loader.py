import copy
import glob
import os
import yaml
from generators import ecs_helpers

# Loads ECS and optional custom schemas. They are deeply nested, then merged.
# This script doesn't fill in defaults other than the bare minimum for a predictable
# deeply nested structure. It doesn't concern itself with what "should be allowed"
# in being a good ECS citizen. It just loads things and merges them together.

# The deeply nested structured returned by this script looks like this.
#
# [schema name]: {
#   'schema_details': {
#       'reusable': ...
#   },
#   'field_details': {
#       'type': ...
#   },
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


def load_schemas(included_files):
    """Loads ECS and custom schemas. They are returned deeply nested and merged."""
    fields = deep_nesting_representation(load_schema_files(ecs_helpers.ecs_files()))
    if included_files and len(included_files) > 0:
        custom_files = ecs_helpers.get_glob_files(included_files, ecs_helpers.YAML_EXT)
        custom_fields = deep_nesting_representation(load_schema_files(custom_files))
        fields = merge_custom_fields(fields, custom_fields)
    return fields


def load_schema_files(files):
    fields_nested = {}
    for f in files:
        new_fields = read_schema_file(f)
        fields_nested = ecs_helpers.safe_merge_dicts(fields_nested, new_fields)
    return fields_nested


def read_schema_file(file):
    """Read a raw schema yml into a dict."""
    with open(file) as f:
        raw = yaml.safe_load(f.read())
    return nest_schema(raw, file)


def nest_schema(raw, file):
    '''
    Raw schema files are an of schema details: [{'name': 'base', ...]

    This function loops over the array (usually 1 schema per file) and turns it into
    a dict with the schema name as the key: { 'base': { 'name': 'base', ...}}
    '''
    fields = {}
    for schema in raw:
        if 'name' not in schema:
            raise ValueError("Schema file {} is missing mandatory attribute 'name'".format(file))
        fields[schema['name']] = schema
    return fields


def deep_nesting_representation(fields):
    deeply_nested = {}
    for (name, flat_schema) in fields.items():
        # We destructively select what goes into schema_details and child fields.
        # The rest is 'field_details'.
        flat_schema = flat_schema.copy()

        # Schema-only details. Not present on other nested field groups.
        schema_details = {}
        for schema_key in ['root', 'group', 'reusable', 'title']:
            if schema_key in flat_schema:
                schema_details[schema_key] = flat_schema.pop(schema_key)


        nested_schema = nest_fields(flat_schema.pop('fields', []))
        # Re-assemble new structure
        deeply_nested[name] = {
            'schema_details': schema_details,
            # What's still in flat_schema is the field_details for the field set itself
            'field_details': flat_schema,
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
            # Where nested fields will live
            nested_schema[level].setdefault('fields', {})
            # Make type:object explicit for intermediary parent fields
            nested_schema[level].setdefault('field_details', {})
            nested_schema[level]['field_details'].setdefault('type', 'object')
            # moving the nested_schema cursor deeper
            nested_schema = nested_schema[level]['fields']
        nested_schema.setdefault(leaf_field, {})
        # Overwrite 'name' with the leaf field's name. The flat_name is already computed.
        nested_schema[leaf_field]['field_details'] = field
    return schema_root

# Merge

def merge_fields(a, b):
    """Merge ECS field sets with custom field sets."""
    a = copy.deepcopy(a)
    b = copy.deepcopy(b)
    for key in b:
        if key not in a:
            a[key] = b[key]
            continue
        # merge field details
        if 'normalize' in b[key]['field_details']:
            a[key].setdefault('field_details', {})
            a[key]['field_details'].setdefault('normalize', [])
            a[key]['field_details']['normalize'].extend(b[key]['field_details'].pop('normalize'))
        a[key]['field_details'].update(b[key]['field_details'])
        # merge schema details
        if 'schema_details' in b[key]:
            asd = a[key]['schema_details']
            bsd = b[key]['schema_details']
            if 'reusable' in b[key]['schema_details']:
                asd.setdefault('reusable', {})
                if 'top_level' in bsd['reusable']:
                    asd['reusable']['top_level'] = bsd['reusable']['top_level']
                else:
                    asd['reusable'].setdefault('top_level', True)
                asd['reusable'].setdefault('expected', [])
                asd['reusable']['expected'].extend(bsd['reusable']['expected'])
                bsd.pop('reusable')
            asd.update(bsd)
        # merge nested fields
        if 'fields' in b[key]:
            a[key].setdefault('fields', {})
            a[key]['fields'] = merge_fields(a[key]['fields'], b[key]['fields'])
    return a
