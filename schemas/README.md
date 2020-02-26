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
- reusable (optional): YAML object composed of top_level and expected sub properties

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
- short (optional): Optional shorter definition, for display in tight spaces.
  Derived automatically if description is short enough.
- description (required): Description of the field
- example (optional): A single value example of what can be expected in this field
- multi\_fields (optional): Specify additional ways to index the field.
- index (optional): If `False`, means field is not indexed (overrides type)
- format: Field format that can be used in a Kibana index template.
- normalize: Normalization steps that should be applied at ingestion time. Supported values:
  - array: the content of the field should be an array (even when there's only one value).

Supported keys to describe expected values for a field

```YAML
  accepted_values:
  - name: authentication
    description: ...
  - name: process
    description: ...
    expected_event_types:
      - start
      - iamgroot
```

- accepted\_values: list of dictionaries with the 'name' and 'description' of the expected values.
  Optionally, entries in this list can specify 'expected\_event\_types'.
- expected\_event\_types: list of expected "event.type" values to use in association
  with that category.

### Multi\_fields

- type (required): type of the multi\_fields
- name (optional): defaults to multi\_fields type
