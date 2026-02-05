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

"""Schema Cleaner Module.

Validates, normalizes, and enriches schema definitions after loading.
Second stage of pipeline: loader.py → cleaner.py → finalizer.py

Key operations:
- Validates mandatory attributes (name, title, description, type, level)
- Sets defaults (group=2, root=false, ignore_above=1024 for keywords, etc.)
- Expands reuse shorthand notation
- Validates descriptions, examples, and patterns

In strict mode (--strict), warnings become exceptions.

See scripts/docs/schema-pipeline.md for complete documentation.
"""

import re
from typing import (
    Dict,
    List,
    Optional,
    Union,
)

from generators import ecs_helpers
from schema import visitor
from ecs_types import (
    Field,
    FieldDetails,
    FieldEntry,
    MultiField,
)

strict_mode: Optional[bool]  # work-around from https://github.com/python/mypy/issues/5732


def clean(fields: Dict[str, Field], strict: Optional[bool] = False) -> None:
    """Clean, validate, and enrich schema definitions in place.

    Args:
        fields: Deeply nested field dictionary from loader.py
        strict: If True, warnings become exceptions

    Raises:
        ValueError: If mandatory attributes are missing or invalid
    """
    global strict_mode
    strict_mode = strict
    visitor.visit_fields(fields, fieldset_func=schema_cleanup, field_func=field_cleanup)


# Schema level cleanup


def schema_cleanup(schema: FieldEntry) -> None:
    """Clean and enrich a fieldset: validate, set defaults, expand reuse notation."""
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
    """Validate mandatory attributes (name, title, description) are present."""
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
    """Perform additional validation checks on enriched fieldset.

    Called after defaults are filled in and normalization is complete.
    Validates quality constraints like description length and format.

    Args:
        schema: Fieldset entry to validate

    Side Effects:
        May print warnings or raise exceptions depending on strict_mode

    Checks Performed:
        - Short description is single line and under 120 characters
        - Beta description (if present) is single line
        - Reuse short_override descriptions (if present) are single line

    Note:
        Behavior depends on global strict_mode variable:
        - strict=False: Prints warnings
        - strict=True: Raises exceptions
    """
    single_line_short_description(schema, strict=strict_mode)
    if 'beta' in schema['field_details']:
        single_line_beta_description(schema, strict=strict_mode)
    if 'reusable' in schema['schema_details']:
        single_line_short_override_description(schema, strict=strict_mode)


def normalize_reuse_notation(schema: FieldEntry) -> None:
    """Expand shorthand reuse notation to explicit {at:, as:} dictionary format.

    Schema YAMLs allow two formats for specifying where a fieldset should be reused:

    1. Shorthand string: 'destination'
       Expands to: {'at': 'destination', 'as': 'user'}
       Results in: destination.user.* fields

    2. Explicit dict: {'at': 'process', 'as': 'parent'}
       Already explicit, just validated
       Results in: process.parent.* fields

    This function normalizes both formats to the explicit dictionary form and
    calculates the 'full' path for convenience.

    Args:
        schema: Fieldset entry (only processed if reusable)

    Side Effects:
        Modifies schema['schema_details']['reusable']['expected'] in place,
        converting all entries to explicit dictionary format with 'full' key

    Raises:
        ValueError: If dictionary notation is incomplete (missing 'at' or 'as')

    Reuse Examples:
        Shorthand:
        ```yaml
        reusable:
          expected:
            - destination  # Shorthand
        ```
        Becomes:
        {'at': 'destination', 'as': 'user', 'full': 'destination.user'}

        Explicit:
        ```yaml
        reusable:
          expected:
            - at: process
              as: parent
        ```
        Becomes:
        {'at': 'process', 'as': 'parent', 'full': 'process.parent'}

    Use Cases:
        - 'user' reused at 'destination', 'source', 'client', 'server'
        - 'process' reused as 'process.parent' (self-nesting)
        - 'geo' reused under 'client.geo', 'server.geo' (not top-level)

    Note:
        The 'full' path is used by downstream stages to quickly identify
        where fields will appear after reuse is performed.
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
    """Clean, validate, and enrich a single field definition.

    Performs all cleanup operations for a field:
    - Validates mandatory attributes
    - Strips whitespace (unless intermediate field)
    - Fills in defaults
    - Validates constraints

    Args:
        field: Field entry with 'field_details' and optionally 'fields'

    Side Effects:
        Modifies field dictionary in place

    Raises:
        ValueError: If mandatory attributes missing or invalid

    Processing Steps:
        1. Validate mandatory attributes present
        2. Skip further processing if intermediate field
        3. Clean string values (strip whitespace)
        4. Clean allowed_values if present
        5. Apply datatype-specific defaults
        6. Validate constraints (examples, patterns, etc.)

    Note:
        Intermediate fields are skipped because they're auto-generated
        structural fields, not real data fields.

        Called by visitor for each field during traversal.
    """
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
    """Apply default values for optional field attributes.

    Sets sensible defaults based on field type, reducing boilerplate in
    schema YAML files. Also processes multi-fields.

    Args:
        field: Field entry to enrich with defaults

    Side Effects:
        Modifies field dictionary in place

    Defaults Applied:
        General:
        - short: Copy of description (if not specified)
        - normalize: [] (empty array if not specified)

        Type-specific (see field_or_multi_field_datatype_defaults):
        - keyword: ignore_above=1024
        - text: norms=false
        - fields with index=false: doc_values=false

        Multi-fields:
        - name: type name if not specified (e.g., 'text', 'keyword')

    Note:
        Multi-fields get their own defaults applied recursively.
    """
    field['field_details'].setdefault('short', field['field_details']['description'])
    field['field_details'].setdefault('normalize', [])
    field_or_multi_field_datatype_defaults(field['field_details'])
    if 'multi_fields' in field['field_details']:
        for mf in field['field_details']['multi_fields']:
            field_or_multi_field_datatype_defaults(mf)
            if 'name' not in mf:
                mf['name'] = mf['type']


def field_or_multi_field_datatype_defaults(field_details: Union[Field, MultiField]) -> None:
    """Apply datatype-specific defaults to field or multi-field.

    Different Elasticsearch field types have different sensible defaults.
    This function applies appropriate defaults based on the 'type' attribute.

    Args:
        field_details: Field or multi-field definition dict

    Side Effects:
        Modifies field_details dictionary in place

    Defaults by Type:
        - keyword: ignore_above=1024 (truncate very long values)
        - text: norms=false (save space, usually not needed for search)
        - wildcard: Remove 'index' param (not applicable)
        - index=false: doc_values=false, remove ignore_above

    Rationale:
        - ignore_above prevents errors from very long strings
        - norms=false is common for log data (saves significant space)
        - doc_values=false with index=false is an optimization
        - wildcard fields don't support some parameters

    Note:
        Works for both regular fields and multi-fields (same logic applies).
    """
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
    """Validate that all mandatory field attributes are present.

    Checks for required attributes with special handling for type-specific
    requirements (alias, scaled_float).

    Args:
        field: Field entry to validate

    Raises:
        ValueError: If any mandatory attributes are missing

    Mandatory Attributes:
        All fields:
        - name: Field identifier
        - description: Field description
        - type: Elasticsearch field type
        - level: Field level (core/extended/custom)

        Type-specific:
        - alias fields: Also require 'path' (target field)
        - scaled_float fields: Also require 'scaling_factor'

    Note:
        Intermediate fields (auto-created parents) are skipped as they
        don't need full validation.

    Example:
        >>> field = {
        ...     'field_details': {
        ...         'name': 'method',
        ...         'description': '...'
        ...         # Missing 'type' and 'level'
        ...     }
        ... }
        >>> field_mandatory_attributes(field)
        ValueError: Field is missing the following mandatory attributes: type, level
    """
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
    """Perform additional validation checks on enriched field.

    Called after defaults are filled in and normalization is complete.
    Validates quality constraints and semantic correctness.

    Args:
        field: Field entry to validate

    Side Effects:
        May print warnings or raise exceptions depending on strict_mode

    Checks Performed:
        - Short description is single line and under 120 characters
        - Beta description (if present) is single line
        - Pattern (if present) is valid regex
        - Example value matches pattern/expected_values
        - Level is one of: core, extended, custom

    Raises:
        ValueError: Always for invalid level (regardless of strict mode)

    Note:
        Behavior depends on global strict_mode variable:
        - strict=False: Prints warnings for most issues
        - strict=True: Raises exceptions for all issues
        - Invalid level always raises (can't continue with invalid level)
    """
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

# Common Validation Helpers


SHORT_LIMIT = 120


def single_line_short_check(short_to_check: str, short_name: str) -> Union[str, None]:
    """Check if a short description meets formatting requirements.

    Validates that a short description is:
    - Single line (no newline characters)
    - Under 120 characters long

    Args:
        short_to_check: Short description string to validate
        short_name: Name of field/fieldset (for error messages)

    Returns:
        Error message string if validation fails, None if valid

    Note:
        Does not raise or warn directly; returns error message for caller
        to handle based on strict mode.
    """
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
    """Handle validation messages based on strict mode.

    Args:
        message: Validation error/warning message
        strict: Whether to treat as error (True) or warning (False)

    Raises:
        ValueError: If strict=True

    Side Effects:
        Prints warning if strict=False

    Note:
        This centralized handler allows consistent behavior across all
        validation checks.
    """
    if strict:
        raise ValueError(message)
    else:
        ecs_helpers.strict_warning(message)


def single_line_short_description(schema_or_field: FieldEntry, strict: Optional[bool] = True):
    """Validate that short description is single line and under limit.

    Args:
        schema_or_field: Field or fieldset entry to validate
        strict: Whether to raise exception (True) or print warning (False)

    Raises:
        ValueError: If validation fails and strict=True

    Side Effects:
        Prints warning if validation fails and strict=False
    """
    error: Union[str, None] = single_line_short_check(
        schema_or_field['field_details']['short'], schema_or_field['field_details']['name'])
    if error:
        strict_warning_handler(error, strict)


def single_line_short_override_description(schema_or_field: FieldEntry, strict: Optional[bool] = True):
    """Validate that reuse short_override descriptions are single line.

    When a fieldset is reused, it can have custom short descriptions for
    each reuse location. This validates all such overrides.

    Args:
        schema_or_field: Fieldset entry with reusable expected locations
        strict: Whether to raise exception (True) or print warning (False)

    Raises:
        ValueError: If validation fails and strict=True

    Side Effects:
        Prints warning if validation fails and strict=False

    Note:
        Only validates short_override if present; it's optional.
    """
    for field in schema_or_field['schema_details']['reusable']['expected']:
        if not 'short_override' in field:
            continue
        error: Union[str, None] = single_line_short_check(field['short_override'], field['full'])
        if error:
            strict_warning_handler(error, strict)


def check_example_value(field: Union[List, FieldEntry], strict: Optional[bool] = True) -> None:
    """Validate example value meets field constraints.

    Performs several validation checks on the example value:
    1. Not a YAML-interpreted object/array (should be quoted string)
    2. Matches pattern regex (if pattern specified)
    3. In expected_values list (if expected_values specified)

    Args:
        field: Field entry with field_details
        strict: Whether to raise exception (True) or print warning (False)

    Raises:
        ValueError: If validation fails and strict=True

    Side Effects:
        Prints warning if validation fails and strict=False

    Example Value Formats:
        - Simple: "GET"
        - Array: '["GET", "POST"]' (must be quoted to avoid YAML parsing)
        - With pattern: Must match the regex in 'pattern' attribute

    Special Handling:
        - Array fields (normalize contains 'array'): Parses and validates each value
        - Missing example: Skipped (example is optional)

    Common Issues:
        - Unquoted array: [GET, POST] becomes Python list → Error
          Fix: Quote it: "[GET, POST]"
        - Pattern mismatch: Example doesn't match validation regex
        - Invalid enum: Example not in expected_values list

    Note:
        This prevents documentation from containing invalid or misleading examples.
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
    """Validate that beta description is single line.

    Beta fields/fieldsets have a 'beta' attribute explaining why they're
    in beta. This must be a single line for consistency.

    Args:
        schema_or_field: Field or fieldset entry with beta attribute
        strict: Whether to raise exception (True) or print warning (False)

    Raises:
        ValueError: If validation fails and strict=True

    Side Effects:
        Prints warning if validation fails and strict=False
    """
    if "\n" in schema_or_field['field_details']['beta']:
        msg: str = "Beta descriptions must be single line.\n"
        msg += f"Offending field or field set: {schema_or_field['field_details']['name']}"
        strict_warning_handler(msg, strict)


def validate_pattern_regex(field, strict=True):
    """Validate that pattern attribute is a valid regular expression.

    Some fields have a 'pattern' attribute specifying a validation regex.
    This ensures the pattern itself is syntactically valid.

    Args:
        field: Field definition dict with 'pattern' attribute
        strict: Whether to raise exception (True) or print warning (False)

    Raises:
        ValueError: If validation fails and strict=True

    Side Effects:
        Prints warning if validation fails and strict=False

    Note:
        Uses Python's re.compile() to test validity.
        Invalid patterns would cause runtime errors if not caught here.
    """
    try:
        re.compile(field['pattern'])
    except re.error:
        msg = "Pattern value must be a valid regular expression.\n"
        msg += f"Offending field name: {field['name']}"
        strict_warning_handler(msg, strict)
