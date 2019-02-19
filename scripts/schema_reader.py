import glob
import yaml

import pprint

# class SchemaReader:
#     def __init__(self):
#         files = find_files("schemas/*.yml")

def schema_files():
    """Return the schema file list to load"""
    return sorted(glob.glob("schemas/*.yml"))

# TODO Implement validation
def validate_schema(schema):
    """Returns schema if valid, aborts with useful message if anything is amiss"""
    return schema

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

def finalize_schemas(schemas):
    for key in schemas.keys:
        schema = schemas[key]
        set_fieldset_nesting(schema)
        # set_default_values(schema)
        # interpret_markdown(schema)

def set_fieldset_nesting(schema):
    if 'prefix' not in schema:
        schema['prefix'] = schema['name']

# def set_default_values(schema):

if __name__ == '__main__':
    # for file in schema_files():
    #     print file
    # print read_schema_file('schemas/ecs.yml')
    # print load_all_schema_files()

    # fields_nested = load_schema_files()
    # print pprint.pprint(fields_nested)
    fields_nested = load_schema_files(['schemas/base.yml'])
    print pprint.pprint(fields_nested)
