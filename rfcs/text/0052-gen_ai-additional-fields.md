# 0052: Additional fields for Generative AI

- Stage: **Proposal** <!-- Do not change. -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. -->
- Target maturity: **beta** <!-- Select one. See https://github.com/elastic/ecs/blob/main/docs/reference/ecs-principles-design.md#_field_stability -->

## Summary

Following up on [RFC 0050](https://github.com/elastic/ecs/pull/2475), which introduced an initial batch of `gen_ai` fields, this RFC adds six additional fields based on user feedback and OTel Semantic Conventions v1.40.0+. The fields cover the following GenAI interactions: system instructions, input and output messages, tool definitions available to an agent or model, and tool call arguments and results. All six fields carry the same names as their OTel counterparts and are defined as `flattened` to align with how the OTel Collector Elasticsearch exporter handles complex attribute types[1].

## Usage

These fields enable security monitoring and threat detection for GenAI applications. Practitioners can use `gen_ai.input.messages` and `gen_ai.output.messages` to audit full conversation context for prompt injection, data exfiltration, or policy violations. `gen_ai.system_instructions` captures the system prompt, which is a common target for injection attacks. The `gen_ai.tool.*` fields allow monitoring of agentic tool use — for example, detecting whether a model was manipulated into calling a privileged tool with attacker-controlled arguments.[2]

## Fields

Field | Type | Description /Usage
-- | -- | --
gen_ai.system_instructions | flattened | The system message or instructions provided to the GenAI model separately from the chat history.
gen_ai.input.messages | flattened | The chat history provided to the model as an input.
gen_ai.output.messages | flattened | Messages returned by the model where each message represents a specific model response (choice, candidate).
gen_ai.tool.definitions | flattened | (Part of invoke_agent span) The list of source system tool definitions available to the GenAI agent or model.
gen_ai.tool.call.arguments | flattened | (Part of OTel execute_tool span) Parameters passed to the tool call.
gen_ai.tool.call.result | flattened | (Part of OTel execute_tool span) The result returned by the tool call (if any and if execution was successful).

Changes based on OTel https://github.com/open-telemetry/semantic-conventions/pull/2179/files

All six fields use `type: flattened` without defined child fields. Explicit leaf-field definitions are not appropriate here because the OTel specification defines these as `any`-typed attributes whose exact structure varies by model vendor — defining explicit children would create upstream dependencies on vendor-specific schemas. Cross-integration type conflicts are prevented by the upstream OTel specification that all producers are expected to follow; the expected data shapes are illustrated in the YAML examples in `rfcs/text/0052/gen_ai.yaml`. See the Concerns section for the full justification for `flattened` over `nested`.

## Source data

### OTel GenAI span (OpenAI)

An ECS event produced from an OpenAI Chat Completions API call instrumented via the [OTel GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/). This example includes a tool call exchange where the model requests weather data.

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

## Scope of impact

These are new additive fields; no breaking changes to existing ingest pipelines. The OTel Collector Elasticsearch exporter already maps complex `any`-typed attributes to `flattened`, so OTel-based ingest is compatible without modification. Custom integrations collecting GenAI telemetry may need to add field mappings for the new fields.

## Concerns

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

## References

### In-line references for this RFC

[1] https://github.com/elastic/ecs/pull/2532#issuecomment-4121325575
[2] GH issue can be provided upon request

### General

* https://opentelemetry.io/blog/2024/otel-generative-ai/
* https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/
* https://github.com/open-telemetry/semantic-conventions/commits/main/docs/gen-ai/gen-ai-events.md
* https://github.com/open-telemetry/semantic-conventions/pull/2702
* https://www.elastic.co/docs/reference/ecs/ecs-gen_ai#_gen_ai_field_details
* https://github.com/open-telemetry/semantic-conventions/pull/2179/

### RFC Pull Requests

* Stage 0: https://github.com/elastic/ecs/pull/2519
* Stage 1: https://github.com/elastic/ecs/pull/2525
* Stage 2: https://github.com/elastic/ecs/pull/2532
