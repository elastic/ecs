import yaml


def read_schema_file(path):
    """Read a schema.yml file and cleans up the fields
    """
    fields = []
    with open(path) as f:
        fields = yaml.load(f.read())

    clean_fields(fields)
    return fields


def read_use_case_file(path):
    """Read a use-case.yml file and cleans up the fields
    """
    with open(path) as f:
        use_case = yaml.load(f.read())

    fields = use_case["fields"]
    clean_fields(fields)
    use_case["fields"] = fields
    return use_case


def clean_fields(fields):
    """Cleans up all fields to set defaults
    """
    for namespace in fields:

        # For now set the default group to 2
        if "group" not in namespace:
            namespace["group"] = 2

        for field in namespace["fields"]:
            clean_string_field(field, "description")
            clean_string_field(field, "example")
            clean_string_field(field, "type")

            # Prefix if not base namespace
            if namespace["name"] != "base":
                field["name"] = namespace["name"] + "." + field["name"]

            if 'phase' not in field.keys():
                field["phase"] = 0

            if 'group' not in field.keys():
                # If no group set, set parent group
                field["group"] = namespace["group"]

            if "multi_fields" in field:
                for f in field["multi_fields"]:
                    clean_string_field(f, "description")
                    clean_string_field(f, "example")
                    clean_string_field(f, "type")

                    # Prefix if not base namespace
                    if namespace["name"] != "base":
                        f["name"] = field["name"] + "." + f["name"]

                    if 'phase' not in f.keys():
                        f["phase"] = 0

                    if 'group' not in f.keys():
                        # If no group set, set parent group
                        f["group"] = namespace["group"]


def clean_string_field(field, key):
    """Cleans a string field and creates an empty string for the field in case it does not exist
    """
    if key in field.keys():
        # Remove all spaces and newlines from beginning and end
        field[key] = str(field[key]).strip()
    else:
        field[key] = ""


def get_markdown_row(field, link, multi_field):
    """Creates a markdown table for the given fields
    """

    # Replace newlines with HTML representation as otherwise newlines don't work in Markdown
    description = field["description"].replace("\n", "<br/>")

    # Verified and accepted fields are bold
    verified = False
    if 'verified' in field.keys() and field["verified"]:
        field["name"] = "**" + field["name"] + "**"

    example = ""
    if field["example"] != "":
        # Add ticks around examples to not break table
        example = "`{}`".format(field["example"])

    if multi_field:
        multi_field = "1"
    else:
        multi_field = ""

    # If link is true, it link to the anchor is provided. This is used for the use-cases
    if link:
        return '| [`{}`]({}#{})  | {}  | {}  | {}  | {}  |\n'.format(field["name"], link, field["name"], description, field["type"], multi_field, example)

    # By default a anchor is attached to the name
    return '| <a name="{}"></a>`{}`  | {}  | {}  | {}  | {}  |\n'.format(field["name"], field["name"], description, field["type"], multi_field, example)


def get_markdown_table(namespace, title_prefix="##", link=False):

    output = '{} <a name="{}"></a> {} fields\n\n'.format(title_prefix, namespace["name"], namespace["title"])

    # Replaces one newlines with two as otherwise double newlines do not show up in markdown
    output += namespace["description"].replace("\n", "\n\n") + "\n"

    titles = ["Field", "Description", "Type", "Multi Field", "Example"]

    for title in titles:
        output += "| {}  ".format(title)
    output += "|\n"

    for title in titles:
        output += "|---"
    output += "|\n"

    # Sort fields for easier readability
    namespaceFields = sorted(namespace["fields"], key=lambda field: field["name"])

    # Print fields into a table
    for field in namespace["fields"]:
        output += get_markdown_row(field, link, False)
        if "multi_fields" in field:
            for f in field["multi_fields"]:
                output += get_markdown_row(f, link, True)

    output += "\n\n"

    return output
