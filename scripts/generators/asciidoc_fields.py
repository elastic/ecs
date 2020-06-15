from os.path import join
from generators import ecs_helpers


def generate(nested, ecs_version, out_dir):
    save_asciidoc(join(out_dir, 'fields.asciidoc'), page_field_index(nested, ecs_version))
    save_asciidoc(join(out_dir, 'field-details.asciidoc'), page_field_details(nested))
    save_asciidoc(join(out_dir, 'field-values.asciidoc'), page_field_values(nested))

# Helpers


def save_asciidoc(file, text):
    with open(file, "w") as outfile:
        outfile.write(text)


# Rendering schemas

# Field Index


def page_field_index(nested, ecs_version):
    page_text = index_header(ecs_version)
    for fieldset in ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name']):
        page_text += render_field_index_row(fieldset)
    page_text += table_footer()
    page_text += index_footer()
    return page_text


def render_field_index_row(fieldset):
    return index_row().format(
        fieldset_id='ecs-' + fieldset['name'],
        fieldset_title=fieldset['title'],
        fieldset_short=fieldset.get('short', fieldset['description'])
    )


# Field Details Page

def page_field_details(nested):
    page_text = ''
    for fieldset in ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name']):
        page_text += render_fieldset(fieldset, nested)
    return page_text


def render_fieldset(fieldset, nested):
    text = field_details_table_header().format(
        fieldset_title=fieldset['title'],
        fieldset_name=fieldset['name'],
        fieldset_description=render_asciidoc_paragraphs(fieldset['description'])
    )

    text += render_fields(fieldset['fields'])

    text += table_footer()

    text += render_fieldset_reuse_section(fieldset, nested)

    return text


def render_fields(fields):
    text = ''
    for field_name, field in sorted(fields.items()):
        # Skip fields nested in this field set
        if 'original_fieldset' not in field:
            text += render_field_details_row(field)
    return text


def render_asciidoc_paragraphs(string):
    '''Simply double the \n'''
    return string.replace("\n", "\n\n")


def render_field_allowed_values(field):
    if not 'allowed_values' in field:
        return ''
    allowed_values = ', '.join(ecs_helpers.list_extract_keys(field['allowed_values'], 'name'))
    return field_acceptable_value_names().format(
        allowed_values=allowed_values,
        field_flat_name=field['flat_name'],
        field_dashed_name=field['dashed_name'],
    )


def render_field_details_row(field):
    example = ''
    if 'allowed_values' in field:
        example = render_field_allowed_values(field)
    elif 'example' in field:
        example = "example: `{}`".format(str(field['example']))

    field_type_with_mf = field['type']
    if 'multi_fields' in field:
        field_type_with_mf += "\n\nMulti-fields:\n\n"
        for mf in field['multi_fields']:
            field_type_with_mf += "* {} (type: {})\n\n".format(mf['flat_name'], mf['type'])

    field_normalization = ''
    if 'array' in field['normalize']:
        field_normalization = "\nNote: this field should contain an array of values.\n\n"

    text = field_details_row().format(
        field_flat_name=field['flat_name'],
        field_description=render_asciidoc_paragraphs(field['description']),
        field_example=example,
        field_normalization=field_normalization,
        field_level=field['level'],
        field_type=field_type_with_mf,
    )
    return text


def render_fieldset_reuse_section(fieldset, nested):
    '''Render the section on where field set can be nested, and which field sets can be nested here'''
    if not ('nestings' in fieldset or 'reusable' in fieldset):
        return ''

    text = field_reuse_section().format(
        reuse_of_fieldset=render_fieldset_reuses_text(fieldset)
    )
    if 'nestings' in fieldset:
        text += nestings_table_header().format(
            fieldset_name=fieldset['name'],
            fieldset_title=fieldset['title']
        )
        rows = []
        for reused_here_entry in fieldset['reused_here']:
            rows.append({
                'flat_nesting': "{}.*".format(reused_here_entry['full']),
                'name': reused_here_entry['schema_name'],
                'short': reused_here_entry['short']
            })
        for row in sorted(rows, key=lambda x: x['flat_nesting']):
            text += render_nesting_row(row)
        text += table_footer()
    return text


def render_fieldset_reuses_text(fieldset):
    '''Render where a given field set is expected to be reused'''
    if 'reusable' not in fieldset:
        return ''

    section_name = fieldset['name']
    sorted_fields = sorted(fieldset['reusable']['expected'], key=lambda k: k['full'])
    rendered_fields = map(lambda f: "`{}`".format(f['full']), sorted_fields)
    text = "The `{}` fields are expected to be nested at: {}.\n\n".format(
        section_name, ', '.join(rendered_fields))

    if 'top_level' in fieldset['reusable'] and fieldset['reusable']['top_level']:
        template = "Note also that the `{}` fields may be used directly at the root of the events.\n\n"
    else:
        template = "Note also that the `{}` fields are not expected to " + \
            "be used directly at the root of the events.\n\n"
    text += template.format(section_name)
    return text


def render_nesting_row(nesting):
    text = nestings_row().format(
        nesting_name=nesting['name'],
        flat_nesting=nesting['flat_nesting'],
        nesting_short=nesting['short'],
    )
    return text

# Templates


def table_footer():
    return '''
|=====
'''


# Field Index


def index_header(ecs_version):
    # Not using format() because then asciidoc {ecs}, {es}, etc are resolved.
    return '''
[[ecs-field-reference]]
== {ecs} Field Reference

This is the documentation of ECS version ''' + ecs_version + '''.

ECS defines multiple groups of related fields. They are called "field sets".
The <<ecs-base,Base>> field set is the only one whose fields are defined
at the root of the event.

All other field sets are defined as objects in {es}, under which
all fields are defined.

[float]
[[ecs-fieldsets]]
=== Field Sets
[cols="<,<",options="header",]
|=====
| Field Set  | Description
'''


def index_row():
    return '''
| <<{fieldset_id},{fieldset_title}>> | {fieldset_short}
'''


def index_footer():
    return '''
include::field-details.asciidoc[]
'''


# Field Details Page

# Main Fields Table


def field_details_table_header():
    return '''
[[ecs-{fieldset_name}]]
=== {fieldset_title} Fields

{fieldset_description}

==== {fieldset_title} Field Details

[options="header"]
|=====
| Field  | Description | Level

// ===============================================================
'''


def field_details_row():
    return '''
| {field_flat_name}
| {field_description}

type: {field_type}

{field_normalization}

{field_example}

| {field_level}

// ===============================================================
'''


def field_acceptable_value_names():
    return '''
*Important*: The field value must be one of the following:

{allowed_values}

To learn more about when to use which value, visit the page
<<ecs-allowed-values-{field_dashed_name},allowed values for {field_flat_name}>>
'''


# Field reuse

def field_reuse_section():
    return '''
==== Field Reuse

{reuse_of_fieldset}

'''


# Nestings table

def nestings_table_header():
    return '''
[[ecs-{fieldset_name}-nestings]]
===== Field sets that can be nested under {fieldset_title}

[options="header"]
|=====
| Nested fields | Description

// ===============================================================

'''


def nestings_row():
    return '''
| <<ecs-{nesting_name},{flat_nesting}>>
| {nesting_short}

// ===============================================================

'''


# Allowed values section


def page_field_values(nested):
    section_text = values_section_header()
    category_fields = ['event.kind', 'event.category', 'event.type', 'event.outcome']
    for cat_field in category_fields:
        section_text += render_field_values_page(nested['event']['fields'][cat_field])
    return section_text


def values_section_header():
    return '''
[[ecs-category-field-values-reference]]
== {ecs} Categorization Fields

WARNING: This section of ECS is in beta and is subject to change. These allowed values
are still under active development. Additional values will be published gradually,
and some of the values or relationships described here may change.
Users who want to provide feedback, or who want to have a look at
upcoming allowed values can visit this public feedback document
https://ela.st/ecs-categories-draft.

At a high level, ECS provides fields to classify events in two different ways:
"Where it's from" (e.g., `event.module`, `event.dataset`, `agent.type`, `observer.type`, etc.),
and "What it is." The categorization fields hold the "What it is" information,
independent of the source of the events.

ECS defines four categorization fields for this purpose, each of which falls under the `event.*` field set.

[float]
[[ecs-category-fields]]
=== Categorization Fields

* <<ecs-allowed-values-event-kind,event.kind>>
* <<ecs-allowed-values-event-category,event.category>>
* <<ecs-allowed-values-event-type,event.type>>
* <<ecs-allowed-values-event-outcome,event.outcome>>

NOTE: If your events don't match any of these categorization values, you should
leave the fields empty. This will ensure you can start populating the fields
once the appropriate categorization values are published, in a later release.
'''


def render_field_values_page(field):
    # Page heading
    heading = field_values_page_template().format(
        dashed_name=field['dashed_name'],
        flat_name=field['flat_name'],
        field_description=render_asciidoc_paragraphs(field['description']),
    )

    # Each allowed value
    body = ''
    toc = ''
    try:
        for value_details in field['allowed_values']:
            toc += "* <<ecs-{field_dashed_name}-{value_name},{value_name}>>\n".format(
                field_dashed_name=field['dashed_name'],
                value_name=value_details['name']
            )
            if 'expected_event_types' in value_details:
                additional_details = render_expected_event_types(value_details)
            else:
                additional_details = ''
            body += field_value_template().format(
                field_dashed_name=field['dashed_name'],
                value_name=value_details['name'],
                value_description=render_asciidoc_paragraphs(value_details['description']),
                additional_details=additional_details
            )
    except UnicodeEncodeError:
        print("Problem with field {}, field value:".format(field['flat_name']))
        print(value_details)
        raise
    return heading + toc + body


def render_expected_event_types(value_details):
    return expected_event_types_template().format(
        category_name=value_details['name'],
        expected_types=', '.join(value_details['expected_event_types']),
    )


def expected_event_types_template():
    return '''
*Expected event types for category {category_name}:*

{expected_types}
'''


def field_values_page_template():
    return '''
[[ecs-allowed-values-{dashed_name}]]
=== ECS Categorization Field: {flat_name}

{field_description}

WARNING: After the beta period for categorization, only the allowed categorization
values listed in the ECS repository and official ECS documentation should be considered
official. Use of any other values may result in incompatible implementations
that will require subsequent breaking changes.

*Allowed Values*

'''


def field_value_template():
    return '''
[float]
[[ecs-{field_dashed_name}-{value_name}]]
==== {value_name}

{value_description}

{additional_details}
'''
