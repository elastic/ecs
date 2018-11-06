import yaml
import os
import argparse
from helper import *
import os.path


def write_stdout():

    schema = get_schema()
    flat_schema = create_flat_schema(schema)

    links = ""
    for file in sorted(os.listdir("./use-cases")):

        output = ""

        if not file.endswith(".yml"):
            continue

        use_case = read_use_case_file("./use-cases/" + file)

        # Intentionally a relative link, to avoid leaving forked repo or branch
        schema_link = "use-cases/"
        # Link list to field prefixes
        links += " * [{}]({}{}.md)\n".format(use_case["title"], schema_link, use_case["name"])

        output += "## {} use case\n\n".format(use_case["title"])
        output += "{}\n\n".format(use_case["description"])

        fields = []
        for use_case_section in use_case["fields"]:
            # In case a description exists for a prefix, add it as field with .*
            if "description" in use_case_section and use_case_section["description"] != "":
                fields.append({
                    "name": use_case_section["name"] + ".&ast;",
                    "description": use_case_section["description"],
                    "type": "",
                    "level": "",
                    "example": "",
                    "ecs": False,
                })

            for section_fields in use_case_section["fields"]:
                # Complete ECS fields with ECS information if not set
                if section_fields["name"] in flat_schema:
                    section_fields["ecs"] = True
                    section_fields["type"] = flat_schema[section_fields["name"]]["type"]
                    section_fields["level"] = flat_schema[section_fields["name"]]["level"]
                    if section_fields["description"] == "":
                        section_fields["description"] = flat_schema[section_fields["name"]]["description"]
                    if section_fields["example"] == "":
                        section_fields["example"] = flat_schema[section_fields["name"]]["example"]
                else:
                    section_fields["ecs"] = False
                    section_fields["level"] = "(use case)"

                fields.append(section_fields)

        global_fields = {"name": use_case["name"], "title": use_case["title"], "description": "", "fields": fields}
        # Generate use cases with a relative link to access field definitions
        output += get_markdown_section(global_fields, "###", "../README.md") + "\n"

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

    # Outputs html of links to each use case (for the readme)
    # and generates an html file per use case besides their each yaml file.
    if args.stdout == "true":
        write_stdout()
