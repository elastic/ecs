import glob
import yaml

# File loading stuff


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


def load_schema_files(files=schema_files()):
    fields_nested = {}
    for f in files:
        new_fields = read_schema_file(f)
        fields_nested.update(new_fields)
    return fields_nested

# Generic helpers


def dict_clean_string_values(dict):
    """Remove superfluous spacing in all field values of a dict"""
    for key in dict:
        value = dict[key]
        if isinstance(value, basestring):
            dict[key] = value.strip()
            # TODO: Remove trailing \n?


def dict_set_default(dict, key, default):
    if key not in dict:
        dict[key] = default


# Finalize in memory representation of ECS field definitions (e.g. defaults, cleanup)

# Schema level (data about the field sets)


def schema_cleanup_values(schema):
    dict_clean_string_values(schema)
    schema_set_default_values(schema)
    schema_set_fieldset_prefix(schema)
    schema_fields_as_dictionary(schema)


def schema_set_default_values(schema):
    schema['type'] = 'group'
    dict_set_default(schema, 'group', 2)


def schema_set_fieldset_prefix(schema):
    if 'root' in schema and schema['root']:
        schema['prefix'] = ''
    else:
        schema['prefix'] = schema['name'] + '.'


def schema_fields_as_dictionary(schema):
    """Re-nest the array of field names as a dictionary of 'fieldname' => { field definition }"""
    field_array = schema.pop('fields')
    schema['fields'] = {}
    for field in field_array:
        schema['fields'][field['name']] = field

# Field definitions


def field_cleanup_values(field, prefix):
    dict_clean_string_values(field)
    field_set_defaults(field)
    field_set_flat_name(field, prefix)


def field_set_flat_name(field, prefix):
    field['flat_name'] = prefix + field['name']


def field_set_defaults(field):
    dict_set_default(field, 'short', field['description'])
    if field['type'] == 'keyword':
        dict_set_default(field, 'ignore_above', 1024)
    if field['type'] == 'text':
        dict_set_default(field, 'norms', False)
    if field['type'] == 'object':
        dict_set_default(field, 'object_type', 'keyword')

    if 'index' in field and not field['index']:
        dict_set_default(field, 'doc_values', False)
    if 'multi_fields' in field:
        field_set_multi_field_defaults(field)


def field_set_multi_field_defaults(parent_field):
    """Sets defaults for each nested field in the multi_fields array"""
    for mf in parent_field['multi_fields']:
        dict_set_default(mf, 'name', mf['type'])
        mf['flat_name'] = parent_field['flat_name'] + '.' + mf['name']


def duplicate_reusable_fieldsets(schema, fields_flat):
    """Copies reusable field definitions to their expected places in the flattened schema only"""
    if 'reusable' in schema:
        for new_nesting in schema['reusable']['expected']:

            for (name, field) in schema['fields'].items():
                # Poor folks deepcopy, sorry -- A Rubyist
                copied_field = field.copy()
                if 'multi_fields' in copied_field:
                    copied_field['multi_fields'] = copied_field['multi_fields'].copy()

                destination_name = new_nesting + '.' + field['flat_name']
                copied_field['flat_name'] = destination_name
                copied_field['original_fieldset'] = schema['name']
                fields_flat[destination_name] = copied_field

# Main


def finalize_schemas(fields_nested, fields_flat):
    for schema_name in fields_nested:
        schema = fields_nested[schema_name]
        schema_cleanup_values(schema)

        for (name, field) in schema['fields'].items():
            field_cleanup_values(field, schema['prefix'])

            fields_flat[field['flat_name']] = field

        # TODO duplicate in nested too?
        duplicate_reusable_fieldsets(schema, fields_flat)


def load_ecs():
    fields_nested = load_schema_files()
    fields_flat = {}
    finalize_schemas(fields_nested, fields_flat)
    return (fields_nested, fields_flat)
