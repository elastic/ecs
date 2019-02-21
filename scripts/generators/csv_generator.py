import csv
import sys


def base_first(ecs_flat):
    base_list = []
    sorted_list = []
    for field_name in sorted(ecs_flat):
        if '.' in field_name:
            sorted_list.append(ecs_flat[field_name])
        else:
            base_list.append(ecs_flat[field_name])
    return base_list + sorted_list


def generate(ecs_flat):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"

    sorted_fields = base_first(ecs_flat)

    with open('generated/csv/fields.csv', open_mode) as csvfile:
        schema_writer = csv.writer(csvfile,
                                   delimiter=',',
                                   quoting=csv.QUOTE_MINIMAL,
                                   lineterminator='\n')
        schema_writer.writerow(["Field", "Type", "Level", "Example"])
        for field in sorted_fields:
            schema_writer.writerow([field['flat_name'], field['type'], field['level'], field.get('example', '')])
