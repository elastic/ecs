import os
import yaml
import sys
import copy
from helper import *
import argparse
from functools import reduce
import json


def addNamespace(namespaces, namespace):
    namespaces[namespace["name"]] = {
        "name": namespace["name"],
        "title": namespace["title"],
        "description": namespace["description"],
        "type": namespace["type"],
        "group": namespace["group"],
        "fields": {}
    }

    return namespaces


def addFields(namespaces, namespace):
    namespaceName = namespace["name"]

    def fieldAsJson(fieldsByName, field):
        fieldsByName[field["name"]] = {
            "name": field["name"],
            "type": field["type"],
            "required": field.get("required", False),
            "description": field["description"],
            "example": field["example"],
            "group": field["group"],
            "level": field["level"],
            "footnote": field["footnote"],
        }

        return fieldsByName

    namespaces[namespaceName]["fields"] = reduce(fieldAsJson, namespace["fields"], {})
    return namespaces


def create_json(fields, file):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"

    # Output schema to json
    with open(file, open_mode) as jsonfile:
        root = reduce(addNamespace, fields, {})
        schema = reduce(addFields, fields, root)

        jsonfile.write(json.dumps(schema, indent=2, sort_keys=True))


def create_markdown_document(fields):
    # Create markdown schema output string
    tables = ""

    links = ""
    for namespace in fields:
        if len(namespace["fields"]) == 0:
            continue
        # Links to each namespace / top level object
        links += " * [{} fields](#{})\n".format(namespace["title"], namespace["name"])
        tables += get_markdown_section(namespace)

    return links + "\n" + tables + "\n\n"


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

    # Generates Markdown for README
    if args.stdout == "true":
        groups = [1, 2, 3]
        f_fields = filtered_fields(sortedNamespaces, groups)
        # Print to stdout
        print(create_markdown_document(f_fields))

    # Generates schema.csv
    else:
        groups = [1, 2, 3]
        f_fields = filtered_fields(sortedNamespaces, groups)
        create_json(f_fields, "schema.json")
