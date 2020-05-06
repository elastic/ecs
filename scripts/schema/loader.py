import copy
import glob
import os
import yaml
from generators import ecs_helpers

# Loads ECS and optional custom schemas. They are deeply nested, then merged.

def load_schemas(included_files):
    """Loads ECS and custom schemas. They are returned deeply nested and merged."""
    fields = deep_nesting_representation(load_schema_files(ecs_helpers.ecs_files()))
    ecs_helpers.yaml_dump('_notes/nest-as/loader-ecs.yml', fields)
    if included_files and len(included_files) > 0:
        custom_files = ecs_helpers.get_glob_files(included_files, ecs_helpers.YAML_EXT)
        custom_fields = deep_nesting_representation(load_schema_files(custom_files))
        ecs_helpers.yaml_dump('_notes/nest-as/loader-custom.yml', custom_fields)
        fields = merge_custom_fields(fields, custom_fields)
        ecs_helpers.yaml_dump('_notes/nest-as/loader-merged.yml', fields)
    # TODO mandatory_attributes(fields)

    return fields


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


def deep_nesting_representation(fields):
    deeply_nested = {}
    for (name, flat_schema) in fields.items():
        # We destructively select what goes into schema_details and child fields.
        # The rest is 'field_details'.
        flat_schema = flat_schema.copy()

        # Schema-only details. Not present on other nested field groups.
        schema_details = {}
        for schema_key in ['root', 'group', 'reusable']:
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
            nested_schema[level].setdefault('fields', {})
            # moving the nested_schema cursor deeper
            nested_schema = nested_schema[level]['fields']
        nested_schema.setdefault(leaf_field, {})
        # Overwrite 'name' with the leaf field's name. The flat_name is already computed.
        nested_schema[leaf_field]['field_details'] = field
    return schema_root

# Merge

def merge_custom_fields(a, b):
    """Merge ECS field sets with custom field sets"""
    object_like_types = ['group', 'object', 'nested']
    a = copy.deepcopy(a)
    for key in b:
        if key not in a:
            a[key] = b[key]
            continue
        a_object_like = ('fields' in a[key] or
                a[key]['field_details']['type'] in object_like_types)
        b_object_like = ('fields' in b[key] or
                'schema_details' in b[key] or
                b[key]['field_details']['type'] in object_like_types)
        if a_object_like != b_object_like:
            raise ValueError('Field {} unmergeable: one side is a leaf field and not the other'.format(key))
        if not a_object_like:
            raise ValueError('ECS field details cannot be overridden fow now. Field: {}'.format(key))
        # TODO merge field details?
        if 'schema_details' in a[key] and 'schema_details' in b[key]:
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
                asd['reusable']['expected'] = sorted(asd['reusable']['expected'])
        if 'fields' in b[key]:
            a[key].setdefault('fields', {})
            a[key]['fields'] = merge_custom_fields(a[key]['fields'], b[key]['fields'])
    return a


def old_merge(a, b):
    """Merge ECS field sets with custom field sets"""
    for key in b:
        if key not in a:
            a[key] = b[key]
        else:
            a_type = a[key].get('field_details', {}).get('type', 'object')
            b_type = b[key].get('field_details', {}).get('type', 'object')
            if a_type != b_type:
                raise ValueError('Schemas unmergeable for {}: type {} does not match type {}'.format(key, a_type, b_type))
            elif a_type not in ['object', 'nested']:
                print('Warning: dropping field {}, already defined'.format(key))
                continue
            if b[key]['schema_details'] and 'reusable' in b[key]:
                a[key].setdefault('reusable', {})
                a[key]['reusable']['top_level'] = a[key]['reusable'].get(
                    'top_level', False) or b[key]['reusable']['top_level']
                a[key]['reusable'].setdefault('expected', [])
                a[key]['reusable']['expected'].extend(b[key]['reusable']['expected'])
                a[key]['reusable']['expected'] = sorted(a[key]['reusable']['expected'])
            if 'fields' in b[key]:
                a[key].setdefault('fields', {})
                merge_schema_fields(a[key]['fields'], b[key]['fields'])



