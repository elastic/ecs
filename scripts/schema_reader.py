import os
import yaml
import copy
from generators import ecs_helpers

# This script has a few entrypoints. The code related to each entrypoint is grouped
# together between comments.
#
# load_schemas()
#   yml file load (ECS or custom) + cleanup of field set attributes.
# merge_schema_fields()
#   Merge ECS field sets with custom field sets
# generate_nested_flat()
#   Finalize the intermediate representation of all fields. Fills field defaults,
#   performs field nestings, and precalculates many values used by various generators.

# Loads schemas and perform cleanup of schema attributes


def load_schemas(files=ecs_helpers.ecs_files()):
    """Loads the list of files and performs schema level cleanup"""
    fields_intermediate = load_schema_files(files)
    finalize_schemas(fields_intermediate)
    return fields_intermediate


def load_schema_files(files):
    fields_nested = {}
    for f in files:
        new_fields = read_schema_file(f)
        fields_nested = ecs_helpers.safe_merge_dicts(fields_nested, new_fields)
    return fields_nested


def read_schema_file(file):
    """Read a raw schema yml into a map, removing the wrapping array in each file"""
    with open(file) as f:
        raw = yaml.safe_load(f.read())
    fields = {}
    for field_set in raw:
        fields[field_set['name']] = field_set
    return fields


def finalize_schemas(fields_nested):
    """Clean up all schema level attributes"""
    for schema_name in fields_nested:
        schema = fields_nested[schema_name]
        schema_cleanup_values(schema)


def schema_cleanup_values(schema):
    """Clean up one schema"""
    ecs_helpers.dict_clean_string_values(schema)
    schema_set_default_values(schema)
    schema_set_fieldset_prefix(schema)
    schema_fields_as_dictionary(schema)


def schema_set_default_values(schema):
    schema['type'] = 'group'
    schema.setdefault('group', 2)
    schema.setdefault('short', schema['description'])
    if "\n" in schema['short']:
        raise ValueError("Short descriptions must be single line.\nFieldset: {}\n{}".format(schema['name'], schema))


def schema_set_fieldset_prefix(schema):
    if 'root' in schema and schema['root']:
        schema['prefix'] = ''
    else:
        schema['prefix'] = schema['name'] + '.'


def schema_fields_as_dictionary(schema):
    """Re-nest the array of field names as a dictionary of 'fieldname' => { field definition }"""
    field_array = schema.pop('fields', [])
    schema['fields'] = {}
    for field in field_array:
        nested_levels = field['name'].split('.')
        nested_schema = schema['fields']
        for level in nested_levels[:-1]:
            if level not in nested_schema:
                nested_schema[level] = {}
            if 'fields' not in nested_schema[level]:
                nested_schema[level]['fields'] = {}
            nested_schema = nested_schema[level]['fields']
        if nested_levels[-1] not in nested_schema:
            nested_schema[nested_levels[-1]] = {}
        # Only leaf fields will have field details so we can identify them later
        nested_schema[nested_levels[-1]]['field_details'] = field

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


def duplicate_reusable_fieldsets(schema, fields_nested):
    """Copies reusable field definitions to their expected places"""
    # Note: across this schema reader, functions are modifying dictionaries passed
    # as arguments, which is usually a risk of unintended side effects.
    # Here it simplifies the nesting of 'group' under 'user',
    # which is in turn reusable in a few places.
    if 'reusable' in schema:
        for new_nesting in schema['reusable']['expected']:
            split_flat_name = new_nesting.split('.')
            top_level = split_flat_name[0]
            # List field set names expected under another field set.
            # E.g. host.nestings = [ 'geo', 'os', 'user' ]
            nested_schema = fields_nested[top_level]['fields']
            for level in split_flat_name[1:]:
                nested_schema = nested_schema.get(level, None)
                if not nested_schema:
                    raise ValueError('Field {} in path {} not found in schema'.format(level, new_nesting))
                if nested_schema.get('reusable', None):
                    raise ValueError(
                        'Reusable fields cannot be put inside other reusable fields except when the destination reusable is at the top level')
                nested_schema = nested_schema.setdefault('fields', {})
            nested_schema[schema['name']] = schema


def cleanup_fields_recursive(fields, prefix, original_fieldset=None):
    for (name, field) in fields.items():
        # Copy field here so reusable field sets become unique copies instead of references to the original set
        field = field.copy()
        fields[name] = field
        temp_original_fieldset = name if ('reusable' in field and prefix != "") else original_fieldset
        if 'field_details' in field:
            # Deep copy the field details so we can insert different flat names for each reusable fieldset
            field_details = copy.deepcopy(field['field_details'])
            new_flat_name = prefix + name
            field_details['flat_name'] = new_flat_name
            field_details['dashed_name'] = new_flat_name.replace('.', '-').replace('_', '-')
            if temp_original_fieldset:
                field_details['original_fieldset'] = temp_original_fieldset
            ecs_helpers.dict_clean_string_values(field_details)
            field_set_defaults(field_details)
            field['field_details'] = field_details
        if 'fields' in field:
            field['fields'] = field['fields'].copy()
            new_prefix = prefix + name + "."
            if 'root' in field and field['root']:
                new_prefix = ""
            cleanup_fields_recursive(field['fields'], new_prefix, temp_original_fieldset)


def field_set_defaults(field):
    field.setdefault('normalize', [])
    if field['type'] == 'keyword':
        field.setdefault('ignore_above', 1024)
    if field['type'] == 'text':
        field.setdefault('norms', False)
    if field['type'] == 'object':
        field.setdefault('object_type', 'keyword')

    field.setdefault('short', field['description'])
    if "\n" in field['short']:
        raise ValueError("Short descriptions must be single line.\nField: {}\n{}".format(field['flat_name'], field))
        # print("  Short descriptions must be single line. Field: {}".format(field['flat_name']))

    if 'index' in field and not field['index']:
        field.setdefault('doc_values', False)
    if 'multi_fields' in field:
        field_set_multi_field_defaults(field)


def field_set_multi_field_defaults(parent_field):
    """Sets defaults for each nested field in the multi_fields array"""
    for mf in parent_field['multi_fields']:
        mf.setdefault('name', mf['type'])
        if mf['type'] == 'text':
            mf.setdefault('norms', False)
        mf['flat_name'] = parent_field['flat_name'] + '.' + mf['name']


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
