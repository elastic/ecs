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

Generates markdown docs using Jinja2 templates from scripts/templates/:
- index.md, ecs-field-reference.md, ecs-{fieldset}.md per fieldset
- ecs-otel-alignment-details.md and ecs-otel-alignment-overview.md
"""

from functools import wraps
import os.path as path
import os

import jinja2

from generators import ecs_helpers
from copy import deepcopy


def generate(nested, docs_only_nested, ecs_generated_version, semconv_version, otel_generator, out_dir):
    """Generate all markdown docs: index, field reference, per-fieldset pages, and OTel alignment pages."""

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
    """Return sorted list of full reuse paths for reusable fieldsets, or None if not reusable."""
    if not fieldset.get('reusable'):
        return None
    reusable_fields = fieldset['reusable']['expected']
    sorted_fields = sorted(reusable_fields, key=lambda k: k['full'])
    return map(lambda f: f['full'], sorted_fields)


def render_nestings_reuse_section(fieldset):
    """Return sorted list of reused_here entries with flat_nesting (path.*), or None."""
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
    """Return list of allowed value names for a field, or [] if none."""
    if not field.get('allowed_values'):
        return []
    return ecs_helpers.list_extract_keys(field['allowed_values'], 'name')


def sort_fields(fieldset):
    """Return fieldset fields as a list sorted by name, with allowed_value_names added to each field."""
    fields_list = list(fieldset['fields'].values())
    for field in fields_list:
        field['allowed_value_names'] = extract_allowed_values_key_names(field)
    return sorted(fields_list, key=lambda field: field['name'])


def check_for_usage_doc(fieldset_name, usage_file_list=ecs_helpers.usage_doc_files()):
    """Return True if ecs-{fieldset_name}-usage.md exists in the usage docs directory."""
    return f"ecs-{fieldset_name}-usage.md" in usage_file_list


def templated(template_name):
    """Decorator that renders the function's dict return value through the named Jinja2 template."""
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
    """Render a Jinja2 template from scripts/templates/ with the given context."""
    template = template_env.get_template(template_name)
    return template.render(**context)


def save_markdown(f, text):
    """Write markdown text to file, creating parent directories as needed."""
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
    """Render index.md."""
    return dict(ecs_generated_version=ecs_generated_version)


# Field Index


@templated('fieldset.j2')
def page_fieldset(fieldset, nested, ecs_generated_version):
    """Render ecs-{fieldset.name}.md with fields, reuse, and nesting sections."""
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
    """Render ecs-field-reference.md with all fieldsets."""
    return dict(ecs_generated_version=ecs_generated_version,
                es=es,
                fieldsets=fieldsets)


# Field Details Page


def page_field_details(nested, docs_only_nested):
    """Return concatenated field_details.j2 output for all fieldsets. Merges docs_only_nested in place."""
    if docs_only_nested:
        for fieldset_name, fieldset in docs_only_nested.items():
            nested[fieldset_name]['fields'].update(fieldset['fields'])
    fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])
    results = (generate_field_details_page(fieldset) for fieldset in fieldsets)
    return ''.join(results)


@templated('field_details.j2')
def generate_field_details_page(fieldset):
    """Render field_details.j2 for one fieldset."""
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
    """Render ecs-otel-alignment-details.md for fieldsets with at least one otel mapping."""
    fieldsets = [deepcopy(fieldset) for fieldset in ecs_helpers.dict_sorted_by_keys(
        nested, ['group', 'name']) if is_eligable_for_otel_mapping(fieldset)]
    for fieldset in fieldsets:
        sorted_fields = sort_fields(fieldset)
        fieldset['fields'] = sorted_fields

    return dict(fieldsets=fieldsets,
                semconv_version=semconv_version,
                ecs_generated_version=ecs_generated_version)


def is_eligable_for_otel_mapping(fieldset):
    """Return True if any field in fieldset has an 'otel' mapping."""
    for field in fieldset['fields'].values():
        if 'otel' in field:
            return True
    return False

# OTel Mapping Summary Page


@templated('otel_alignment_overview.j2')
def page_otel_alignment_overview(otel_generator, nested, ecs_generated_version, semconv_version):
    """Render ecs-otel-alignment-overview.md with mapping summaries from otel_generator."""
    fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])
    summaries = otel_generator.get_mapping_summaries(fieldsets)
    return dict(summaries=summaries,
                semconv_version=semconv_version,
                ecs_generated_version=ecs_generated_version)

# Allowed values section


@templated('field_values.j2')
def page_field_values(nested, template_name='field_values_template.j2'):
    """Render allowed-values docs for event.kind, event.category, event.type, event.outcome."""
    category_fields = ['event.kind', 'event.category', 'event.type', 'event.outcome']
    nested_fields = []
    for cat_field in category_fields:
        nested_fields.append(nested['event']['fields'][cat_field])

    return dict(fields=nested_fields)
