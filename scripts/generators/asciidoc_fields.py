from functools import wraps
import os.path as path

import jinja2

from generators import ecs_helpers


def generate(nested, ecs_version, out_dir):
    save_asciidoc(path.join(out_dir, 'fields.asciidoc'), page_field_index(nested, ecs_version))
    save_asciidoc(path.join(out_dir, 'field-details.asciidoc'), page_field_details(nested))
    save_asciidoc(path.join(out_dir, 'field-values.asciidoc'), page_field_values(nested))

# Helpers


def render_fieldset_reuse_text(fields):
    """Renders the expected nesting locations.

    :param fields: The reusable, expected fields
    """
    sorted_fields = sorted(fields, key=lambda k: k['full'])
    return map(lambda f: f['full'], sorted_fields)


def render_nestings_reuse_section(fieldset):
    rows = []
    for reused_here_entry in fieldset['reused_here']:
        rows.append({
            'flat_nesting': "{}.*".format(reused_here_entry['full']),
            'name': reused_here_entry['schema_name'],
            'short': reused_here_entry['short']
        })

    return sorted(rows, key=lambda x: x['flat_nesting'])


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
        outfile.write(text)

# jinja2 setup


TEMPLATE_DIR = path.join(path.dirname(path.abspath(__file__)), '../templates')
template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
template_env = jinja2.Environment(loader=template_loader)
template_env.filters.update({
    'list_extract_keys': ecs_helpers.list_extract_keys,
    'render_fieldset_reuse_text': render_fieldset_reuse_text,
    'render_nestings_reuse_section': render_nestings_reuse_section})

# Rendering schemas

# Field Index


@templated('fields_template.j2')
def page_field_index(nested, ecs_version):
    fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])
    return dict(ecs_version=ecs_version, fieldsets=fieldsets)


# Field Details Page

@templated('field_details.j2')
def page_field_details(nested):
    fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])
    return dict(fieldsets=fieldsets)


# Allowed values section

@templated('field_values_template.j2')
def page_field_values(nested, template_name='field_values_template.j2'):
    category_fields = ['event.kind', 'event.category', 'event.type', 'event.outcome']
    nested_fields = []
    for cat_field in category_fields:
        nested_fields.append(nested['event']['fields'][cat_field])

    return dict(fields=nested_fields)
