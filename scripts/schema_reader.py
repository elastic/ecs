import glob
import yaml

import pprint

# class SchemaReader:
#     def __init__(self):
#         files = find_files("schemas/*.yml")

## File loading stuff

def schema_files():
    """Return the schema file list to load"""
    return sorted(glob.glob("schemas/*.yml"))

def read_schema_file(file):
    """Read a raw schema yml into a map, removing the wrapping array in each file"""
    with open(file) as f:
        raw = yaml.load(f.read())
    fields = {}
    for field_set in raw:
        fields[field_set['name']] = field_set
    return fields

def load_schema_files(files = schema_files()):
    fields_nested = {}
    for f in files:
        new_fields = read_schema_file(f)
        fields_nested.update(new_fields)
    return fields_nested

## Validation

# TODO Implement validation
def validate_schema(schema):
    """Return schema if valid, aborts with useful message if anything is amiss"""
    return schema

## Generic helpers

def dict_clean_string_values(dict):
    """Remove superfluous spacing in all field values of a dict"""
    for key in dict:
        value = dict[key]
        if isinstance(value, basestring):
            dict[key] = value.strip()
            # TODO: Remove trailing \n?

## Finalize in memory representation of ECS field definitions (e.g. defaults, cleanup)

def schema_cleanup_values(schema):
    dict_clean_string_values(schema)
    schema_set_default_values(schema)
    schema_set_fieldset_prefix(schema)

def schema_set_default_values(schema):
    schema['type'] = 'group'
    if 'group' not in schema:
        schema['group'] = 2

def schema_set_fieldset_prefix(schema):
    if 'root' in schema and schema['root']:
        schema['prefix'] = ''
    else:
        schema['prefix'] = schema['name'] + '.'


def field_cleanup_values(field, prefix):
    dict_clean_string_values(field)
    field_set_defaults(field)
    field_set_flat_name(field, prefix)

def field_set_flat_name(field, prefix):
    field['flat_name'] = prefix + field['name']

def field_set_defaults(field):
    if 'index' in field and field['index'] == False:
        field.delete('type')
    if 'short' not in field:
        field['short'] = field['description']
    if 'multi_fields' in field:
        field_set_multi_field_defaults(field)

def field_set_multi_field_defaults(parent_field):
    """Sets defaults for each nested field in the multi_fields array"""
    for mf in parent_field['multi_fields']:
        if 'name' not in mf:
            mf['name'] = mf['type']
        mf['flat_name'] = parent_field['flat_name'] + '.' + mf['name']

        # Not sure if we'll need:
        # if 'description' not in multi_fields:
        #     multi_fields['description'] = field['description']
        # if 'example' not in multi_fields:
        #     multi_fields['example'] = field['example']

def finalize_schemas(schemas):
    for schema_name in schemas:
        schema = schemas[schema_name]
        schema_set_default_values(schema)

        for field in schema['fields']:
            field_cleanup_values(field, schema['prefix'])

        # interpret_markdown(schema)

if __name__ == '__main__':
    fields_nested = load_schema_files()
    # fields_nested = load_schema_files(['schemas/base.yml'])

    finalize_schemas(fields_nested)
    # print pprint.pprint(fields_nested)
    print pprint.pprint(fields_nested['event'])
