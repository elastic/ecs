import csv
import sys

def generate(ecs_fields):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"

    with open('generated/csv/fields.csv', open_mode) as csvfile:
        schema_writer = csv.writer(csvfile,
                                   delimiter=',',
                                   quoting=csv.QUOTE_MINIMAL,
                                   lineterminator='\n')
        schema_writer.writerow(["Field", "Type", "Level", "Example"])
        for field_name in sorted(ecs_fields):
            field = ecs_fields[field_name]
            schema_writer.writerow([field_name, field["type"], field["level"], field.get('example', '')])
