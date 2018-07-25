import yaml
import os
import argparse
from helper import *
import os.path


def write_stdout():

    link_prefix = "https://github.com/elastic/ecs"
    schema = get_schema()
    flat_schema = create_flat_schema(schema)

    links = ""
    for file in sorted(os.listdir("./use-cases")):

        output = ""

        if not file.endswith(".yml"):
            continue

        use_case = read_use_case_file("./use-cases/" + file)

        schema_link = "https://github.com/elastic/ecs/blob/master/use-cases/"
        # Link list to field prefixes
        links += " * [{}]({}{}.md)\n".format(use_case["title"], schema_link, use_case["name"])

        output += "## {} use case\n\n".format(use_case["title"])
        output += "{}\n\n".format(use_case["description"])

        fields = []
        for f in use_case["fields"]:
            # In case a description exists for a prefix, add is as field with .*
            if "description" in f and f["description"] != "":
                fields.append({
                    "name": f["name"] + ".*",
                    "description": f["description"],
                    "type": "",
                    "phase": "",
                    "example": "",
                })

            for f2 in f["fields"]:
                f2["ecs"] = f2["name"] in flat_schema
                fields.append(f2)

        global_fields = {"name": use_case["name"], "title": use_case["title"], "description": "", "fields": fields}
        output += get_markdown_table(global_fields, "###", link_prefix) + "\n"

        # Write output to /use-cases/use_case["name"].md file
        # Adjust links

        with open("./use-cases/" + use_case["name"] + ".md", "w") as f:
            f.write(output)

    print("\n" + links + "\n\n")


def create_flat_schema(schema):
    fields = {}

    for namespace in schema:
        if len(namespace["fields"]) == 0:
            continue

        for f in namespace["fields"]:
            fields[f["name"]] = f

    return fields


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--stdout', help='output to stdout instead of files')
    args = parser.parse_args()

    if args.stdout == "true":
        write_stdout()
