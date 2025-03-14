---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-principles-design.html
applies_to:
  stack: all
  serverless: all
---

# Design principles [ecs-principles-design]

The considerations here form the basis of ECS design. These principles help guide making the appropriate decisions for the project.


## A common schema [_a_common_schema]

A goal of ECS is to maximize interoperability and reuse. When expanding the concepts represented in ECS, consider how broad or narrow the intended use cases are.

Defining fields with narrow, lacking, or incorrect definitions limit future use. The best practice is to add the fewest fields to adequately capture an event. Adding more fields in the future is less complicated than changing or removing established ones.

Also, avoid adding fields because a concept exists. For example, a network protocol specification may contain many features, but some are obscure and used infrequently. Finally, avoid standardization for standardization’s sake.


## Field sets are namespaces [_field_sets_are_namespaces]

Field sets create independent schema sections for understanding a concept in isolation.

Complex concepts may be better captured using nesting. A field set may contain several sub-components that make up a larger concept: `dns.question.class`, `dns.question.answer`, `dns.question.type`.


## Naming consistency [_naming_consistency]

Consistent naming across the schema makes learning and memorizing field names easier. Do not limit terms with broad meaning to a single case.

Examples:

* Many concepts can include a `.name` or `.id` value (for example, `event.id`, `error.id`, `group.id`, `rule.id`, `user.id`).
* Several potential IP addresses in a single event (`source.ip`, `destination.ip`, `host.ip`).


## Reuse [_reuse]

Introducing extra fields may seem necessary when adding or expanding a concept. But, try to use an existing field or reuse an existing field set to avoid duplicating fields. Leveraging consistent fields across event sources helps build more straightforward queries and visualizations.

For example, imagine an app or framework produces a unique ID for each log it emits. Instead of adding a custom `.id` field specific to that app, consider the `event.id` field.

Reusing fields simplifies capturing several entities of a type within a single event. One example, the `user.*` field set and the reuse `user.target.*` allow collecting the same detail about the acting and target users. Redefining the entire `user.*` field set is unnecessary. In limited use, consider an array of field set reuses if multiples of the same reuse need capturing.


## Custom fields are a feature [_custom_fields_are_a_feature]

Many situations will need custom fields to fully capture the event contents. Users and integrations are encouraged to add custom fields to capture concepts not defined in ECS. Custom fields give users the flexibility to add fields for their internal use cases, less common concepts, and experimentation.

Following the [best practices](/reference/ecs-custom-fields-in-ecs.md), users and integrations can create a path for future migration if a similar concept appears in ECS.

