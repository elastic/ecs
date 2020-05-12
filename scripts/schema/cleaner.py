import copy

from generators import ecs_helpers

# This script performs a few cleanup functions:
# - check that mandatory attributes are present, without which we can't do much.
# - cleans things up, like stripping spaces, sorting arrays
# - makes all defaults explicit
# - pre-calculate additional helpful fields
# - converts shorthands into full representation (e.g. reuse locations)

def clean(fields):
    visit_fields(fields, fieldset_func=schema_cleanup)
    return fields


def visit_fields(fields, fieldset_func=None, field_func=None, path=[]):
    for (name, details) in fields.items():
        current_path = path + [name]
        if fieldset_func and 'schema_details' in details:
            fieldset_func(details)
        # Note that all schemas have field_details as well, so this gets called on them too.
        if field_func and 'field_details' in details:
            field_func(details, current_path)
        if 'fields' in details:
            visit_fields(details['fields'], fieldset_func=fieldset_func, field_func=field_func, path=current_path)


def schema_cleanup(schema):
    # Sanity check first
    schema_mandatory_attributes(schema)
    # trailing space cleanup
    ecs_helpers.dict_clean_string_values(schema['schema_details'])
    ecs_helpers.dict_clean_string_values(schema['field_details'])
    # Some defaults
    schema['schema_details'].setdefault('group', 2)
    schema['schema_details'].setdefault('root', False)
    schema['field_details'].setdefault('type', 'group')
    schema['field_details'].setdefault('short', schema['field_details']['description'])
    # Precalculate stuff. Those can't be set in the YAML.
    if schema['schema_details']['root']:
        schema['schema_details']['prefix'] = ''
    else:
        schema['schema_details']['prefix'] = schema['field_details']['name'] + '.'
    # Final validity check
    schema_assertions_and_warnings(schema)


SCHEMA_MANDATORY_ATTRIBUTES = ['name', 'title', 'description']


def schema_mandatory_attributes(schema):
    '''Ensures for the presence of the mandatory schema attributes and raises if any are missing'''
    current_schema_attributes = sorted(list(schema['field_details'].keys()) +
            list(schema['schema_details'].keys()))
    missing_attributes = ecs_helpers.list_subtract(SCHEMA_MANDATORY_ATTRIBUTES, current_schema_attributes)
    if len(missing_attributes) > 0:
        msg = "Schema {} is missing the following mandatory attributes: {}.\nFound these: {}".format(
                schema['field_details']['name'], ', '.join(missing_attributes), current_schema_attributes)
        raise ValueError(msg)


def schema_assertions_and_warnings(schema):
    '''Additional checks on a fleshed out schema'''
    single_line_short_description(schema)


def field_cleanup(field, path):
    field_mandatory_attributes(field)
    # Fill in defaults
    # Precalculate stuff. Those can't be set in the YAML.
    # Final validity check
    field_assertions_and_warnings(field)


FIELD_MANDATORY_ATTRIBUTES = ['name', 'description', 'type', 'level']


def field_mandatory_attributes(field):
    '''Ensures for the presence of the mandatory field attributes and raises if any are missing'''
    current_field_attributes = sorted(field['field_details'].keys())
    missing_attributes = ecs_helpers.list_subtract(FIELD_MANDATORY_ATTRIBUTES, current_field_attributes)
    if len(missing_attributes) > 0:
        msg = "Field is missing the following mandatory attributes: {}.\nFound these: {}.\nField details: {}".format(', '.join(missing_attributes),
                current_field_attributes,
                field)
        raise ValueError(msg)


def field_assertions_and_warnings(field):
    '''Additional checks on a fleshed out field'''
    single_line_short_description(field)


def single_line_short_description(schema_or_field):
    if "\n" in schema_or_field['field_details']['short']:
        msg = ("Short descriptions must be single line.\n" +
            "Fieldset: {}\n{}".format(schema_or_field['field_details']['name'], schema_or_field))
        raise ValueError(msg)


        # # Both 'fields' and 'field_details' can be present (e.g. when type=object like dns.answers)
        # if 'field_details' in nested:   # it's a field!
        #     field_func(current_nesting, nested['field_details'])
        # if 'fields' in nested:          # it has nested fields!
        #     recurse_fields(field_func, nested['fields'], current_nesting)

    # # fieldset attributes at same level, not nested under 'field_details'
    # is_fieldset = (fields.get('type', None) == 'group' and
        #           type(fields.get('fields', None)) == dict and
        #           [] == field_nesting)
    # if is_fieldset:
        # if 'root' in fields:
        #     current_nesting = []
        # else:
        #     current_nesting = [fields['name']]
        # fields = fields['fields']
    # else:
        # current_nesting = [fields['name']]

    # for (name, nested) in fields.items():
        # # if 'root' in nested: # should only be "base" fields
        # #     current_nesting = field_nesting
        # # else:
        # #     current_nesting = field_nesting + [name]

        # # Both 'fields' and 'field_details' can be present (e.g. when type=object like dns.answers)
        # if 'field_details' in nested:   # it's a field!
        #     field_func(current_nesting, nested['field_details'])
        # if 'fields' in nested:          # it has nested fields!
        #     recurse_fields(field_func, nested['fields'], current_nesting)


