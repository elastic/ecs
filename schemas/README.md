# Fields supported in schemas/\*.yml

YAML with a twist: Flattened field names equivalent to nested. E.g. `foo.bar: value` and `foo:\n  bar: value`.

Note that we use the wording "schema" and "field set" alternatively to mean the same concept:
a group of related fields.

## Field set heading

Required field set attributes:

- name: Name of the field set, lowercased and with underscores to separate words.
  For programmatic use.
- title: Capitalized name of the field set, with spaces to separate words.
  For use in documentation section titles.
- description: Description of the field set. Two subsequent newlines create a new paragraph.
- fields: YAML array as described in the "List of fields" section below.

Optional field set attributes:

- short: Short version of the description to display in small spaces, such as the list of field sets.
  Short descriptions must not have newlines.
  Defaults to the main description when absent.
  If the main description has multiple paragraphs, then a 'short' description
  with no newlines is required.
- root (default false): Whether or not the fields of this field set should be namespaced under the field set name.
  Most field sets are expected to have their fields namespaced under the field set name.
  Only the "base" field set is expected to set this to true (to define a few root fields like `@timestamp`).
- group (default 2): To sort field sets against one another.
  For example the "base" field set has group=1 and is the first listed in the documentation.
  All others have group=2 and are therefore after "base" (sorted alphabetically).
- type (ignored): at this level, should always be `group`
- reusable (optional): Used to identify which field sets are expected to be reused in multiple places.
  See "Field set reuse" for details.
- beta: Adds a beta marker for the entire fieldset. The text provided in this attribute is used as content of the beta marker in the documentation.
  Beta notices should not have newlines.

### Field set reuse

Unless otherwise noted via the `reusable` attribute, a field set is a group of
fields that will be defined at the root of the events.
As an example, the fields of the `event` field set are nested like: `{"event": {"id": "foo"}}`.

Field set reuse lets us define a group of fields that's expected to be used in
multiple places, like for example `geo`, which can appear under `source`, `destination` and other places:

```JSON
{
  "source": { "ip": "10.10.10.10", "geo": { "country_name": "..." } },
  "destination": { "ip": "10.42.42.42", "geo": { "country_name": "..." } }
}
```

The `reusable` attribute is composed of `top_level` and `expected` sub-attributes:

- top\_level (optional, default true): Is this field set expected at the root of
  events or is it only expected in the nested locations?
- expected (default []): list of places the field set's fields are expected.
  There are two valid notations to list expected locations.

The "flat" (or dotted) notation to represent where the fields are nested:

```YAML
  reusable:
    top_level: false
    expected:
      - network
      - network.inner
```

The above would nest field set `vlan` at `network.vlan.*` and `network.inner.vlan.*`:

```JSON
{
  "network": {
    "vlan": { },
    "inner": {
      "vlan": {}
    }
  }
}
```

In some cases we need to nest a field set within itself, as a different name,
which can be thought of loosely as a "role".
A good example is nesting `process` at `process.parent`, to capture the parent of a process.
In these cases, we replace the "flat" key name with a small object with keys `at` and `as`:

```
  reusable:
    top_level: true
    expected:
      - { at: process, as: parent }
```

The above defines all process fields in both places:

```JSON
{
  "process": {
    "pid": 4242,
    "parent": {
      "pid": 1
    }
  }
}
```

The `beta` marker can optionally be used along with `at` and `as` to include a beta marker in the field reuses section, marking specific reuse locations as beta.
Beta notices should not have newlines.

```
  reusable:
    top_level: true
    expected:
    - at: user
      as: target
      beta: Reusing these fields in this location is currently considered beta.
```

### List of fields

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
- description (required): Description of the field
- short (optional): Short version of the description to display in small spaces.
  Short descriptions must not have newlines.
  Defaults to the main description when absent.
  If the main description has multiple paragraphs, then a 'short' description
  with no newlines is required.
- example (optional): A single value example of what can be expected in this field.
  Example values that are composite types (array, object) should be quoted to avoid YAML interpretation
  in ECS-generated artifacts and other downstream projects depending on the schema.
- multi\_fields (optional): Specify additional ways to index the field.
- index (optional): If `False`, means field is not indexed (overrides type). This parameter has no effect
  on a `wildcard` field.
- format: Field format that can be used in a Kibana index template.
- normalize: Normalization steps that should be applied at ingestion time. Supported values:
  - array: the content of the field should be an array (even when there's only one value).
- beta (optional): Adds a beta marker for the field to the description. The text provided in this attribute is used as content of the beta marker in the documentation. Note that when a whole field set is marked as beta, it is not necessary nor recommended to mark all fields in the field set as beta. Beta notices should not have newlines.

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

Supported keys when using the [alias field type](https://www.elastic.co/guide/en/elasticsearch/reference/current/alias.html)

```YAML
    - name: a_field
      level: extended
      type: alias
      path: another_field
      description: >
        An alias of another field.
```
- path (optional): The full path to the [aliases' target field](https://www.elastic.co/guide/en/elasticsearch/reference/current/alias.html#alias-targets).

#### Multi\_fields

- type (required): type of the multi\_fields
- name (optional): defaults to multi\_fields type

## Minimal example

```YAML
- name: my_fields
  title: My fields
  description: My awesome fields.
  fields:

    - name: a_field
      level: extended
      type: keyword
      example: 42
      description: >
        A description

        with multiple paragraphs

        requires you to provide a 'short' description as well.
      short: A short version of the description.

    - name: another_field
      level: extended
      type: keyword
      multi_fields:
      - type: text
        name: text
      example: I am Groot
      description: A short description that doesn't require an explicit 'short'.
```
