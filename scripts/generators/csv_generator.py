import _csv
import csv
import sys
from typing import Dict, List
from os.path import join
from _types import Field
from generator import ecs_helpers


def generate(ecs_flat: Dict[str, Field], version: str, out_dir: str) -> None:
    ecs_helpers.make_dirs(join(out_dir, 'csv'))
    sorted_fields = base_first(ecs_flat)
    save_csv(join(out_dir, 'csv/fields.csv'), sorted_fields, version)


def base_first(ecs_flat: Dict[str, Field]) -> List[Field]:
    base_list: List[Field] = []
    sorted_list: List[Field] = []

    for field_name in sorted(ecs_flat):
        if '.' in field_name:
            sorted_list.append(ecs_flat[field_name])
        else:
            base_list.append(ecs_flat[field_name])

    return base_list + sorted_list


def save_csv(file: str, sorted_fields: List[Field], version: str) -> None:
    open_mode = "w"

    with open(file, open_mode) as csvfile:
        schema_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        schema_writer.writerow(["ECS_Version", "Indexed", "Field_Set", "Field",
                                "Type", "Level", "Normalization", "Example", "Description"])

        for field in sorted_fields:
            key_parts = field['flat_name'].split('.')
            field_set = 'base' if len(key_parts) == 1 else key_parts[0]
            indexed = str(field.get('index', True)).lower()

            schema_writer.writerow([
                version,
                indexed,
                field_set,
                field['flat_name'],
                field['type'],
                field['level'],
                ', '.join(field['normalize']),
                field.get('example', ''),
                field['short'],
            ])

            if 'multi_fields' in field:
                for mf in field['multi_fields']:
                    schema_writer.writerow([
                        version,
                        indexed,
                        field_set,
                        mf['flat_name'],
                        mf['type'],
                        field['level'],
                        '',
                        field.get('example', ''),
                        field['short'],
                    ])
