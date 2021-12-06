# Usage Docs

ECS fields can benefit from additional context and examples which describe their real-world usage. This directory provides a place in the documentation to capture these usage details. AsciiDoc markdown files can be added for any fieldset defined in ECS.

## Adding a Usage Doc

1. Create an AsciiDoc formatted file with the `.asciidoc` file extension.
2. Save the file in this directory (`docs/usage`), naming it after its associated field set (e.g. a usage document for the fields defined in `schemas/base.yml` fields would be named `docs/usage/base.asciidoc`).
3. The anchor at the top of the file (e.g. `[[ecs-base-usage]]`) must use the following convention for valid link references in the generated docs: `[[ecs-<<fieldset-name>>-usage]]`.
4. The title immediately following the anchor (e.g. `==== Base Fields Usage and Examples`) must use the following convention for formatting and naming Usage and Examples in the generated docs:
`==== <<fieldset-name>> Usage and Examples`.
5. Run `make`. The asciidoc generator will generate the ECS field reference, including the present usage docs.

If the filename doesn't match a currently defined fieldset, the usage document will not appear on the ECS docs site. This logic is handled in the AsciiDoc generator scripts, `scripts/generators/asciidoc_fields.py`.

## Template

The following is a simple AsciiDoc template as a starting point:

```asciidoc

[[ecs-fieldset-usage]]
==== Fieldset Fields Usage and Examples

Add relevant text here.

[discrete]
===== New Section header

Text for the new section.

[discrete]
===== Examples

[source,sh]
-----------
{
    "key": "value"
}
-----------

```
