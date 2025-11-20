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

"""Markdown Documentation Generator.

This module generates comprehensive markdown documentation from ECS field schemas.
It produces human-readable reference documentation including:
- Field reference pages for each fieldset
- OTel alignment overview and detailed mappings
- Index pages and cross-references
- Usage documentation integration

The generator uses Jinja2 templates to render structured data into markdown format,
creating the official ECS documentation published on elastic.co.

Key Components:
    - generate(): Main entry point for documentation generation
    - page_*(): Template rendering functions for different page types
    - Helper functions: Field sorting, reuse tracking, allowed values extraction
    - Jinja2 integration: Template loading and rendering

Templates used (from scripts/templates/):
    - index.j2: Main index page
    - fieldset.j2: Individual fieldset documentation
    - ecs_field_reference.j2: Complete field reference
    - otel_alignment_details.j2: Detailed OTel mappings
    - otel_alignment_overview.j2: OTel alignment summary

See also: scripts/docs/markdown-generator.md for detailed documentation
"""

from functools import wraps
import os.path as path
import os

import jinja2

from generators import ecs_helpers
from copy import deepcopy


def generate(nested, docs_only_nested, ecs_generated_version, semconv_version, otel_generator, out_dir):
    """Generate all markdown documentation files from ECS schemas.

    This is the main entry point for markdown generation. It orchestrates the
    creation of all documentation pages including:
    - Main index page
    - OTel alignment overview and details
    - Complete field reference
    - Individual fieldset pages (one per ECS fieldset)

    Args:
        nested: Dictionary of nested fieldsets with field hierarchies
        docs_only_nested: Additional fields used only in documentation
        ecs_generated_version: ECS version string (e.g., '8.11.0' or '8.11.0+exp')
        semconv_version: OTel semantic conventions version (e.g., 'v1.24.0')
        otel_generator: OTelGenerator instance for alignment summaries
        out_dir: Output directory path for generated markdown files

    Generates files:
        - index.md: Main documentation index
        - ecs-otel-alignment-details.md: Detailed field-by-field mappings
        - ecs-otel-alignment-overview.md: Summary statistics
        - ecs-field-reference.md: Complete field reference
        - ecs-{fieldset}.md: One file per fieldset (e.g., ecs-http.md)

    Note:
        - Creates output directory if it doesn't exist
        - Strips leading 'v' from semconv_version for display
        - Uses Jinja2 templates from scripts/templates/

    Example:
        >>> from generators.otel import OTelGenerator
        >>> otel_gen = OTelGenerator('v1.24.0')
        >>> generate(nested, docs_only, '8.11.0', 'v1.24.0', otel_gen, 'docs/reference')
    """

    ecs_helpers.make_dirs(out_dir)

    if semconv_version.startswith('v'):
        semconv_version = semconv_version[1:]

    save_markdown(path.join(out_dir, 'index.md'), page_index(ecs_generated_version))
    save_markdown(path.join(out_dir, 'ecs-otel-alignment-details.md'),
                  page_otel_alignment_details(nested, ecs_generated_version, semconv_version))
    save_markdown(path.join(out_dir, 'ecs-otel-alignment-overview.md'),
                  page_otel_alignment_overview(otel_generator, nested, ecs_generated_version, semconv_version))
    fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])
    save_markdown(path.join(out_dir, 'ecs-field-reference.md'),
                  page_field_reference(ecs_generated_version, "Elasticsearch", fieldsets))
    for fieldset in fieldsets:
        save_markdown(path.join(out_dir, f'ecs-{fieldset["name"]}.md'),
                      page_fieldset(fieldset, nested, ecs_generated_version))

# Helpers


def render_fieldset_reuse_text(fieldset):
    """Extract and sort expected nesting locations for reusable fieldsets.

    When a fieldset is marked as reusable, this function extracts the list of
    locations where it's expected to be nested and sorts them alphabetically.
    Used in documentation to show where users can expect to find these fields.

    Args:
        fieldset: Fieldset dictionary potentially containing 'reusable' metadata

    Returns:
        Generator of sorted full field paths (e.g., ['client.as', 'destination.as']),
        or None if the fieldset is not reusable

    Example:
        >>> fieldset = {'reusable': {'expected': [
        ...     {'full': 'destination.geo'}, {'full': 'client.geo'}
        ... ]}}
        >>> list(render_fieldset_reuse_text(fieldset))
        ['client.geo', 'destination.geo']
    """
    if not fieldset.get('reusable'):
        return None
    reusable_fields = fieldset['reusable']['expected']
    sorted_fields = sorted(reusable_fields, key=lambda k: k['full'])
    return map(lambda f: f['full'], sorted_fields)


def render_nestings_reuse_section(fieldset):
    """Build reuse section data showing which fieldsets are nested here.

    Creates a list of metadata about other fieldsets that are reused (nested)
    within this fieldset. Each entry includes the nesting path, schema name,
    description, and any special properties like beta status or normalization.

    Args:
        fieldset: Target fieldset dictionary potentially containing 'reused_here' list

    Returns:
        List of dictionaries sorted by nesting path, each containing:
        - flat_nesting: The nesting path with wildcard (e.g., 'client.geo.*')
        - name: Schema name of the reused fieldset
        - short: Short description
        - beta: Beta status marker (if applicable)
        - normalize: Normalization rules (if applicable)

        Returns None if no fieldsets are reused here.

    Example:
        >>> fieldset = {'reused_here': [
        ...     {'full': 'client.geo', 'schema_name': 'geo', 'short': 'Location'}
        ... ]}
        >>> render_nestings_reuse_section(fieldset)
        [{'flat_nesting': 'client.geo.*', 'name': 'geo', 'short': 'Location', ...}]
    """
    if not fieldset.get('reused_here'):
        return None
    rows = []
    for reused_here_entry in fieldset['reused_here']:
        rows.append({
            'flat_nesting': "{}.*".format(reused_here_entry['full']),
            'name': reused_here_entry['schema_name'],
            'short': reused_here_entry['short'],
            'beta': reused_here_entry.get('beta', ''),
            'normalize': reused_here_entry.get('normalize')
        })

    return sorted(rows, key=lambda x: x['flat_nesting'])


def extract_allowed_values_key_names(field):
    """Extract names of all allowed values for a field.

    For fields with constrained value sets (like enumerations), this extracts
    the name of each allowed value for display in documentation.

    Args:
        field: Field dictionary potentially containing 'allowed_values' list

    Returns:
        List of allowed value names, or empty list if no allowed values defined

    Example:
        >>> field = {'allowed_values': [
        ...     {'name': 'success', 'description': 'Success'},
        ...     {'name': 'failure', 'description': 'Failure'}
        ... ]}
        >>> extract_allowed_values_key_names(field)
        ['success', 'failure']
    """
    if not field.get('allowed_values'):
        return []
    return ecs_helpers.list_extract_keys(field['allowed_values'], 'name')


def sort_fields(fieldset):
    """Prepare and sort fieldset fields for template rendering.

    Converts the fieldset's fields dictionary into a sorted list and enriches
    each field with extracted allowed value names. This prepares the data
    structure for consumption by Jinja2 templates.

    Args:
        fieldset: Fieldset dictionary containing 'fields' dictionary

    Returns:
        List of field dictionaries sorted alphabetically by name, each enriched
        with 'allowed_value_names' property

    Note:
        Modifies field objects in place by adding 'allowed_value_names' key.
        Fields are sorted by their 'name' property for consistent output.

    Example:
        >>> fieldset = {'fields': {
        ...     'status': {'name': 'status', 'allowed_values': [...]},
        ...     'method': {'name': 'method'}
        ... }}
        >>> sorted_fields = sort_fields(fieldset)
        >>> [f['name'] for f in sorted_fields]
        ['method', 'status']
    """
    fields_list = list(fieldset['fields'].values())
    for field in fields_list:
        field['allowed_value_names'] = extract_allowed_values_key_names(field)
    return sorted(fields_list, key=lambda field: field['name'])


def check_for_usage_doc(fieldset_name, usage_file_list=ecs_helpers.usage_doc_files()):
    """Check if a usage documentation file exists for a fieldset.

    Usage docs provide additional guidance and examples for using specific
    fieldsets. This function checks if such a document has been created.

    Args:
        fieldset_name: Name of the fieldset (e.g., 'http', 'user')
        usage_file_list: List of available usage doc filenames (defaults to
                        scanning docs/fields/usage/ directory)

    Returns:
        True if a usage doc exists, False otherwise

    Note:
        Usage docs follow the naming pattern: ecs-{fieldset_name}-usage.md
        They are typically stored in docs/fields/usage/

    Example:
        >>> check_for_usage_doc('http')
        True  # If docs/fields/usage/ecs-http-usage.md exists
    """
    return f"ecs-{fieldset_name}-usage.md" in usage_file_list


def templated(template_name):
    """Decorator to automatically render a function's return value through a Jinja2 template.

    This decorator simplifies page generation by allowing functions to return
    context dictionaries that are automatically rendered through specified templates.

    Args:
        template_name: Name of the Jinja2 template file (e.g., 'fieldset.j2')

    Returns:
        Decorator function that wraps the target function

    Behavior:
        - If decorated function returns a dict: Passes it as template context
        - If function returns None: Uses empty dict as context
        - If function returns non-dict: Returns value unchanged (bypass rendering)

    Example:
        >>> @templated('index.j2')
        ... def page_index(version):
        ...     return {'version': version}
        >>>
        >>> # Calling page_index('8.11.0') automatically renders index.j2
        >>> # with {'version': '8.11.0'} as context
    """
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            ctx = func(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def render_template(template_name, **context):
    """Render a Jinja2 template with the provided context.

    Loads a template from the configured template directory and renders it
    with the given variables.

    Args:
        template_name: Name of the template file (e.g., 'fieldset.j2')
        **context: Keyword arguments passed as template variables

    Returns:
        Rendered template as a string

    Raises:
        jinja2.TemplateNotFound: If the template file doesn't exist

    Note:
        Templates are loaded from scripts/templates/ directory.
        The template_env is configured with keep_trailing_newline=True
        and trim_blocks=True for consistent formatting.

    Example:
        >>> render_template('index.j2', version='8.11.0', title='ECS Reference')
        '# ECS Reference\\n\\nVersion: 8.11.0\\n...'
    """
    template = template_env.get_template(template_name)
    return template.render(**context)


def save_markdown(f, text):
    """Save rendered markdown text to a file.

    Creates parent directories if needed and writes the markdown content.

    Args:
        f: Full file path where markdown should be saved
        text: Rendered markdown content to write

    Note:
        Creates any missing parent directories automatically.
        Overwrites existing files without warning.

    Example:
        >>> save_markdown('docs/reference/ecs-http.md', markdown_content)
    """
    os.makedirs(path.dirname(f), exist_ok=True)
    with open(f, "w") as outfile:
        outfile.write(text)

# jinja2 setup


local_dir = path.dirname(path.abspath(__file__))
TEMPLATE_DIR = path.join(local_dir, '../templates')
template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
template_env = jinja2.Environment(loader=template_loader,
                                  keep_trailing_newline=True,
                                  trim_blocks=True,
                                  lstrip_blocks=False)

# Rendering schemas

# Index


@templated('index.j2')
def page_index(ecs_generated_version):
    """Generate the main documentation index page.

    Creates the landing page for ECS documentation with version information
    and links to other documentation pages.

    Args:
        ecs_generated_version: ECS version string (e.g., '8.11.0')

    Returns:
        Rendered markdown content for index.md

    Template: index.j2
    """
    return dict(ecs_generated_version=ecs_generated_version)


# Field Index


@templated('fieldset.j2')
def page_fieldset(fieldset, nested, ecs_generated_version):
    """Generate documentation page for a single fieldset.

    Creates comprehensive documentation for one ECS fieldset including:
    - Fieldset description and metadata
    - List of all fields with types and descriptions
    - Reuse information (where this fieldset is used)
    - Nesting information (what fieldsets are nested here)
    - Link to usage documentation if available

    Args:
        fieldset: Fieldset dictionary containing name, fields, and metadata
        nested: Complete nested fieldsets structure (for context)
        ecs_generated_version: ECS version string

    Returns:
        Rendered markdown content for ecs-{fieldset_name}.md

    Template: fieldset.j2

    Example:
        >>> page_fieldset(nested['http'], nested, '8.11.0')
        # Returns markdown for ecs-http.md
    """
    sorted_reuse_fields = render_fieldset_reuse_text(fieldset)
    render_nestings_reuse_fields = render_nestings_reuse_section(fieldset)
    sorted_fields = sort_fields(fieldset)
    usage_doc = check_for_usage_doc(fieldset.get('name'))
    return dict(fieldset=fieldset,
                sorted_reuse_fields=sorted_reuse_fields,
                render_nestings_reuse_section=render_nestings_reuse_fields,
                sorted_fields=sorted_fields,
                usage_doc=usage_doc)

# Field Reference Page


@templated('ecs_field_reference.j2')
def page_field_reference(ecs_generated_version, es, fieldsets):
    """Generate the complete ECS field reference page.

    Creates a comprehensive reference listing all ECS fieldsets and their fields
    in a single document. This serves as a complete field catalog.

    Args:
        ecs_generated_version: ECS version string
        es: Elasticsearch product name (typically "Elasticsearch")
        fieldsets: List of all fieldsets sorted by group and name

    Returns:
        Rendered markdown content for ecs-field-reference.md

    Template: ecs_field_reference.j2

    Note:
        This page can be quite large as it includes all fields from all fieldsets.
    """
    return dict(ecs_generated_version=ecs_generated_version,
                es=es,
                fieldsets=fieldsets)


# Field Details Page


def page_field_details(nested, docs_only_nested):
    """Generate combined field details for all fieldsets.

    Creates a consolidated view of all fieldsets with detailed information.
    Merges documentation-only fields into the main nested structure.

    Args:
        nested: Dictionary of nested fieldsets
        docs_only_nested: Additional fields only used in documentation

    Returns:
        Concatenated markdown content for all fieldsets

    Note:
        This function modifies the nested dictionary in place by merging
        docs_only_nested fields. Currently not used in main generation flow.
    """
    if docs_only_nested:
        for fieldset_name, fieldset in docs_only_nested.items():
            nested[fieldset_name]['fields'].update(fieldset['fields'])
    fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])
    results = (generate_field_details_page(fieldset) for fieldset in fieldsets)
    return ''.join(results)


@templated('field_details.j2')
def generate_field_details_page(fieldset):
    """Generate detailed documentation for a single fieldset.

    Helper function for page_field_details that renders one fieldset
    with complete information including reuse and nesting details.

    Args:
        fieldset: Fieldset dictionary to document

    Returns:
        Rendered markdown content for this fieldset's details

    Template: field_details.j2
    """
    # render field reuse text section
    sorted_reuse_fields = render_fieldset_reuse_text(fieldset)
    render_nestings_reuse_fields = render_nestings_reuse_section(fieldset)
    sorted_fields = sort_fields(fieldset)
    usage_doc = check_for_usage_doc(fieldset.get('name'))
    return dict(fieldset=fieldset,
                sorted_reuse_fields=sorted_reuse_fields,
                render_nestings_reuse_section=render_nestings_reuse_fields,
                sorted_fields=sorted_fields,
                usage_doc=usage_doc)

# OTel Fields Mapping Page


@templated('otel_alignment_details.j2')
def page_otel_alignment_details(nested, ecs_generated_version, semconv_version):
    """Generate detailed OTel alignment documentation showing field-by-field mappings.

    Creates comprehensive documentation showing how each ECS field maps to
    OpenTelemetry Semantic Conventions. Only includes fieldsets that have
    at least one OTel mapping defined.

    Args:
        nested: Dictionary of nested fieldsets
        ecs_generated_version: ECS version string
        semconv_version: OTel semantic conventions version (without 'v' prefix)

    Returns:
        Rendered markdown content for ecs-otel-alignment-details.md

    Template: otel_alignment_details.j2

    Note:
        - Filters out fieldsets with no OTel mappings
        - Deep copies fieldsets to avoid modifying original data
        - Converts fields dict to sorted list for template iteration

    Example output includes:
        - Relation types (match, equivalent, related, etc.)
        - Attribute/metric names
        - Stability levels
        - Explanatory notes
    """
    fieldsets = [deepcopy(fieldset) for fieldset in ecs_helpers.dict_sorted_by_keys(
        nested, ['group', 'name']) if is_eligable_for_otel_mapping(fieldset)]
    for fieldset in fieldsets:
        sorted_fields = sort_fields(fieldset)
        fieldset['fields'] = sorted_fields

    return dict(fieldsets=fieldsets,
                semconv_version=semconv_version,
                ecs_generated_version=ecs_generated_version)


def is_eligable_for_otel_mapping(fieldset):
    """Check if a fieldset has any OTel mappings defined.

    Determines whether a fieldset should be included in OTel alignment
    documentation by checking if any of its fields have OTel mappings.

    Args:
        fieldset: Fieldset dictionary containing 'fields'

    Returns:
        True if at least one field has an 'otel' mapping, False otherwise

    Example:
        >>> fieldset = {'fields': {
        ...     'method': {'otel': [{'relation': 'match'}]},
        ...     'version': {}
        ... }}
        >>> is_eligable_for_otel_mapping(fieldset)
        True
    """
    for field in fieldset['fields'].values():
        if 'otel' in field:
            return True
    return False

# OTel Mapping Summary Page


@templated('otel_alignment_overview.j2')
def page_otel_alignment_overview(otel_generator, nested, ecs_generated_version, semconv_version):
    """Generate OTel alignment overview with summary statistics.

    Creates high-level documentation showing alignment statistics between
    ECS and OpenTelemetry Semantic Conventions. Provides counts of:
    - Total fields in each namespace
    - Number of matching, equivalent, related fields
    - Conflicting and not-applicable fields
    - Coverage percentages

    Args:
        otel_generator: OTelGenerator instance for computing summaries
        nested: Dictionary of nested fieldsets
        ecs_generated_version: ECS version string
        semconv_version: OTel semantic conventions version (without 'v' prefix)

    Returns:
        Rendered markdown content for ecs-otel-alignment-overview.md

    Template: otel_alignment_overview.j2

    Note:
        Uses the OTelGenerator to compute alignment statistics.
        Includes both ECS namespaces and OTel-only namespaces.

    Example output includes tables with:
        - Namespace names
        - Field counts by relation type
        - Coverage percentages
    """
    fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])
    summaries = otel_generator.get_mapping_summaries(fieldsets)
    return dict(summaries=summaries,
                semconv_version=semconv_version,
                ecs_generated_version=ecs_generated_version)

# Allowed values section


@templated('field_values.j2')
def page_field_values(nested, template_name='field_values_template.j2'):
    """Generate documentation for categorization fields with allowed values.

    Creates specialized documentation for key event categorization fields
    that have constrained value sets. Focuses on the core event taxonomy
    fields used for event classification.

    Args:
        nested: Dictionary of nested fieldsets
        template_name: Template to use (default: 'field_values_template.j2')
                      Note: Currently not used, hardcoded to 'field_values.j2'

    Returns:
        Rendered markdown content showing allowed values for categorization fields

    Template: field_values.j2

    Fields documented:
        - event.kind: High-level event category
        - event.category: Event category for filtering
        - event.type: Sub-category for event
        - event.outcome: Event outcome (success, failure, unknown)

    Note:
        Currently only processes fields from the 'event' fieldset.
        The template_name parameter is accepted but not used.
    """
    category_fields = ['event.kind', 'event.category', 'event.type', 'event.outcome']
    nested_fields = []
    for cat_field in category_fields:
        nested_fields.append(nested['event']['fields'][cat_field])

    return dict(fields=nested_fields)
