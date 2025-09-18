# 0052: Additional fields for Generative AI
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
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
gen_ai.system_instructions | (Looking for feedback) flattened | The system message or instructions provided to the GenAI model separately from the chat history.
gen_ai.input.messages | (Looking for feedback) flattened | The chat history provided to the model as an input.
gen_ai.output.messages | (Looking for feedback) flattened | Messages returned by the model where each message represents a specific model response (choice, candidate).
gen_ai.tool.definitions | (Looking for feedback) nested | (Part of invoke_agent span) The list of source system tool definitions available to the GenAI agent or model.
gen_ai.tool.call.arguments | (Looking for feedback) nested | (Part of OTel execute_tool span) Parameters passed to the tool call.
gen_ai.tool.call.result | (Looking for feedback) flattened | (Part of OTel execute_tool span) The result returned by the tool call (if any and if execution was successful).

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

        // Below needs to be updated, but keeping in this commit for illustration purposes.
        "assistant": {
            "message": {
                "content": "To carry a 5lb package, you would need a drone with sufficient payload capacity. Drones designed for heavy lifting often fall in the industrial or commercial category. Consider drones with a payload capacity of at least 6-7lbs to ensure safe transport and account for additional factors like battery and stability.",
                "role": "assistant",
                "tool_calls": [
                    {
                        "function": "getDroneSpecifications",
                        "arguments": {"payloadWeight": 5},
                        "name": "getDroneSpecifications",
                        "id": "toolCall1",
                        "type": "function_call",
                    },
                    {
                        "function": "retrieveAvailableDronesDocument",
                        "arguments": {"documentType": "availableDrones", "payloadRequirement": 5},
                        "name": "retrieveAvailableDronesDocument",
                        "id": "toolCall2",
                        "type": "function_call",
                    }
                ],
            }
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

In OTel, many field types are set to `any` and are typically .json objects. [Example](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/)
In ECS, should we use something like [flattened](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/flattened) type, if allowed?

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @susan-shu-c | author

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

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
