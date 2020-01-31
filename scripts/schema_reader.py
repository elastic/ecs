import glob
import os
import yaml
import copy

# File loading stuff


def ecs_files():
    """Return the schema file list to load"""
    schema_glob = os.path.join(os.path.dirname(__file__), '../schemas/*.yml')
    return sorted(glob.glob(schema_glob))


def read_schema_file(file):
    """Read a raw schema yml into a map, removing the wrapping array in each file"""
    with open(file) as f:
        raw = yaml.safe_load(f.read())
    fields = {}
    for field_set in raw:
        fields[field_set['name']] = field_set
    return fields


def load_schema_files(files=ecs_files()):
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
        if isinstance(value, str):
            dict[key] = value.strip()


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
    dict_set_default(schema, 'short', schema['description'])
    if "\n" in schema['short']:
        raise ValueError("Short descriptions must be single line.\nFieldset: {}\n{}".format(schema['name'], schema))


def schema_set_fieldset_prefix(schema):
    if 'root' in schema and schema['root']:
        schema['prefix'] = ''
    else:
        schema['prefix'] = schema['name'] + '.'


def schema_fields_as_dictionary(schema):
    """Re-nest the array of field names as a dictionary of 'fieldname' => { field definition }"""
    field_array = schema.pop('fields')
    schema['fields'] = {}
    for order, field in enumerate(field_array):
        field['order'] = order
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


def field_set_defaults(field):
    if field['type'] == 'keyword':
        dict_set_default(field, 'ignore_above', 1024)
    if field['type'] == 'text':
        dict_set_default(field, 'norms', False)
    if field['type'] == 'object':
        dict_set_default(field, 'object_type', 'keyword')

    dict_set_default(field, 'short', field['description'])
    if "\n" in field['short']:
        raise ValueError("Short descriptions must be single line.\nField: {}\n{}".format(field['flat_name'], field))
        # print("  Short descriptions must be single line. Field: {}".format(field['flat_name']))

    if 'index' in field and not field['index']:
        dict_set_default(field, 'doc_values', False)
    if 'multi_fields' in field:
        field_set_multi_field_defaults(field)


def field_set_multi_field_defaults(parent_field):
    """Sets defaults for each nested field in the multi_fields array"""
    for mf in parent_field['multi_fields']:
        dict_set_default(mf, 'name', mf['type'])
        if mf['type'] == 'text':
            dict_set_default(mf, 'norms', False)
        mf['flat_name'] = parent_field['flat_name'] + '.' + mf['name']


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
            nestings = fields_nested[top_level].setdefault('nestings', [])
            if schema['name'] not in nestings:
                nestings.append(schema['name'])
            nestings.sort()
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

# Main


def finalize_schemas(fields_nested):
    for schema_name in fields_nested:
        schema = fields_nested[schema_name]

        schema_cleanup_values(schema)

    # This happens as a second pass, so that all fieldsets have their
    # fields array replaced with a fields dictionary.
    for schema_name in fields_nested:
        schema = fields_nested[schema_name]

        duplicate_reusable_fieldsets(schema, fields_nested)


def flatten_fields(fields, key_prefix, original_fieldset=None):
    flat_fields = {}
    for (name, field) in fields.items():
        new_key = key_prefix + name
        temp_original_fieldset = original_fieldset
        if 'reusable' in field:
            temp_original_fieldset = name
        if 'field_details' in field:
            flat_fields[new_key] = field['field_details'].copy()
            if temp_original_fieldset:
                flat_fields[new_key]['original_fieldset'] = temp_original_fieldset
        if 'fields' in field:
            new_prefix = new_key + "."
            if 'root' in field and field['root']:
                new_prefix = ""
            flat_fields.update(flatten_fields(field['fields'], new_prefix, temp_original_fieldset))
    return flat_fields


def generate_partially_flattened_fields(fields_nested):
    flat_fields = {}
    for (name, field) in fields_nested.items():
        # assigning field.copy() adds all the top level schema fields, has to be a copy since we're about
        # to reassign the 'fields' key and we don't want to modify fields_nested
        flat_fields[name] = field.copy()
        flat_fields[name]['fields'] = flatten_fields(field['fields'], "")
    return flat_fields


def generate_fully_flattened_fields(fields_nested):
    return flatten_fields(fields_nested, "")


def cleanup_fields_recursive(fields, prefix):
    for (name, field) in fields.items():
        # Copy field here so reusable field sets become unique copies instead of references to the original set
        field = field.copy()
        fields[name] = field
        if 'field_details' in field:
            # Deep copy the field details so we can insert different flat names for each reusable fieldset
            field_details = copy.deepcopy(field['field_details'])
            new_flat_name = prefix + name
            field_details['flat_name'] = new_flat_name
            field_details['dashed_name'] = new_flat_name.replace('.', '-').replace('_', '-')
            dict_clean_string_values(field_details)
            field_set_defaults(field_details)
            field['field_details'] = field_details
        if 'fields' in field:
            field['fields'] = field['fields'].copy()
            new_prefix = prefix + name + "."
            if 'root' in field and field['root']:
                new_prefix = ""
            cleanup_fields_recursive(field['fields'], new_prefix)


def load_schemas(files=ecs_files()):
    """Loads the given list of files"""
    fields_intermediate = load_schema_files(files)
    finalize_schemas(fields_intermediate)
    cleanup_fields_recursive(fields_intermediate, "")
    fields_nested = generate_partially_flattened_fields(fields_intermediate)
    fields_flat = generate_fully_flattened_fields(fields_intermediate)
    return (fields_nested, fields_flat)
