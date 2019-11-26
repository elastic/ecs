import csv
import sys


def generate(ecs_flat, version):
    sorted_fields = base_first(ecs_flat)
    save_csv('generated/csv/fields.csv', sorted_fields, version)


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

            schema_writer.writerow([
                version,
                str(field.get('index', True)).lower(),
                field_set,
                field['flat_name'],
                field['type'],
                field['level'],
                field.get('example', ''),
                field['short'],
            ])
