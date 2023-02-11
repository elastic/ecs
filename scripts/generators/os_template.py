from typing import (
    Dict,
)

from os.path import join

from _types import (
    Field,
)
from generators import ecs_helpers
from generators.es_template import dict_add_nested, entry_for, mapping_settings, save_json, template_settings


OPENSEARCH_REMAP = {
    'constant_keyword': 'keyword',
    'wildcard': 'keyword',
    'flattened': 'object',
    'version': 'keyword',
}


def generate(
    ecs_flat: Dict[str, Field],
    ecs_version: str,
    out_dir: str,
    mapping_settings_file: str,
    template_settings_file: str
) -> None:
    """Generate the opensearch index template"""
    field_mappings = {}
    for flat_name in sorted(ecs_flat):
        field = ecs_flat[flat_name]
        opensearch_remap_field_type(field)

        name_parts = flat_name.split('.')
        dict_add_nested(field_mappings, name_parts, entry_for(field))

    mappings_section: Dict = mapping_settings(mapping_settings_file)
    mappings_section['properties'] = field_mappings

    generate_legacy_template_version(ecs_version, mappings_section, out_dir, template_settings_file)


def generate_legacy_template_version(
    ecs_version: str,
    mappings_section: Dict,
    out_dir: str,
    template_settings_file: str
) -> None:
    ecs_helpers.make_dirs(join(out_dir, 'opensearch'))
    template: Dict = template_settings(ecs_version, mappings_section, template_settings_file, is_legacy=True)

    filename: str = join(out_dir, "opensearch/template.json")
    save_json(filename, template)


def opensearch_remap_field_type(
    field: Dict
) -> None:
    if field['type'] in OPENSEARCH_REMAP:
        typ = field['type']
        field['type'] = OPENSEARCH_REMAP[typ]