# Fields supported in schemas/\*.yml

YAML with a twist: Flattened field names equivalent to nested. E.g. `foo.bar: value` and `foo:\n  bar: value`.

## Schema heading

- name (required): Name of the field set
- root (optional, default false): Whether or not the fields of this field set should be nested under the field set name.
- title (required): Rendered name of the field set (e.g. for documentation)
  Must be correctly capitalized
- group (required for now): TBD. Just set it to 2, for now ;-)
- description (required): Description of the field set
- fields (required): YAML array as described below
- type (ignored): at this level, should always be `group`

## Field set

Array of YAML objects:

```YAML
- name: version
  level: core
  type: keyword
```

Supported keys to describe fields

- name (required): Name of the field
- level (required, one of: core, extended): ECS Level of maturity of the field
- type (required): Type of the field. Must be set explicitly, no default.
- required (TBD): TBD if still relevant.
- short (optional): Optional shorter definition, for display in tight spaces
- description (required): Description of the field
- example (optional): A single value example of what can be expected in this field
- multi\_fields (optional):
- reusable (optional):
- index (optional): If `False`, means field is not indexed (overrides type)

### Multi\_fields

- type (required): type of the multi\_fields
- name (optional): defaults to multi\_fields type
