import os
import yaml
import sys
import copy
from helper import *
import argparse


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
