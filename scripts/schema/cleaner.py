import copy

from generators import ecs_helpers
from schema import visitor

# This script performs a few cleanup functions in place, within the deeply nested
# 'fields' structure passed to `clean(fields)`.
#
# What happens here:
#
# - check that mandatory attributes are present, without which we can't do much.
# - cleans things up, like stripping spaces, sorting arrays
# - makes lots of defaults explicit
# - pre-calculate a few additional helpful fields
# - converts shorthands into full representation (e.g. reuse locations)
#
# This script only deals with field sets themselves and the fields defined
# inside them. It doesn't perform field reuse, and therefore doesn't
# deal with final field names either.

def clean(fields):
    visitor.visit_fields(fields, fieldset_func=schema_cleanup, field_func=field_cleanup)


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
        schema['schema_details']['prefix'] = ''
    else:
        schema['schema_details']['prefix'] = schema['field_details']['name'] + '.'
    normalize_reuse_notation(schema)
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
    if 'reusable' in schema['schema_details']:
        reuse_attributes = sorted(schema['schema_details']['reusable'].keys())
        missing_reuse_attributes = ecs_helpers.list_subtract(['expected', 'top_level'], reuse_attributes)
        if len(missing_reuse_attributes) > 0:
            msg = "Reusable schema {} is missing the following reuse attributes: {}.\nFound these: {}".format(
                    schema['field_details']['name'], ', '.join(missing_reuse_attributes), reuse_attributes)
            raise ValueError(msg)


def schema_assertions_and_warnings(schema):
    '''Additional checks on a fleshed out schema'''
    single_line_short_description(schema)


def normalize_reuse_notation(schema):
    """
    Replace single word reuse shorthands from the schema YAMLs with the explicit {at: , as:} notation.

    When marking "user" as reusable under "destination" with the shorthand entry
    `- destination`, this is expanded to the complete entry
    `- { "at": "destination", "as": "user" }`.
    The field set is thus nested at `destination.user.*`, with fields such as `destination.user.name`.

    The dictionary notation enables nesting a field set as a different name.
    An example is nesting "process" fields to capture parent process details
    at `process.parent.*`.
    The dictionary notation `- { "at": "process", "as": "parent" }` will yield
    fields such as `process.parent.pid`.
    """
    if 'reusable' not in schema['schema_details']:
        return
    schema_name = schema['field_details']['name']
    reuse_entries = []
    for reuse_entry in schema['schema_details']['reusable']['expected']:
        if type(reuse_entry) is dict: # Already explicit
            if 'at' in reuse_entry and 'as' in reuse_entry:
                explicit_entry = reuse_entry
            else:
                raise ValueError("When specifying reusable expected locations for {} " +
                                 "with the dictionary notation, keys 'as' and 'at' are required. " +
                                 "Got {}.".format(schema_name, reuse_entry))
        else: # Make it explicit
            explicit_entry = {'at': reuse_entry, 'as': schema_name}
        explicit_entry['full'] = explicit_entry['at'] + '.' + explicit_entry['as']
        reuse_entries.append(explicit_entry)
    schema['schema_details']['reusable']['expected'] = reuse_entries


# Field level cleanup


def field_cleanup(field):
    field_mandatory_attributes(field)
    if is_intermediate(field):
        return
    ecs_helpers.dict_clean_string_values(field['field_details'])
    if 'allowed_values' in field['field_details']:
        for allowed_value in field['field_details']['allowed_values']:
            ecs_helpers.dict_clean_string_values(allowed_value)
    field_defaults(field)
    field_assertions_and_warnings(field)


def field_defaults(field):
    field['field_details'].setdefault('short', field['field_details']['description'])
    field['field_details'].setdefault('normalize', [])
    field_or_multi_field_datatype_defaults(field['field_details'])
    if 'multi_fields' in field['field_details']:
        for mf in field['field_details']['multi_fields']:
            field_or_multi_field_datatype_defaults(mf)
            if 'name' not in mf:
                mf['name'] = mf['type']


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

# Common


def single_line_short_description(schema_or_field):
    if "\n" in schema_or_field['field_details']['short']:
        msg = ("Short descriptions must be single line.\n" +
            "Fieldset: '{}'\n{}".format(schema_or_field['field_details']['name'], schema_or_field))
        raise ValueError(msg)
