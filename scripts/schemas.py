import csv
import os
import yaml
import sys
import copy
from helper import *
import argparse


def create_csv(fields, file):

    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"

    # Create markdown schema output file
    with open(file, open_mode) as csvfile:
        schema_writer = csv.writer(csvfile,
                                   delimiter=',',
                                   quoting=csv.QUOTE_MINIMAL,
                                   lineterminator='\n')
        schema_writer.writerow(["Field", "Type", "Phase", "Example"])

        for namespace in fields:
            if len(namespace["fields"]) == 0:
                continue

            # Sort fields for easier readability
            namespaceFields = sorted(namespace["fields"],
                                     key=lambda field: field["name"])

            # Print fields into a table
            for field in namespaceFields:
                schema_writer.writerow([field["name"], field["type"], field["phase"], field["example"]])


def create_markdown(fields, file):
    # Create markdown schema output file
    output = open(file, 'w')

    for namespace in fields:
        if len(namespace["fields"]) == 0:
            continue
        output.write(get_markdown_table(namespace))

    output.close()


def create_markdown_string(fields):
    # Create markdown schema output string
    output = ""

    links = ""
    for namespace in fields:
        if len(namespace["fields"]) == 0:
            continue
        # Link list to field prefixes
        links += " * [{} fields](#{})\n".format(namespace["title"], namespace["name"])
        output += get_markdown_table(namespace)

    output = links + "\n" + output + "\n\n"
    return output


def filtered_fields(fields, groups):
    new_fields = copy.deepcopy(fields)
    for f in new_fields:
        n = 0
        for field in list(f["fields"]):
            if field["group"] not in groups:
                del f["fields"][n]
                continue
            n = n + 1

    return new_fields

def check_fields(fields):
    for f in fields:
        for field in list(f["fields"]):
            if field["level"] not in ["core", "extended"]:
                raise Exception('Field {} does not have an allowed level'.format(field["name"]))

if __name__ == "__main__":

    fields = get_schema()

    # Load all fields into object
    sortedNamespaces = sorted(fields, key=lambda field: field["group"])

    parser = argparse.ArgumentParser()
    parser.add_argument('--stdout', help='output to stdout instead of files')
    args = parser.parse_args()

    check_fields(sortedNamespaces)

    if args.stdout == "true":
        groups = [1, 2, 3]
        f_fields = filtered_fields(sortedNamespaces, groups)
        # Print to stdout
        print(create_markdown_string(f_fields))

    else:
        groups = [1, 2, 3]
        f_fields = filtered_fields(sortedNamespaces, groups)
        #create_markdown(f_fields, "schema.md")
        create_csv(f_fields, "schema.csv")
