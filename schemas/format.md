# Fields supported in schemas/*.yml

YAML with a twist: Flattened field names equivalent to nested. E.g. `foo.bar: value` and `foo:\n  bar: value`.

## Schema heading

- name (required): Name of the field set
- prefix (optional): Prefix under which the field set is nested. Defaults to the name of the field set. May be set to empty string.
- title (required): Rendered name of the field set (e.g. for documentation)
  Must be correctly capitalized
- group (required for now): TBD. Just set it to 2, for now ;-)
- description (required): Description of the field set
- type (required for now): at this level, should just be set to `group`
- fields (required): YAML array as described below

## Field set

Array of YAML objects:

```YAML
- name: version
  level: core
```

Supported keys to describe fields

- name (required): Name of the field
- level (required, one of: core, extended): ECS Level of maturity of the field
- type (required): Type of the field. Must be set explicitly, no default.
- required (TBD): TBD if still relevant.
- description (required): Description of the field
- example (optional): A single value example of what can be expected in this field
- multi\_fields ():
- reusable (optional):
