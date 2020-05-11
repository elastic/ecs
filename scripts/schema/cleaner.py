import copy

from generators import ecs_helpers

# This script performs a few cleanup functions:
# - check that mandatory attributes are present, without which we can't do much.
# - cleans things up, like stripping spaces, sorting arrays
# - makes all defaults explicit
# - pre-calculate additional helpful fields
# - converts shorthands into full representation (e.g. reuse locations)

def clean(fields):
    return fields


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


MANDATORY_SCHEMA_ATTRIBUTES = ['name', 'title', 'description']


def schema_mandatory_attributes(schema):
    '''Checks for the presence of the mandatory attributes and raises if any are missing'''
    current_schema_attributes = sorted(list(schema['field_details'].keys()) +
            list(schema['schema_details'].keys()))
    missing_attributes = ecs_helpers.list_subtract(MANDATORY_SCHEMA_ATTRIBUTES, current_schema_attributes)
    if len(missing_attributes) > 0:
        msg = "Schema {} is missing the following mandatory attributes: {}.\nFound these: {}".format(
                schema['field_details']['name'], ', '.join(missing_attributes), current_schema_attributes)
        raise ValueError(msg)

# def field_cleanup(field, path):


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


