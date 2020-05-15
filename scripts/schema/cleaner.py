import copy

from generators import ecs_helpers

# This script performs a few cleanup functions:
# - check that mandatory attributes are present, without which we can't do much.
# - cleans things up, like stripping spaces, sorting arrays
# - makes all defaults explicit
# - pre-calculate additional helpful fields
# - converts shorthands into full representation (e.g. reuse locations)

def clean(fields):
    visit_fields(fields, fieldset_func=schema_cleanup) #, field_func=field_cleanup)
    return fields


# Schema level cleanup


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
        # schema['field_details']['path'] = []
        schema['schema_details']['prefix'] = ''
    else:
        # schema['field_details']['path'] = [schema['field_details']['name']]
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

# Field level cleanup


def field_cleanup(field):
    field_mandatory_attributes(field)
    # field_precalculated(field)
    if not is_intermediate(field):
        ecs_helpers.dict_clean_string_values(field['field_details'])
        field_defaults(field)
        field_assertions_and_warnings(field)


# def field_precalculated(field):
#     if schema['schema_details']['root']:
#         namespace = ''
#     else:
#         namespace = schema['field_details']['name'] + '.'
#         field['field_details']['path'] + [field['field_details']['name']]
#         name_parts = field['field_details']['path'] + [field['field_details']['name']]
#     field['field_details']['flat_name'] = '.'.join(name_parts)
#     field['field_details']['dashed_name'] = field['field_details']['flat_name'].replace('.', '-').replace('_', '-')


def field_defaults(field):
    field['field_details'].setdefault('short', field['field_details']['description'])
    field['field_details'].setdefault('normalize', [])
    field_or_multi_field_datatype_defaults(field['field_details'])
    if 'multi_fields' in field['field_details']:
        for mf in field['field_details']['multi_fields']:
            field_or_multi_field_datatype_defaults(mf)
            if 'name' not in mf:
                mf['name'] = mf['type']
            # # Precalculated values for multi-fields
            # mf['flat_name'] = field['field_details']['flat_name'] + '.' + mf['name']


def field_or_multi_field_datatype_defaults(field_details):
    '''Sets datatype-related defaults on a canonical field or multi-field entries.'''
    if field_details['type'] == 'keyword':
        field_details.setdefault('ignore_above', 1024)
    if field_details['type'] == 'text':
        field_details.setdefault('norms', False)
    if 'index' in field_details and not field_details['index']:
        field_details.setdefault('doc_values', False)


def is_intermediate(field):
    '''Encapsulates the check to see if a field is an intermediate field or a "real" field.'''
    return ('intermediate' in field['field_details'] and field['field_details']['intermediate'])


FIELD_MANDATORY_ATTRIBUTES = ['name', 'description', 'type', 'level']
ACCEPTABLE_FIELD_LEVELS = ['core', 'extended', 'custom']


def field_mandatory_attributes(field):
    '''Ensures for the presence of the mandatory field attributes and raises if any are missing'''
    if is_intermediate(field):
        return
    current_field_attributes = sorted(field['field_details'].keys())
    missing_attributes = ecs_helpers.list_subtract(FIELD_MANDATORY_ATTRIBUTES, current_field_attributes)
    if len(missing_attributes) > 0:
        msg = "Field is missing the following mandatory attributes: {}.\nFound these: {}.\nField details: {}"
        raise ValueError(msg.format(', '.join(missing_attributes),
            current_field_attributes, field))


def field_assertions_and_warnings(field):
    '''Additional checks on a fleshed out field'''
    if not is_intermediate(field):
        single_line_short_description(field)
        if field['field_details']['level'] not in ACCEPTABLE_FIELD_LEVELS:
            msg = "Invalid level for field '{}'.\nValue: {}\nAcceptable values: {}".format(
                    field['field_details']['name'], field['field_details']['level'],
                    ACCEPTABLE_FIELD_LEVELS)
            raise ValueError(msg)

# Common stuff


def single_line_short_description(schema_or_field):
    if "\n" in schema_or_field['field_details']['short']:
        msg = ("Short descriptions must be single line.\n" +
            "Fieldset: '{}'\n{}".format(schema_or_field['field_details']['name'], schema_or_field))
        raise ValueError(msg)


def visit_fields(fields, fieldset_func=None, field_func=None, fieldset_prefix=None):
    '''
    This function navigates the deeply nested tree structure and runs provided
    functions on each fieldset or field encountered (both optional).

    The function caller should not provide a value for the 'fieldset_prefix' argument,
    as this is populated automatically as visit_fields recursively descends into
    the tree.

    The 'fieldset_func' provided will be called with one argument, the dictionary containing
    all fieldset details ({'schema_details': {}, 'field_details': {}, 'fields': {}).

    The 'field_func' provided will be called with two arguments:
    - first is the field details ({'field_details': {}, 'fields': {})
    - second is the fieldset_namespace, an array used to calculate the full path to the field.
    '''
    for (name, details) in fields.items():
        current_fieldset = fieldset
        if 'schema_details' in details:
            current_fieldset = details
            if fieldset_func:
                fieldset_func(details)
        else:
            # We don't apply the same standard on a schema's "field_details" as we do
            # on actual fields, so this only calls the function on real fields.
            if field_func and 'field_details' in details:
                field_func(details, current_fieldset)
        if 'fields' in details:
            visit_fields(details['fields'],
                    fieldset_func=fieldset_func,
                    field_func=field_func,
                    fieldset_prefix=fieldset_prefix)
