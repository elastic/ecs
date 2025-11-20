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

"""Schema Finalizer Module.

This module performs field reuse and calculates final field names. It's the third
stage of the schema processing pipeline, after loader and cleaner:

    loader.py → cleaner.py → finalizer.py → intermediate_files.py

The finalizer performs two critical operations:
1. **Field Reuse**: Copy fieldsets to multiple locations (composition)
2. **Name Calculation**: Compute flat_name, dashed_name for all fields

Field Reuse Mechanism:
    ECS uses composition to avoid repetition. Common fieldsets like 'user', 'geo',
    and 'process' can be reused at multiple locations. For example:

    - user → destination.user, source.user, client.user, server.user
    - geo → client.geo, destination.geo, host.geo (but NOT at root level)
    - process → process.parent (self-nesting for parent process)

Two Phases of Reuse:

    **Phase 1: Foreign Reuse (Across Fieldsets)**
    Copy a fieldset into a different fieldset. Example:
    - 'user' → 'destination.user.*'
    - Fields: destination.user.name, destination.user.email, etc.
    - Transitive: If 'group' is reused in 'user', then 'destination.user'
      automatically contains 'destination.user.group.*'

    **Phase 2: Self-Nesting (Within Same Fieldset)**
    Copy a fieldset into itself with a different name. Example:
    - 'process' → 'process.parent.*'
    - Fields: process.parent.pid, process.parent.name, etc.
    - NOT transitive: 'source.process' does NOT get 'source.process.parent'

    Key Difference: Phase 1 reuse is transitive (carried along when destination
    is also reused). Phase 2 reuse is local only (not propagated).

Reuse Order:
    Some fieldsets depend on others being reused first. The 'order' attribute
    controls reuse sequence:
    - order=1: Reused first (e.g., 'group' must be in 'user' before 'user' is reused)
    - order=2: Default priority (most fieldsets)

    Within each order level, Phase 1 (foreign) happens before Phase 2 (self-nesting).

Tracking Reuse:
    - original_fieldset: Set on all reused fields to track their source
    - reused_here: List on receiving fieldset showing what was reused into it
    - nestings: Legacy list of nested fieldset names (maintained for compatibility)

Final Field Names:
    After reuse is complete, calculates:
    - flat_name: Full dotted name (e.g., 'destination.user.name')
    - dashed_name: Kebab-case version (e.g., 'destination-user-name')
    - Multi-field flat_names: e.g., 'user.name.text'

Example:
    >>> from schema import loader, cleaner, finalizer
    >>> fields = loader.load_schemas()
    >>> cleaner.clean(fields)
    >>> finalizer.finalize(fields)
    # Now fields contain all reused copies and have final names calculated

See also: scripts/docs/schema-pipeline.md for complete pipeline documentation
"""

import copy
import re

from schema import visitor


def finalize(fields):
    """Finalize schemas by performing reuse and calculating final field names.

    This is the main entry point for the finalizer module. It orchestrates
    the two-phase reuse process and then calculates all final field properties.

    Args:
        fields: Deeply nested field dictionary from cleaner.py

    Side Effects:
        Modifies fields dictionary in place:
        - Adds reused fieldset copies at specified locations
        - Sets original_fieldset on all reused fields
        - Calculates flat_name, dashed_name for all fields
        - Sets multi-field flat_names
        - Adds reused_here metadata to receiving fieldsets

    Processing Steps:
        1. Perform field reuse (two-phase, respecting order)
        2. Calculate final values (names and derived properties)

    Example:
        >>> fields = loader.load_schemas()
        >>> cleaner.clean(fields)
        >>> finalize(fields)
        # Fields now contain all reused copies with calculated names
    """
    perform_reuse(fields)
    calculate_final_values(fields)


def order_reuses(fields):
    """Organize reuse operations by priority order and phase type.

    Examines all reusable fieldsets and categorizes their reuse locations into:
    - Foreign reuses (Phase 1): Reuse into different fieldset
    - Self-nestings (Phase 2): Reuse into same fieldset

    Both are grouped by 'order' priority for sequential processing.

    Args:
        fields: Deeply nested field dictionary

    Returns:
        Tuple of (foreign_reuses, self_nestings):
        - foreign_reuses: {order: {schema_name: [reuse_entries]}}
        - self_nestings: {order: {schema_name: [reuse_entries]}}

    Structure Example:
        foreign_reuses = {
            1: {  # Order 1 (high priority)
                'group': [
                    {'at': 'user', 'as': 'group', 'full': 'user.group'}
                ]
            },
            2: {  # Order 2 (default priority)
                'user': [
                    {'at': 'destination', 'as': 'user', 'full': 'destination.user'},
                    {'at': 'source', 'as': 'user', 'full': 'source.user'}
                ]
            }
        }

        self_nestings = {
            2: {
                'process': [
                    {'at': 'process', 'as': 'parent', 'full': 'process.parent'}
                ]
            }
        }

    Note:
        - Foreign vs self determined by comparing source and destination fieldset names
        - Order values typically 1 (high priority) or 2 (default)
        - Used by perform_reuse() to execute reuses in correct sequence
    """
    foreign_reuses = {}
    self_nestings = {}
    for schema_name, schema in fields.items():
        if not 'reusable' in schema['schema_details']:
            continue
        reuse_order = schema['schema_details']['reusable']['order']
        for reuse_entry in schema['schema_details']['reusable']['expected']:
            destination_schema_name = reuse_entry['full'].split('.')[0]
            if destination_schema_name == schema_name:
                # Accumulate self-nestings for phase 2.
                self_nestings.setdefault(reuse_order, {})
                self_nestings[reuse_order].setdefault(destination_schema_name, [])
                self_nestings[reuse_order][destination_schema_name].extend([reuse_entry])
            else:
                # Group foreign reuses by 'order' attribute.
                foreign_reuses.setdefault(reuse_order, {})
                foreign_reuses[reuse_order].setdefault(schema_name, [])
                foreign_reuses[reuse_order][schema_name].extend([reuse_entry])
    return foreign_reuses, self_nestings


def perform_reuse(fields):
    """Execute all field reuse operations in correct order and phases.

    Orchestrates the two-phase reuse process, respecting priority order.
    For each order level (1, 2, etc.):
    1. Phase 1: Foreign reuses (transitive)
    2. Phase 2: Self-nestings (non-transitive)

    Args:
        fields: Deeply nested field dictionary

    Side Effects:
        Modifies fields dictionary in place by:
        - Adding reused field copies at destination locations
        - Marking all copied fields with original_fieldset
        - Setting intermediate=True on reused fieldset wrappers
        - Recording reused_here metadata on destination fieldsets

    Reuse Process:
        1. Organize reuses by order and type (foreign vs self)
        2. For each order (sorted, low to high):
           a. Phase 1: Process all foreign reuses at this order
              - Deep copy source fieldset's fields
              - Mark all with original_fieldset
              - Place at destination location
           b. Phase 2: Process all self-nestings at this order
              - Make pristine copy before any self-nesting
              - Deep copy for each self-nesting location
              - Place under same fieldset

    Example:
        Order 1:
        - Foreign: group → user.group
        Order 2:
        - Foreign: user (now containing group) → destination.user (includes group!)
        - Self: process → process.parent

    Transitive Behavior:
        Foreign reuses are transitive:
        - If A is reused in B, and B is reused in C, then C gets A too
        - Example: group in user, user in destination → destination.user.group

        Self-nestings are NOT transitive:
        - If A self-nests as A.parent, reusing A elsewhere doesn't include A.parent
        - Example: process.parent exists, but source.process.parent does NOT

    Note:
        Uses deep copy to avoid sharing references between locations.
        Each reused location gets independent field copies.
    """
    foreign_reuses, self_nestings = order_reuses(fields)

    # Process foreign reuses and self-nestings together, respecting order
    all_orders = sorted(set(list(foreign_reuses.keys()) + list(self_nestings.keys())))

    for order in all_orders:
        # Phase 1: foreign reuse for this order
        if order in foreign_reuses:
            for schema_name, reuse_entries in foreign_reuses[order].items():
                schema = fields[schema_name]
                for reuse_entry in reuse_entries:
                    nest_as = reuse_entry['as']
                    destination_schema_name = reuse_entry['full'].split('.')[0]
                    destination_schema = fields[destination_schema_name]
                    ensure_valid_reuse(schema, destination_schema)

                    new_field_details = copy.deepcopy(schema['field_details'])
                    new_field_details['name'] = nest_as
                    new_field_details['original_fieldset'] = schema_name
                    new_field_details['intermediate'] = True
                    reused_fields = copy.deepcopy(schema['fields'])
                    set_original_fieldset(reused_fields, schema_name)
                    destination_fields = field_group_at_path(reuse_entry['at'], fields)
                    destination_fields[nest_as] = {
                        'field_details': new_field_details,
                        'fields': reused_fields,
                    }
                    append_reused_here(schema, reuse_entry, destination_schema)

        # Phase 2: self-nesting for this order
        if order in self_nestings:
            for schema_name, reuse_entries in self_nestings[order].items():
                schema = fields[schema_name]
                ensure_valid_reuse(schema)
                # Since we're about self-nest more fields within these, make a pristine copy first
                reused_fields = copy.deepcopy(schema['fields'])
                set_original_fieldset(reused_fields, schema_name)
                for reuse_entry in reuse_entries:
                    nest_as = reuse_entry['as']
                    new_field_details = copy.deepcopy(schema['field_details'])
                    new_field_details['name'] = nest_as
                    new_field_details['original_fieldset'] = schema_name
                    new_field_details['intermediate'] = True
                    # to handle multi-level self-nesting
                    if reuse_entry['at'] != schema_name:
                        destination_fields = field_group_at_path(reuse_entry['at'], fields)
                    else:
                        destination_fields = schema['fields']
                    destination_fields[nest_as] = {
                        'field_details': new_field_details,
                        # Make a new copy of the pristine copy
                        'fields': copy.deepcopy(reused_fields),
                    }
                    append_reused_here(schema, reuse_entry, fields[schema_name])


def ensure_valid_reuse(reused_schema, destination_schema=None):
    """Validate that schemas can participate in reuse operation.

    Root fieldsets (root=true) cannot be reused or have fields reused into them
    because their fields appear at document root level without a prefix.

    Args:
        reused_schema: Schema being reused (source)
        destination_schema: Schema receiving the reuse (destination), optional
                          for self-nesting validation

    Raises:
        ValueError: If reused_schema has root=true, or if destination_schema
                   (when provided) has root=true

    Rationale:
        Root fieldsets like 'base' have fields at document root (@timestamp,
        labels, tags). These can't be meaningfully reused elsewhere, and other
        fieldsets can't be reused into them without breaking the root contract.

    Example:
        >>> # Valid: user is not root, can be reused
        >>> ensure_valid_reuse(fields['user'], fields['destination'])

        >>> # Invalid: base is root
        >>> ensure_valid_reuse(fields['base'], fields['destination'])
        ValueError: Schema base has attribute root=true and cannot be reused
    """
    if reused_schema['schema_details']['root']:
        msg = "Schema {} has attribute root=true and therefore cannot be reused.".format(
            reused_schema['field_details']['name'])
        raise ValueError(msg)
    elif destination_schema and destination_schema['schema_details']['root']:
        msg = "Schema {} has attribute root=true and therefore cannot have other field sets reused inside it.".format(
            destination_schema['field_details']['name'])
        raise ValueError(msg)


def append_reused_here(reused_schema, reuse_entry, destination_schema):
    """Record metadata about what was reused into a destination schema.

    Maintains two tracking mechanisms:
    1. nestings: Legacy list of full paths (e.g., ['destination.user'])
    2. reused_here: Detailed array with descriptions and metadata

    Args:
        reused_schema: Source schema being reused
        reuse_entry: Reuse configuration dict with 'at', 'as', 'full', etc.
        destination_schema: Destination schema receiving the reuse

    Side Effects:
        Modifies destination_schema['schema_details'] in place:
        - Appends to 'nestings' array
        - Appends to 'reused_here' array

    reused_here Entry Structure:
        {
            'schema_name': 'user',  # Source schema
            'full': 'destination.user',  # Full path
            'short': '...',  # Description (from short_override or source)
            'normalize': [...],  # Optional normalization rules
            'beta': '...'  # Optional beta notice
        }

    Use Cases:
        - Documentation: Show what fieldsets are nested where
        - Validation: Verify expected reuse locations
        - Metadata: Track normalization and beta status at reuse location

    Note:
        Supports short_override for contextual descriptions at reuse location.
        Example: 'user' might have different short description when reused
        at 'destination.user' vs 'source.user'.
    """
    # Legacy, too limited
    destination_schema['schema_details'].setdefault('nestings', [])
    destination_schema['schema_details']['nestings'] = sorted(
        destination_schema['schema_details']['nestings'] + [reuse_entry['full']]
    )
    # New roomier way: we could eventually include contextual description here
    destination_schema['schema_details'].setdefault('reused_here', [])
    reused_here_entry = {
        'schema_name': reused_schema['field_details']['name'],
        'full': reuse_entry['full'],
        # Check for a short override, if not present, fall back to the top-level fieldset's short
        'short': reuse_entry['short_override'] if 'short_override' in reuse_entry else reused_schema['field_details']['short']
    }
    # If it exists, bring through the normalization
    if 'normalize' in reuse_entry:
        reused_here_entry['normalize'] = reuse_entry['normalize']
    # Check for beta attribute
    if 'beta' in reuse_entry:
        reused_here_entry['beta'] = reuse_entry['beta']
    destination_schema['schema_details']['reused_here'].extend([reused_here_entry])


def set_original_fieldset(fields, original_fieldset):
    """Recursively mark all fields with their source fieldset name.

    When fields are reused, they need to remember where they came from.
    This function stamps all fields in a field group with the original_fieldset
    attribute, using the visitor pattern.

    Args:
        fields: Field group dictionary (can be nested)
        original_fieldset: Name of source fieldset (e.g., 'user', 'process')

    Side Effects:
        Modifies all fields in place, adding 'original_fieldset' attribute

    Behavior:
        - Uses setdefault, so doesn't override if already set
        - Preserves nested original_fieldset (e.g., group fields in user)
        - Applied recursively to all nested fields

    Example:
        >>> # Copying 'user' fields to 'destination.user'
        >>> reused_fields = copy.deepcopy(fields['user']['fields'])
        >>> set_original_fieldset(reused_fields, 'user')
        # All fields now have original_fieldset='user'
        # destination.user.name shows it came from user

    Use Cases:
        - Documentation: Show which fields are reused vs native
        - OTel mapping: Reused fields may have different OTel mappings
        - Debugging: Track field provenance through reuse chain
    """
    def func(details):
        # Don't override if already set (e.g. 'group' for user.group.* fields)
        details['field_details'].setdefault('original_fieldset', original_fieldset)
    visitor.visit_fields(fields, field_func=func)


def field_group_at_path(dotted_path, fields):
    """Navigate to and return the fields dictionary at a dotted path.

    Traverses the nested field structure following a dotted path and returns
    the 'fields' dictionary at that location, creating it if necessary for
    object/group/nested types.

    Args:
        dotted_path: Dot-separated path string (e.g., 'destination.user')
        fields: Root fields dictionary to navigate from

    Returns:
        The 'fields' dictionary at the specified path

    Raises:
        ValueError: If path doesn't exist or non-nestable field is in the way

    Behavior:
        - Follows path components left to right
        - Creates 'fields' dict if needed for object/group/nested types
        - Fails if path goes through non-nestable field (keyword, long, etc.)

    Example:
        >>> # Get user fields under destination
        >>> user_fields = field_group_at_path('destination', fields)
        # Returns fields['destination']['fields']

        >>> # Navigate deeper
        >>> group_fields = field_group_at_path('destination.user', fields)
        # Returns fields['destination']['fields']['user']['fields']

    Use Cases:
        - Placing reused fieldsets at specific locations
        - Adding fields to nested structures during reuse
        - Validating paths exist before modification

    Note:
        Auto-creates 'fields' dict for object/group/nested types if missing.
        This supports incremental field addition during reuse.
    """
    path = dotted_path.split('.')
    nesting = fields
    for next_field in path:
        field = nesting.get(next_field, None)
        if not field:
            raise ValueError("Field {} not found, failed to find {}".format(dotted_path, next_field))
        nesting = field.get('fields', None)
        if not nesting:
            field_type = field['field_details']['type']
            if field_type in ['object', 'group', 'nested']:
                nesting = field['fields'] = {}
            else:
                raise ValueError("Field {} (type {}) already exists and cannot have nested fields".format(
                    dotted_path, field_type))
    return nesting


def calculate_final_values(fields):
    """Calculate final field names and properties after reuse is complete.

    Traverses all fields and computes path-based values that couldn't be
    calculated until after reuse was performed:
    - flat_name: Full dotted field name
    - dashed_name: Kebab-case version for use in URLs, filenames
    - multi-field flat_names: Names for alternate representations
    - OTel mappings for reused fields (from otel_reuse)

    Args:
        fields: Deeply nested field dictionary (after reuse)

    Side Effects:
        Modifies all field definitions in place, adding calculated properties

    Processing:
        Uses visitor pattern with path tracking to build full field names
        from the root down through all nesting levels.

    Example:
        Before: field name='name', path=['destination', 'user']
        After: flat_name='destination.user.name',
               dashed_name='destination-user-name'

    Note:
        Must be called AFTER perform_reuse() so all fields are in final
        locations before calculating names.
    """
    visitor.visit_fields_with_path(fields, field_finalizer)


def field_finalizer(details, path):
    """Calculate and set final field properties based on path.

    Callback function used by visitor during calculate_final_values traversal.
    Computes all path-dependent field properties.

    Args:
        details: Field entry dict with 'field_details'
        path: Array of field names from root to parent (e.g., ['destination', 'user'])

    Side Effects:
        Modifies details['field_details'] in place, adding:
        - flat_name: Full dotted name
        - dashed_name: Kebab-case name
        - multi_fields[].flat_name: Names for each multi-field
        - otel: Mappings (for reused fields with otel_reuse)

    Calculated Values:
        - flat_name: path + node_name joined by dots
          Example: ['destination', 'user'] + 'name' → 'destination.user.name'

        - dashed_name: flat_name with dots/underscores → dashes, @ removed
          Example: 'destination.user.name' → 'destination-user-name'
                   '@timestamp' → 'timestamp'

        - multi-field flat_names: parent flat_name + '.' + multi-field name
          Example: 'message.text' for text multi-field on message

    OTel Reuse Handling:
        - For reused fields: Checks otel_reuse for location-specific mappings
        - Removes base otel mapping (from original location)
        - Applies otel_reuse mapping if it matches the new flat_name
        - Cleans up otel_reuse attribute after processing

    Example:
        >>> # Field at path ['destination', 'user'] with node_name 'name'
        >>> field_finalizer(details, ['destination', 'user'])
        # details['field_details']['flat_name'] = 'destination.user.name'
        # details['field_details']['dashed_name'] = 'destination-user-name'
    """
    name_array = path + [details['field_details']['node_name']]
    flat_name = '.'.join(name_array)

    if 'original_fieldset' in details['field_details']:
        if 'otel' in details['field_details']:
            details['field_details'].pop('otel')

        if 'otel_reuse' in details['field_details']:
            otel_reuse = details['field_details']['otel_reuse']
            for r_mapping in otel_reuse:
                if 'ecs' in r_mapping and 'mapping' in r_mapping and r_mapping['ecs'] == flat_name:
                    details['field_details']['otel'] = [r_mapping['mapping']]

    if 'otel_reuse' in details['field_details']:
        details['field_details'].pop('otel_reuse')

    details['field_details']['flat_name'] = flat_name
    details['field_details']['dashed_name'] = re.sub('[_\.]', '-', flat_name).replace('@', '')
    if 'multi_fields' in details['field_details']:
        for mf in details['field_details']['multi_fields']:
            mf['flat_name'] = flat_name + '.' + mf['name']
