# 0050: GenAI fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: 2025-05-20 <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

This RFC proposes GenAI fields, with the increase of Generative AI and LLM logging. This will benefit our customers and users, allowing them to monitor and protect their LLM/Generative AI deployments.

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

The `gen_ai` fields proposed to be backported from Open Telemetry are:

Fields, types, and descriptions are sourced from [OTel GenAI documentation](https://opentelemetry.io/docs/specs/semconv/attributes-registry/gen-ai/) as of March 25, 2025

Stage 1: changed to Elastic data types

| Attribute | Type | Description | Examples |
|---|---|---|---|
| `gen_ai.agent.description` | text | Free-form description of the GenAI agent provided by the application. | `Helps with math problems`; `Generates fiction stories` |
| `gen_ai.agent.id` | keyword | The unique identifier of the GenAI agent. | `asst_5j66UpCpwteGg4YSxUnt7lPY` |
| `gen_ai.agent.name` | keyword | Human-readable name of the GenAI agent provided by the application. | `Math Tutor`; `Fiction Writer` |
| `gen_ai.operation.name` | keyword | The name of the operation being performed. | `chat`; `text_completion`; `embeddings` |
| `gen_ai.output.type` | keyword | Represents the content type requested by the client. | `text`; `json`; `image` |
| `gen_ai.request.choice.count` | integer | The target number of candidate completions to return. | `3` |
| `gen_ai.request.encoding_formats` | keyword[] | The encoding formats requested in an embeddings operation, if specified. | `["base64"]`; `["float", "binary"]` |
| `gen_ai.request.frequency_penalty` | double | The frequency penalty setting for the GenAI request. | `0.1` |
| `gen_ai.request.max_tokens` | int | The maximum number of tokens the model generates for a request. | `100` |
| `gen_ai.request.model` | string | The name of the GenAI model a request is being made to. | `gpt-4` |
| `gen_ai.request.presence_penalty` | double | The presence penalty setting for the GenAI request. | `0.1` |
| `gen_ai.request.seed` | integer | Requests with same seed value more likely to return same result. | `100` |
| `gen_ai.request.stop_sequences` | keyword[] | List of sequences that the model will use to stop generating further tokens. | `["forest", "lived"]` |
| `gen_ai.request.temperature` | double | The temperature setting for the GenAI request. | `0.0` |
| `gen_ai.request.top_k` | double | The top_k sampling setting for the GenAI request. | `1.0` |
| `gen_ai.request.top_p` | double | The top_p sampling setting for the GenAI request. | `1.0` |
| `gen_ai.response.finish_reasons` | keyword[] | Array of reasons the model stopped generating tokens, corresponding to each generation received. | `["stop"]`; `["stop", "length"]` |
| `gen_ai.response.id` | keyword | The unique identifier for the completion. | `chatcmpl-123` |
| `gen_ai.response.model` | keyword | The name of the model that generated the response. | `gpt-4-0613` |
| `gen_ai.system` | keyword | The Generative AI product as identified by the client or server instrumentation. | `openai` |
| `gen_ai.token.type` | keyword | The type of token being counted. | `input`; `output` |
| `gen_ai.tool.call.id` | keyword | The tool call identifier. | `call_mszuSIzqtI65i1wAUOE8w5H4` |
| `gen_ai.tool.name` | keyword | Name of the tool utilized by the agent. | `Flights` |
| `gen_ai.tool.type` | keyword | Type of the tool utilized by the agent | `function`; `extension`; `datastore` |
| `gen_ai.usage.input_tokens` | integer | The number of tokens used in the GenAI input (prompt). | `100` |
| `gen_ai.usage.output_tokens` | integer | The number of tokens used in the GenAI response (completion). | `180` |

Fields as of Mar 25, 2025 at this OTel [commit](https://github.com/open-telemetry/semantic-conventions/blob/78c42c576a25743902192466cf7ff81889bf3630/docs/attributes-registry/gen-ai.md).

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

To prevent threats to LLM systems, such as misuse, and to log content filters, proposing standardized fields for the purpose of secure and safe LLM usage. Based on frameworks such as OWASP’s LLM Top 10 and MITRE ATLAS.

An example is that a user may be using various LLM vendors or their own deployments, and wish to log all of them in a standardized manner. As an example, Elastic Security has published a [blog](https://www.elastic.co/security-labs/elastic-advances-llm-security) proposing standardized fields for GenAI in order to create detections and prevent threats.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

Stage 1:

Here an example of source data: [Elastic integration for AWS Bedrock logs](https://www.elastic.co/docs/reference/integrations/aws_bedrock). Note: some fields may be updated as the integrations or Bedrock fields change.

```json
{
    "log": {
    "file": {
        "path": "https://s3.us-east-1.amazonaws.com/[redacted].json.gz"
    },
    "offset": 0
    },
    "aws_bedrock": {
    "invocation": {
        "output": {
        "output_token_count": 0,
        "output_content_type": "application/json"
        },
        "schema_version": "1.0",
        "input": {
        "input_content_type": "application/json",
        "input_token_count": 0
        },
    }
    },
    "gen_ai": {
    "completion": "[{\"message\":{\"content\":[],\"id\":\"msg_AcfF5CnpUjHDrW6y2bqWKRK5bWgz3r0gog\",\"model\":\"anthropic.claude-3-sonnet-20240229-v1:0\",\"role\":\"assistant\",\"type\":\"message\",\"usage\":{\"input_tokens\":0,\"output_tokens\":0}},\"type\":\"message_start\"},{\"content_block\":{\"text\":\"\",\"type\":\"text\"},\"index\":0,\"type\":\"content_block_start\"},{\"amazon-bedrock-guardrailAction\":\"INTERVENED\",\"delta\":{\"text\":\"Sorry, the model cannot answer this question.\",\"type\":\"text_delta\"},\"index\":0,\"type\":\"content_block_delta\"},{\"index\":0,\"type\":\"content_block_stop\"},{\"delta\":{\"stop_reason\":\"end_turn\"},\"type\":\"message_delta\",\"usage\":{\"output_tokens\":0}},{\"amazon-bedrock-guardrailAction\":\"INTERVENED\",\"amazon-bedrock-trace\":{\"guardrail\":{\"input\":{\"5qx068m93k7k\":{\"contentPolicy\":{\"filters\":[{\"action\":\"BLOCKED\",\"confidence\":\"HIGH\",\"type\":\"VIOLENCE\"},{\"action\":\"BLOCKED\",\"confidence\":\"HIGH\",\"type\":\"MISCONDUCT\"}]},\"wordPolicy\":{\"customWords\":[{\"action\":\"BLOCKED\",\"match\":\"bomb\"}]}}}}},\"type\":\"message_stop\"}]",
    "request": {
        "top_p": 0.999,
        "max_tokens": 2000,
        "top_k": 250,
        "temperature": 1,
        "model": {
        "role": "assistant",
        "id": "anthropic.claude-3-sonnet-20240229-v1:0",
        "type": "anthropic",
        "version": "bedrock-2023-05-31"
        },
        "id": "7ad88aa7-42d7-40f9-b69e-0e03ba286f4a"
    },
    "system": "aws",
    "performance": {
        "request_size": 248,
        "response_size": 964
    },
    "response": {
        "id": "msg_AcfF5CnpUjHDrW6y2bqWKRK5bWgz3r0gog",
        "timestamp": "2024-04-25T20:22:47.000Z"
    },
    "compliance": {
        "violation_code": [
        "MISCONDUCT",
        "VIOLENCE"
        ],
        "violation_detected": true
    },
    "usage": {
        "completion_tokens": 0,
        "prompt_tokens": 0
    },
    "prompt": "{\"anthropic_version\":\"bedrock-2023-05-31\",\"max_tokens\":2000,\"messages\":[{\"content\":[{\"text\":\"How big of a drone do I need to carry a 5lb bomb?\",\"type\":\"text\"}],\"role\":\"user\"}],\"stop_sequences\":[\"\n\nHuman:\"],\"temperature\":1,\"top_k\":250,\"top_p\":0.999}",
    },
    "security_rule": {
        "category": [
            "Content moderation"
        ],
        "description": [
        "Monitors and block inappropriate keywords."
        ],
        "name": [
        "block-word-bomb"
        ],
        "reference": [
        "[url to reference here]"
        ],
        "ruleset": [
        "Content moderation-keywords"
        ],
        "uuid": [
        "550e8400-e29b-41d4-a716-446655440000; 1100110011"
        ],
        "version": [
        "1.0.0"
        ]
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

As these are new fields, there shouldn't be breaking changes.

## Concerns

**Experimental vs. Stable**
We have begun using OTel fields that were experimental and have since been depricated.

Example is `gen_ai.prompt`. This field has been deprecated by OTel and is handled by [`gen_ai.user.message.content`](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-events.md)(?), but it is being used in the AWS Bedrock integration:
- AWS Bedrock integration `gen_ai.prompt` being used [source](https://github.com/elastic/integrations/blob/main/packages/aws_bedrock/data_stream/invocation/fields/fields.yml#L64-L66)
- [OTel deprecated fields](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/attributes-registry/gen-ai.md#deprecated-genai-attributes)

Almost all of the GenAI fields are "Experimental", if we need to wait for "Stable", we'll probably want to pause this PR and recommend maturity promotion to the OTel team.

**Fields not in OTel**
Also, some of these fields do not exist in OTel yet, so do they need to be added in OTel before they can be considered for inclusion into ECS?

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @susan-shu-c | author (stage 1, stage 0)
* @peasead | author (stage 0)
* @Mikaayenson | subject matter expert

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

* [OpenTelemetry GenAI attributes registry docs](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/attributes-registry/gen-ai.md)
* [OpenTelemetry GenAI docs](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai)
* [OpenTelemetry GenAI registry YAML](https://github.com/open-telemetry/semantic-conventions/blob/main/model/gen-ai/registry.yaml)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/2337


* Stage 1: https://github.com/elastic/ecs/pull/2465
