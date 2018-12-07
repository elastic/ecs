import yaml
import glob


def read_schema_file(path):
    """Read a schema.yml file and cleans up the fields
    """
    fields = []
    with open(path) as f:
        fields = yaml.load(f.read())

    clean_namespace_fields(fields)
    return fields


def read_use_case_file(path):
    """Read a use-case.yml file and cleans up the fields
    """
    with open(path) as f:
        use_case = yaml.load(f.read())

    fields = use_case["fields"]
    clean_namespace_fields(fields)
    use_case["fields"] = fields
    return use_case


def clean_namespace_fields(fields):
    """Cleans up all fields to set defaults
    """
    for namespace in fields:

        # For now set the default group to 2
        if "group" not in namespace:
            namespace["group"] = 2

        prefix = ""
        # Prefix if not base namespace
        if namespace["name"] != "base":
            prefix = namespace["name"]

        clean_fields(namespace["fields"], prefix, namespace["group"])


def clean_fields(fields, prefix, group):
    for field in fields:
        clean_string_field(field, "description")
        clean_string_field(field, "footnote")
        clean_string_field(field, "example")
        clean_string_field(field, "type")

        # Add prefix if needed
        if prefix != "":
            field["name"] = prefix + "." + field["name"]

        if 'level' not in field.keys():
            field["level"] = '(use case)'

        if 'group' not in field.keys():
            # If no group set, set parent group
            field["group"] = group

        if "multi_fields" in field:
            for f in field["multi_fields"]:
                clean_string_field(f, "description")
                clean_string_field(f, "example")
                clean_string_field(f, "type")

                # multi fields always have a prefix
                f["name"] = field["name"] + "." + f["name"]

                if 'group' not in f.keys():
                    # If no group set, set parent group
                    f["group"] = group


def clean_string_field(field, key):
    """Cleans a string field and creates an empty string for the field in case it does not exist
    """
    if key in field.keys():
        # Remove all spaces and newlines from beginning and end
        field[key] = str(field[key]).strip()
    else:
        field[key] = ""

    if "index" in field and field["index"] == False:
        field["type"] = "(not indexed)"


def get_markdown_row(field, link, multi_field):
    """Creates a markdown table for the given fields
    """

    # Replace newlines with HTML representation as otherwise newlines don't work in Markdown
    description = field["description"].replace("\n", "<br/>")

    show_name = field["name"]

    ecs = True
    if 'ecs' in field.keys():
        ecs = field["ecs"]

    # non ecs fields are in italic
    if not ecs:
        show_name = "*" + field["name"] + "*"
        description = "*" + description + "*"

    example = ""
    if field["example"] != "":
        # Add ticks around examples to not break table
        example = "`{}`".format(field["example"])

    # If link is true, it link to the anchor is provided. This is used for the use-cases
    if link and ecs:
        return '| [{}]({}#{})  | {} | {} | {} | {} |\n'.format(show_name, link, field["name"], description, field["level"], field["type"], example)

    # By default a anchor is attached to the name
    return '| <a name="{}"></a>{} | {} | {} | {} | {} |\n'.format(field["name"], show_name, description, field["level"], field["type"], example)


def get_schema():
    fields = []
    for file in sorted(glob.glob("schemas/*.yml")):
        fields = fields + read_schema_file(file)
    return fields


def get_markdown_section(namespace, title_prefix="##", link=False):
    section_name = namespace["name"]

    # Title
    output = '{} <a name="{}"></a> {} fields\n\n'.format(title_prefix, section_name, namespace["title"])

    # Description
    # Replaces one newlines with two as otherwise double newlines do not show up in markdown
    output += namespace["description"].replace("\n", "\n\n") + "\n"

    # Reusable object details
    if "reusable" in namespace and "expected" in namespace["reusable"]:
        sorted_fields = sorted(namespace["reusable"]["expected"])
        rendered_fields = map(lambda f: "`{}.{}`".format(f, section_name), sorted_fields)
        output += "The `{}` fields are expected to be nested at: {}.\n\n".format(
            section_name, ', '.join(rendered_fields))

        if "top_level" in namespace["reusable"] and namespace["reusable"]["top_level"]:
            template = "Note also that the `{}` fields may be used directly at the top level.\n\n"
        else:
            template = "Note also that the `{}` fields are not expected to " + \
                "be used directly at the top level.\n\n"
        output += template.format(section_name)

    # Table
    titles = ["Field", "Description", "Level", "Type", "Example"]

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

    # Footnote
    if "footnote" in namespace:
        output += namespace["footnote"].replace("\n", "\n\n") + "\n"

    return output
