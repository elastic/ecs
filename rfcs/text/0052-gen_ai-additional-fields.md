# 0052: Additional fields for Generative AI
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (candidate)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

Following up on [RFC 0050](https://github.com/elastic/ecs/pull/2475) which introduced an initial batch of `gen_ai` fields, this RFC (0052) adds more fields due to user feedback. The fields are backported from [OTel](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/).

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

Field | Type | Description /Usage
-- | -- | --
gen_ai.system_instructions | flattened | The system message or instructions provided to the GenAI model separately from the chat history.
gen_ai.input.messages | flattened | The chat history provided to the model as an input.
gen_ai.output.messages | flattened | Messages returned by the model where each message represents a specific model response (choice, candidate).
gen_ai.tool.definitions | flattened | (Part of invoke_agent span) The list of source system tool definitions available to the GenAI agent or model.
gen_ai.tool.call.arguments | flattened | (Part of OTel execute_tool span) Parameters passed to the tool call.
gen_ai.tool.call.result | flattened | (Part of OTel execute_tool span) The result returned by the tool call (if any and if execution was successful).

Changes based on OTel https://github.com/open-telemetry/semantic-conventions/pull/2179/files

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

Example usage:

```json
{
    "gen_ai": {
        "system_instructions": {
            [
                {
                    "type": "text",
                    "content": "You are a assistant for frequent travelers."
                },
                {
                    "type": "text",
                    "content": "Your mission is to assist travelers with their queries about locations around the world."
                }
            ]
        },
        "input": {
            "messages": {
                [
                    {
                        "role": "user",
                        "parts": [
                        {
                            "type": "text",
                            "content": "Weather in Paris?"
                        }
                        ]
                    },
                    {
                        "role": "assistant",
                        "parts": [
                        {
                            "type": "tool_call",
                            "id": "call_VSPygqKTWdrhaFErNvMV18Yl",
                            "name": "get_weather",
                            "arguments": {
                            "location": "Paris"
                            }
                        }
                        ]
                    },
                    {
                        "role": "tool",
                        "parts": [
                        {
                            "type": "tool_call_response",
                            "id": " call_VSPygqKTWdrhaFErNvMV18Yl",
                            "result": "rainy, 57°F"
                        }
                        ]
                    }
                ]
            }
        },
        "output" :{
            "messages": {
                [
                    {
                        "role": "assistant",
                        "parts": [
                        {
                            "type": "text",
                            "content": "The weather in Paris is currently rainy with a temperature of 57°F."
                        }
                        ],
                        "finish_reason": "stop"
                    }
                ]
            },
        }
    }
}
```


<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

In OTel, many field types are set to `any` and are typically JSON objects. [Example](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/)

In ECS, should we use something like [flattened](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/flattened) type.

**Resolution:** All six fields in this RFC use `flattened`. The decision was driven by three constraints:

1. OTel Collector ES exporter

> Nested fields are not supported under passthrough namespaces like attributes.* are in the OTel ES schema.
So defining gen_ai.input.messages, gen_ai.output.messages and gen_ai.tool.definitions as nested would not be compatible with OTel ingest.
> Complex attributes types are currently always mapped to flattened in the OTel Collector ES exporter.
> -- @AlexanderWert

See [comment](https://github.com/elastic/ecs/pull/2532#issuecomment-3479329267).

2. Serverless limitation for nested fields on indices

> "The default setting for limiting nested fields on indices (index.mapping.nested_fields.limit) is 50. If customers try to create a new index with a higher limit, they will receive the following error: Settings [index.mapping.nested_fields.limit,index.mapping.nested_objects.limit] are not available when running in serverless mode. It's a serverless limitation that can't be overridden without Elastic support involved."
> -- @Mikaayenson

See [comment](https://github.com/elastic/ecs/pull/2532#issuecomment-3415953216)

3. ES|QL queryability

At the time this RFC was drafted, neither `nested` nor `flattened` were supported in ES|QL. As of March 2026, the picture has changed significantly:

- **`flattened`:** Active development under way. [elasticsearch#144245](https://github.com/elastic/elasticsearch/pull/144245) enables ES|QL to load `flattened` fields as JSON strings, queryable via `JSON_EXTRACT`. [elasticsearch#144451](https://github.com/elastic/elasticsearch/pull/144451) "Allow specific keys within a flattened field to be mapped as typed sub-fields (keyword, ip, etc.) via a new "properties" mapping attribute."
   
`flattened` is therefore the only path to ES|QL queryability in the foreseeable future.

Tradeoffs:

> "With flattened, it would not be possible to query for something like 'system role has a text like helpful bot', [...] the association between the `role` field and the `parts.content` field is lost."
> — @flash1293

See [comment](https://github.com/elastic/ecs/pull/2532#issuecomment-3380468096)


> "We will likely lean on `_source` to access nested dicts in an order preserving fashion."
> — @joe-desimone

See [comment](https://github.com/elastic/ecs/pull/2532#issuecomment-3470660966)

This trade-off is accepted given the OTel compatibility requirement. As of March 2026, ES|QL `flattened` support is actively in development ([elasticsearch#144245](https://github.com/elastic/elasticsearch/pull/144245)), to be passed into the new JSON_EXTRACT function, making `flattened` the only viable path to ES|QL queryability in the foreseeable future.

## People

The following are the people that consulted on the contents of this RFC.

* @susan-shu-c | author
* @Mikaayenson, @joe-desimone | Security subject matter experts

<!--
Who will be or has been consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

<!-- Insert any links appropriate to this RFC in this section. -->

* https://opentelemetry.io/blog/2024/otel-generative-ai/
* https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/
* https://github.com/open-telemetry/semantic-conventions/commits/main/docs/gen-ai/gen-ai-events.md
* https://github.com/open-telemetry/semantic-conventions/pull/2702
* https://www.elastic.co/docs/reference/ecs/ecs-gen_ai#_gen_ai_field_details
* https://github.com/open-telemetry/semantic-conventions/pull/2179/

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/2519
* Stage 1: https://github.com/elastic/ecs/pull/2525
* Stage 2: https://github.com/elastic/ecs/pull/2532
