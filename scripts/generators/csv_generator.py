import csv
import sys
import os
from generator import ecs_helpers


def generate(ecs_flat, version, out_dir):
    ecs_helpers.make_dirs(os.path.join(out_dir, 'csv'))
    sorted_fields = base_first(ecs_flat)
    save_csv(os.path.join(out_dir, 'csv/fields.csv'), sorted_fields, version)


def base_first(ecs_flat):
    base_list = []
    sorted_list = []
    for field_name in sorted(ecs_flat):
        if '.' in field_name:
            sorted_list.append(ecs_flat[field_name])
        else:
            base_list.append(ecs_flat[field_name])
    return base_list + sorted_list


def save_csv(file, sorted_fields, version):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"

    with open(file, open_mode) as csvfile:
        schema_writer = csv.writer(csvfile,
                                   delimiter=',',
                                   quoting=csv.QUOTE_MINIMAL,
                                   lineterminator='\n')

        schema_writer.writerow(["ECS_Version", "Indexed", "Field_Set", "Field",
                                "Type", "Level", "Example", "Description"])
        for field in sorted_fields:
            key_parts = field['flat_name'].split('.')
            if len(key_parts) == 1:
                field_set = 'base'
            else:
                field_set = key_parts[0]

            indexed = str(field.get('index', True)).lower()
            schema_writer.writerow([
                version,
                indexed,
                field_set,
                field['flat_name'],
                field['type'],
                field['level'],
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
                        field.get('example', ''),
                        field['short'],
                    ])
