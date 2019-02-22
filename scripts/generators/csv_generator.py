import csv
import sys


def generate(ecs_flat):
    sorted_fields = base_first(ecs_flat)
    save_csv('generated/csv/fields.csv', sorted_fields)


def base_first(ecs_flat):
    base_list = []
    sorted_list = []
    for field_name in sorted(ecs_flat):
        if '.' in field_name:
            sorted_list.append(ecs_flat[field_name])
        else:
            base_list.append(ecs_flat[field_name])
    return base_list + sorted_list


def save_csv(file, data):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"

    schema_writer = csv.writer(csvfile,
                               delimiter=',',
                               quoting=csv.QUOTE_MINIMAL,
                               lineterminator='\n')

    with open(file, open_mode) as csvfile:
        schema_writer.writerow(["Field", "Type", "Level", "Example"])
        for field in sorted_fields:
            schema_writer.writerow([
                field['flat_name'],
                field['type'],
                field['level'],
                field.get('example', '')
            ])
