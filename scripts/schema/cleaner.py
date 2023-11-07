# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import re
from typing import (
    Dict,
    List,
    Optional,
    Union,
)

from generators import ecs_helpers
from schema import visitor
from _types import (
    Field,
    FieldDetails,
    FieldEntry,
    MultiField,
)

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

strict_mode: Optional[bool]  # work-around from https://github.com/python/mypy/issues/5732


def clean(fields: Dict[str, Field], strict: Optional[bool] = False) -> None:
    global strict_mode
    strict_mode = strict
    visitor.visit_fields(fields, fieldset_func=schema_cleanup, field_func=field_cleanup)


# Schema level cleanup


def schema_cleanup(schema: FieldEntry) -> None:
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
    if 'reusable' in schema['schema_details']:
        # order to perform chained reuses. Set to 1 if it needs to happen earlier.
        schema['schema_details']['reusable'].setdefault('order', 2)
    # Precalculate stuff. Those can't be set in the YAML.
    if schema['schema_details']['root']:
        schema['schema_details']['prefix'] = ''
    else:
        schema['schema_details']['prefix'] = schema['field_details']['name'] + '.'
    normalize_reuse_notation(schema)
    # Final validity check if in strict mode
    schema_assertions_and_warnings(schema)


SCHEMA_MANDATORY_ATTRIBUTES = ['name', 'title', 'description']


def schema_mandatory_attributes(schema: FieldEntry) -> None:
    """Ensures for the presence of the mandatory schema attributes and raises if any are missing"""
    current_schema_attributes: List[str] = sorted(list(schema['field_details'].keys()) +
                                                  list(schema['schema_details'].keys()))
    missing_attributes: List[str] = ecs_helpers.list_subtract(SCHEMA_MANDATORY_ATTRIBUTES, current_schema_attributes)
    if len(missing_attributes) > 0:
        msg = "Schema {} is missing the following mandatory attributes: {}.\nFound these: {}".format(
            schema['field_details']['name'], ', '.join(missing_attributes), current_schema_attributes)
        raise ValueError(msg)
    if 'reusable' in schema['schema_details']:
        reuse_attributes: List[str] = sorted(schema['schema_details']['reusable'].keys())
        missing_reuse_attributes: List[str] = ecs_helpers.list_subtract(['expected', 'top_level'], reuse_attributes)
        if len(missing_reuse_attributes) > 0:
            msg = "Reusable schema {} is missing the following reuse attributes: {}.\nFound these: {}".format(
                schema['field_details']['name'], ', '.join(missing_reuse_attributes), reuse_attributes)
            raise ValueError(msg)


def schema_assertions_and_warnings(schema: FieldEntry) -> None:
    """Additional checks on a fleshed out schema"""
    single_line_short_description(schema, strict=strict_mode)
    if 'beta' in schema['field_details']:
        single_line_beta_description(schema, strict=strict_mode)
    if 'reusable' in schema['schema_details']:
        single_line_short_override_description(schema, strict=strict_mode)


def normalize_reuse_notation(schema: FieldEntry) -> None:
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
        if type(reuse_entry) is dict:  # Already explicit
            if 'at' in reuse_entry and 'as' in reuse_entry:
                explicit_entry = reuse_entry
            else:
                raise ValueError(f"When specifying reusable expected locations for {schema_name} " +
                                 f"with the dictionary notation, keys 'as' and 'at' are required. " +
                                 f"Got {reuse_entry}.")
        else:  # Make it explicit
            explicit_entry = {'at': reuse_entry, 'as': schema_name}
        explicit_entry['full'] = explicit_entry['at'] + '.' + explicit_entry['as']
        reuse_entries.append(explicit_entry)
    schema['schema_details']['reusable']['expected'] = reuse_entries


# Field level cleanup


def field_cleanup(field: FieldDetails) -> None:
    field_mandatory_attributes(field)
    if ecs_helpers.is_intermediate(field):
        return
    ecs_helpers.dict_clean_string_values(field['field_details'])
    if 'allowed_values' in field['field_details']:
        for allowed_value in field['field_details']['allowed_values']:
            ecs_helpers.dict_clean_string_values(allowed_value)
    field_defaults(field)
    field_assertions_and_warnings(field)


def field_defaults(field: FieldDetails) -> None:
    field['field_details'].setdefault('short', field['field_details']['description'])
    field['field_details'].setdefault('normalize', [])
    field_or_multi_field_datatype_defaults(field['field_details'])
    if 'multi_fields' in field['field_details']:
        for mf in field['field_details']['multi_fields']:
            field_or_multi_field_datatype_defaults(mf)
            if 'name' not in mf:
                mf['name'] = mf['type']


def field_or_multi_field_datatype_defaults(field_details: Union[Field, MultiField]) -> None:
    """Sets datatype-related defaults on a canonical field or multi-field entries."""
    if field_details['type'] == 'keyword':
        field_details.setdefault('ignore_above', 1024)
    if field_details['type'] == 'text':
        field_details.setdefault('norms', False)
    # wildcard needs the index param stripped
    if field_details['type'] == 'wildcard':
        field_details.pop('index', None)
    if 'index' in field_details and not field_details['index']:
        field_details.setdefault('doc_values', False)
        field_details.pop('ignore_above', None)


FIELD_MANDATORY_ATTRIBUTES = ['name', 'description', 'type', 'level']
ACCEPTABLE_FIELD_LEVELS = ['core', 'extended', 'custom']


def field_mandatory_attributes(field: FieldDetails) -> None:
    """Ensures for the presence of the mandatory field attributes and raises if any are missing"""
    if ecs_helpers.is_intermediate(field):
        return
    current_field_attributes: List[str] = sorted(field['field_details'].keys())
    missing_attributes: List[str] = ecs_helpers.list_subtract(FIELD_MANDATORY_ATTRIBUTES, current_field_attributes)

    # `alias` fields require a target `path` attribute.
    if field['field_details'].get('type') == 'alias' and 'path' not in current_field_attributes:
        missing_attributes.append('path')
    # `scaled_float` fields require a `scaling_factor` attribute.
    if field['field_details'].get('type') == 'scaled_float' and 'scaling_factor' not in current_field_attributes:
        missing_attributes.append('scaling_factor')

    if len(missing_attributes) > 0:
        msg: str = "Field is missing the following mandatory attributes: {}.\nFound these: {}.\nField details: {}"
        raise ValueError(msg.format(', '.join(missing_attributes),
                                    current_field_attributes, field))


def field_assertions_and_warnings(field: FieldDetails) -> None:
    """Additional checks on a fleshed out field"""
    if not ecs_helpers.is_intermediate(field):
        # check short description length if in strict mode
        single_line_short_description(field, strict=strict_mode)
        if 'beta' in field['field_details']:
            single_line_beta_description(field, strict=strict_mode)
        if 'pattern' in field['field_details']:
            validate_pattern_regex(field['field_details'], strict=strict_mode)
        check_example_value(field, strict=strict_mode)
        if field['field_details']['level'] not in ACCEPTABLE_FIELD_LEVELS:
            msg: str = "Invalid level for field '{}'.\nValue: {}\nAcceptable values: {}".format(
                field['field_details']['name'], field['field_details']['level'],
                ACCEPTABLE_FIELD_LEVELS)
            raise ValueError(msg)

# Common


SHORT_LIMIT = 120


def single_line_short_check(short_to_check: str, short_name: str) -> Union[str, None]:
    short_length: int = len(short_to_check)
    if "\n" in short_to_check or short_length > SHORT_LIMIT:
        msg: str = "Short descriptions must be single line, and under {} characters (current length: {}).\n".format(
            SHORT_LIMIT, short_length)
        msg += "Offending field or field set: {}\nShort description:\n  {}".format(
            short_name,
            short_to_check)
        return msg
    return None


def strict_warning_handler(message, strict):
    """Handles warnings based on --strict mode"""
    if strict:
        raise ValueError(message)
    else:
        ecs_helpers.strict_warning(message)


def single_line_short_description(schema_or_field: FieldEntry, strict: Optional[bool] = True):
    error: Union[str, None] = single_line_short_check(
        schema_or_field['field_details']['short'], schema_or_field['field_details']['name'])
    if error:
        strict_warning_handler(error, strict)


def single_line_short_override_description(schema_or_field: FieldEntry, strict: Optional[bool] = True):
    for field in schema_or_field['schema_details']['reusable']['expected']:
        if not 'short_override' in field:
            continue
        error: Union[str, None] = single_line_short_check(field['short_override'], field['full'])
        if error:
            strict_warning_handler(error, strict)


def check_example_value(field: Union[List, FieldEntry], strict: Optional[bool] = True) -> None:
    """
    Checks if value of the example field is of type list or dict.
    Fails or warns (depending on strict mode) if so.
    """
    example_value: str = field['field_details'].get('example', '')
    pattern: str = field['field_details'].get('pattern', '')
    expected_values: List[str] = field['field_details'].get('expected_values', [])
    name: str = field['field_details']['name']

    if isinstance(example_value, (list, dict)):
        field_name: str = field['field_details']['name']
        msg: str = "Example value for field `{}` contains an object or array which must be quoted to avoid YAML interpretation.".format(
            field_name)
        strict_warning_handler(msg, strict)

    # Examples with arrays must be handled
    if 'array' in field['field_details'].get('normalize', []):
        # strips unnecessary chars in order to split each example value
        example_values = example_value.translate(str.maketrans('', '', '"[] ')).split(',')
    else:
        example_values = [example_value]

    if pattern:
        for example_value in example_values:
            match = re.match(pattern, example_value)
            if not match:
                msg = "Example value for field `{}` does not match the regex defined in the pattern attribute: `{}`.".format(
                    name, pattern)
                strict_warning_handler(msg, strict)

    if expected_values:
        for example_value in example_values:
            if example_value not in expected_values:
                msg = "Example value `{}` for field `{}` is not one of the values defined in `expected_value`: {}.".format(
                    example_value, name, example_values)
                strict_warning_handler(msg, strict)


def single_line_beta_description(schema_or_field: FieldEntry, strict: Optional[bool] = True) -> None:
    if "\n" in schema_or_field['field_details']['beta']:
        msg: str = "Beta descriptions must be single line.\n"
        msg += f"Offending field or field set: {schema_or_field['field_details']['name']}"
        strict_warning_handler(msg, strict)


def validate_pattern_regex(field, strict=True):
    """
    Validates if field['pattern'] contains a valid regular expression.
    """
    try:
        re.compile(field['pattern'])
    except re.error:
        msg = "Pattern value must be a valid regular expression.\n"
        msg += f"Offending field name: {field['name']}"
        strict_warning_handler(msg, strict)
