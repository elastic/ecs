from functools import wraps
import os.path as path

import jinja2

from generators import ecs_helpers


def generate(nested, ecs_generated_version, out_dir):
    save_asciidoc(path.join(out_dir, 'index.asciidoc'), page_index(ecs_generated_version))
    save_asciidoc(path.join(out_dir, 'fields.asciidoc'), page_field_index(nested, ecs_generated_version))
    save_asciidoc(path.join(out_dir, 'field-details.asciidoc'), page_field_details(nested))
    save_asciidoc(path.join(out_dir, 'field-values.asciidoc'), page_field_values(nested))

# Helpers


def render_fieldset_reuse_text(fieldset):
    """Renders the expected nesting locations
       if the the `reusable` object is present.

    :param fieldset: The fieldset to evaluate
    """
    if not fieldset.get('reusable'):
        return None
    reusable_fields = fieldset['reusable']['expected']
    sorted_fields = sorted(reusable_fields, key=lambda k: k['full'])
    return map(lambda f: f['full'], sorted_fields)


def render_nestings_reuse_section(fieldset):
    """Renders the reuse section entries.

    :param fieldset: The target fieldset
    """
    if not fieldset.get('reused_here'):
        return None
    rows = []
    for reused_here_entry in fieldset['reused_here']:
        rows.append({
            'flat_nesting': "{}.*".format(reused_here_entry['full']),
            'name': reused_here_entry['schema_name'],
            'short': reused_here_entry['short'],
            'beta': reused_here_entry.get('beta', '')
        })

    return sorted(rows, key=lambda x: x['flat_nesting'])


def extract_allowed_values_key_names(field):
    """Extracts the `name` keys from the field's
       allowed_values if present in the field
       object.

    :param field: The target field
    """
    if not field.get('allowed_values'):
        return []
    return ecs_helpers.list_extract_keys(field['allowed_values'], 'name')


def sort_fields(fieldset):
    """Prepares a fieldset's fields for being
    passed into the j2 template for rendering. This
    includes sorting them into a list of objects and
    adding a field for the names of any allowed values
    for the field, if present.

    :param fieldset: The target fieldset
    """
    fields_list = list(fieldset['fields'].values())
    for field in fields_list:
        field['allowed_value_names'] = extract_allowed_values_key_names(field)
    return sorted(fields_list, key=lambda field: field['name'])


def check_for_usage_doc(fieldset_name, usage_file_list=ecs_helpers.usage_doc_files()):
    """Checks if a usage doc exists for the specified
       fieldset.

    :param fieldset_name: The name of the target fieldset
    """
    return f"{fieldset_name}.asciidoc" in usage_file_list


def templated(template_name):
    """Decorator function to simplify rendering a template.

    :param template_name: the name of the template to be rendered
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
    """Renders a template from the template folder with the given
    context.

    :param template_name: the name of the template to be rendered
    :param context: the variables that should be available in the
                    context of the template.
    """
    template = template_env.get_template(template_name)
    return template.render(**context)


def save_asciidoc(f, text):
    with open(f, "w") as outfile:
        print(text.strip(), file=outfile)

# jinja2 setup


TEMPLATE_DIR = path.join(path.dirname(path.abspath(__file__)), '../templates')
template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
template_env = jinja2.Environment(loader=template_loader)

# Rendering schemas

# Index


@templated('index.j2')
def page_index(ecs_generated_version):
    return dict(ecs_generated_version=ecs_generated_version)


# Field Index


@templated('fields.j2')
def page_field_index(nested, ecs_generated_version):
    fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])
    return dict(ecs_generated_version=ecs_generated_version, fieldsets=fieldsets)


# Field Details Page

def page_field_details(nested):
    fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])
    results = (generate_field_details_page(fieldset) for fieldset in fieldsets)
    return ''.join(results)


@templated('field_details.j2')
def generate_field_details_page(fieldset):
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


# Allowed values section

@templated('field_values.j2')
def page_field_values(nested, template_name='field_values_template.j2'):
    category_fields = ['event.kind', 'event.category', 'event.type', 'event.outcome']
    nested_fields = []
    for cat_field in category_fields:
        nested_fields.append(nested['event']['fields'][cat_field])

    return dict(fields=nested_fields)
