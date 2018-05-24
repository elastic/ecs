# <a name="implementing-ecs"></a>Implementing ECS

## Adhere to ECS

The following rules apply if an event wants to adhere to ECS

* The document MUST have the `@timestamp` field.
* The [data type](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/mapping-types.html) defined for an ECS field MUST be used.
* It SHOULD have the field `event.version` to define which version of ECS it uses.

To make the most out of ECS as many fields as possible should be mapped to ECS.

## Rules

ECS follows the following writing and naming rules for the fields. The goal of
these rules is to make the fields easy to remember and have a guide when new
fields are added.

Often events will contain additional fields besides ECS. These can follow the
the same naming and writing rules but don't have to.

**Writing**

* All fields must be lower case
* No special characters except `_`
* Words are combined through underscore

**Naming**

* Use present tense unless field describes historical information.
* Use singular and plural names properly to reflect the field content. For example, use `requests_per_sec` rather than `request_per_sec`.
* Organise the prefixes from general to specific to allow grouping fields into objects with a prefix like `host.*`.
* Avoid stuttering of words. If part of the field name is already in the prefix, do not repeat it. Example: `host.host_ip` should be `host.ip`.
* Fields must be prefixed except for the base fields. For example all `host` fields are prefixed with `host.`. See `dot` notation in FAQ for more details.
* Do not use abbreviations (few exceptions like `ip` exist)
