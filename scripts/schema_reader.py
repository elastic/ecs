import yaml
import copy
import pprint
import os
import glob
from enum import Enum

# File loading stuff

ECS_CORE_DIR = os.path.join(os.path.dirname(__file__), '../schemas')
BASE_FILE = os.path.join(ECS_CORE_DIR, 'base.yml')
YAML_EXT = ('*.yml', '*.yaml')


class SchemaFileType(Enum):
    CUSTOM = 1
    FLAT = 2
    NORMAL = 3


class SchemaFileTypeException(Exception):
    pass


class SchemaValidationException(Exception):
    pass


class BaseSchemaException(Exception):
    pass


def get_glob_files(paths, file_types):
    all_files = []
    for path in paths:
        schema_files_with_glob = []
        for t in file_types:
            schema_files_with_glob.extend(glob.glob(os.path.join(path, t)))
        # this preserves the ordering of how the schema flags are included, the last schema directory on the commandline
        # will have the ability to override the previous schema definitions
        all_files.extend(sorted(schema_files_with_glob))

    return all_files


def get_core_files():
    return get_glob_files([ECS_CORE_DIR], YAML_EXT)


def get_file_type(schema):
    """Return an enum representing the type of file being read."""
    if '@timestamp' in schema:
        # If @timestamp is in the global scope it's probably a flattened intermediate file
        return SchemaFileType.FLAT
    elif 'title' in schema:
        # if title is in the global scope then it's probably a custom use-case style schema file
        return SchemaFileType.CUSTOM
    else:
        return SchemaFileType.NORMAL


def read_schema_file(raw):
    """Read a raw schema yml into a map, removing the wrapping array in each file"""
    fields = {}
    for field_set in raw:
        fields[field_set['name']] = field_set
    return fields


def load_base_file():
    with open(BASE_FILE) as schema_file:
        raw = yaml.safe_load(schema_file.read())
    base_fields = read_schema_file(raw)
    return create_nested_and_flat(base_fields)[0]['base']


def load_schema_files(files, validate):
    fields_nested = {}
    flattened_schema = []

    custom_nested = {}
    custom_flattened = {}
    base_fields = load_base_file()

    for f in files:
        with open(f) as schema_file:
            raw = yaml.safe_load(schema_file.read())

        file_type = get_file_type(raw)
        if file_type is SchemaFileType.NORMAL:
            new_fields = read_schema_file(raw)
            fields_nested = merge_dict_overwrite(fields_nested, new_fields, validate)
        elif file_type is SchemaFileType.FLAT:
            flattened_schema.append(raw)
        elif file_type is SchemaFileType.CUSTOM:
            single_file_nested, single_file_flat = create_nested_and_flat(fixup_custom(raw, base_fields))
            custom_nested = merge_dict_overwrite(custom_nested, single_file_nested, validate)
            custom_flattened = merge_dict_overwrite(custom_flattened, single_file_flat, validate)
        else:
            raise SchemaFileTypeException('Unknown file type: {}'.format(file_type))

    final_nested, flattened = create_nested_and_flat(fields_nested)
    final_nested = merge_dict_overwrite(final_nested, custom_nested, validate)

    flattened_schema.extend([flattened, custom_flattened])

    final_flattened = {}
    for flat_item in flattened_schema:
        final_flattened = merge_dict_overwrite(final_flattened, flat_item, validate)

    return final_nested, final_flattened


# Use case helpers


def create_nested_and_flat(fields_intermediate):
    finalize_schemas(fields_intermediate)
    cleanup_fields_recursive(fields_intermediate, "")
    fields_nested = generate_partially_flattened_fields(fields_intermediate)
    fields_flat = generate_fully_flattened_fields(fields_intermediate)
    return fields_nested, fields_flat


def add_needed_fields(fields):
    for field in fields:
        if 'fields' in field:
            add_needed_fields(field['fields'])

        if 'type' not in field:
            field['type'] = 'group'
        if 'level' not in field:
            field['level'] = '(custom)'


def fixup_custom(raw, base_fields):
    """
    Converts a custom nested style yaml file into the appropriate format for so it can be used to override ecs schema.
    The base.yml file should be parsed and passed into this function so fields like @timestamp and message can be
    moved to within the base schema correctly.
    :param raw: the fields read from the yaml file
    :param base_fields: the base.yml file's schema
    :return: the fixed up schema so it's ready to be parsed
    """
    if not base_fields:
        raise Exception('The base fields must be supplied to parse use-case style schema')
    ret_fields = {}
    top_fields = raw['fields']
    collected_base_fields = {
        'name': 'base',
        'title': base_fields['title'],
        'root': base_fields['root'],
        'short': base_fields['short'],
        'description': base_fields['description'],
        'type': base_fields['type'],
        'group': base_fields['group'],
        'fields': []
    }
    ret_fields['base'] = collected_base_fields

    for field in top_fields:
        name = field['name']
        if name in base_fields['fields']:
            if base_fields['fields'][name]['type'] != field['type']:
                raise BaseSchemaException('Found a base field with differing types custom name: {} '
                                          'type: {} base type: {}'.format(name, field['type'],
                                                                          base_fields['fields'][name]['type']))
            ret_fields['base']['fields'].append(base_fields['fields'][name])
        else:
            # title should only be on the top level field
            if 'title' not in field:
                field['title'] = name
            add_needed_fields([field])
            ret_fields[name] = field

    return ret_fields


# Generic helpers


def merge_dict_overwrite(a, b, validate, path=None):
    """
    Merge dictionary b into a. This will overwrite fields in a. Dictionary b takes precedence over a, if there is
    a conflict in values, this will use b's over a's.
    """
    # These keys will not be merged if they exist in both dictionaries, we'll just use dictionary a's value
    ignore_keys = ['description', 'order', 'short', 'example', 'level', 'title']
    # These keys will be ignored for validation errors
    # Name can cause issues because the same field can have a name in the nested style or partially flattened
    # for example in ecs core
    # http.response.status_code, name is response.status_code
    # http:
    #   fields:
    #       response.status_code
    # but it can also be written:
    # http:
    #   fields:
    #       response:
    #           fields:
    #               status_code
    ignore_validation = ['name']
    if path is None:
        path = []
    for key in b:
        if key in a:
            if key in ignore_keys:
                continue
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict_overwrite(a[key], b[key], validate, path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                if validate and key not in ignore_validation:
                    pp = pprint.PrettyPrinter(indent=2)
                    print('Conflict of values at path: {} using dict B\'s value'.format(
                        '.'.join(path + [str(key)])))
                    print('Dict A:')
                    pp.pprint(a[key])
                    print('Dict B:')
                    pp.pprint(b[key])
                    raise SchemaValidationException('Validation failed')
                # Use the custom dictionary (b)'s value to override the ecs schema one
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


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


def set_short_and_desc(schema):
    if 'description' in schema:
        short = schema['description']
    elif 'title' in schema:
        short = schema['title']
    else:
        short = ''
        # fix up the schema if it is missing a description
        schema['description'] = ''

    if '\n' in short:
        short = short.splitlines()[0]
    dict_set_default(schema, 'short', short)


def schema_set_default_values(schema):
    schema['type'] = 'group'
    dict_set_default(schema, 'group', 2)
    set_short_and_desc(schema)


def schema_set_fieldset_prefix(schema):
    if 'root' in schema and schema['root']:
        schema['prefix'] = ''
    else:
        schema['prefix'] = schema['name'] + '.'


def schema_fields_as_dictionary(schema):
    """Re-nest the array of field names as a dictionary of 'fieldname' => { field definition }"""
    if 'fields' not in schema:
        return
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
        # the `fields` key should not be nested under field_details, to remove it and place it on the outer object
        # if it exists
        moved_inner_fields = field.pop('fields', None)
        cur_node = nested_schema[nested_levels[-1]]
        cur_node['field_details'] = field
        if moved_inner_fields:
            # we need to create a temporary dictionary for the recursion because moved_inner_fields is an array
            # and it's possible that cur_node could already have a `fields` key based on a previous loop
            # this would happen if there was a dot notation field and regular nested field like this:
            # host:
            #   fields:
            #       os.something:
            #           ...
            #       os:
            #           fields:
            moved_temp = {'fields': moved_inner_fields}
            schema_fields_as_dictionary(moved_temp)
            # the fields dictionaries need to be merged because they could mix and match dot and nested notation
            merge_dict_overwrite(cur_node, moved_temp, False)


def field_set_defaults(field):
    if field['type'] == 'keyword':
        dict_set_default(field, 'ignore_above', 1024)
    if field['type'] == 'text':
        dict_set_default(field, 'norms', False)
    if field['type'] == 'object':
        dict_set_default(field, 'object_type', 'keyword')

    set_short_and_desc(field)

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
            # List field set names expected under another field set.
            # E.g. host.nestings = [ 'geo', 'os', 'user' ]
            nestings = fields_nested[new_nesting].setdefault('nestings', [])
            nestings.append(schema['name'])
            nestings.sort()
            fields_nested[new_nesting]['fields'][schema['name']] = schema

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
        if 'fields' in field:
            flat_fields[name]['fields'] = flatten_fields(field['fields'], "")
    return flat_fields


def generate_fully_flattened_fields(fields_nested):
    return flatten_fields(fields_nested, "")


def cleanup_fields_recursive(fields, prefix):
    for name, field in fields.items():
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


def load_schemas(files, validate):
    """Loads the given list of files"""
    return load_schema_files(files, validate)
