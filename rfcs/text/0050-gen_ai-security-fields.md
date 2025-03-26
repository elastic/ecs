# 0050: GenAI fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: 2025-03-26 <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

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

<!--
Archived by @peasead w/Elastic Security Labs 10/29/2024
The `llm` fields proposed are: [WIP]

Field | Type | Description /Usage
-- | -- | --
llm.request.content	|	text	|	The full text of the user's request to the LLM.
llm.request.token_count	|	integer	|	Number of tokens in the user's request.
llm.response.content	|	text	|	The full text of the LLM's response.
llm.response.token_count	|	integer	|	Number of tokens in the LLM's response.
llm.user.id	|	keyword	|	Unique identifier for the user.
llm.user.rn	|	keyword	|	Unique resource name for the user.
llm.request.id	|	keyword	|	Unique identifier for the LLM request.
llm.response.id	|	keyword	|	Unique identifier for the LLM response.
llm.response.error_code	|	keyword	|	Error code returned in the LLM response.
llm.response.stop_reason	|	keyword	|	Reason the LLM response stopped.
llm.request.timestamp	|	date	|	Timestamp when the request was made.
llm.response.timestamp	|	date	|	Timestamp when the response was received.
llm.model.name	|	keyword	|	Name of the LLM model used to generate the response.
llm.model.version	|	keyword	|	Version of the LLM model used to generate the response.
llm.model.id	|	keyword	|	Unique identifier for the LLM model.
llm.model.role	|	keyword	|	Role of the LLM model in the interaction.
llm.model.type	|	keyword	|	Type of LLM model.
llm.model.description	|	keyword	|	Description of the LLM model.
llm.model.instructions	|	text	|	Custom instructions for the LLM model.
llm.model.parameters	|	keyword	|	Parameters used to confirm the LLM model.
-->

The `gen_ai` fields proposed to be backported from Open Telemetry are:

Fields, types, and descriptions are sourced from [OTel GenAI documentation](https://opentelemetry.io/docs/specs/semconv/attributes-registry/gen-ai/) as of March 25, 2025

| Attribute | Type | Description | Examples |
|---|---|---|---|
| `gen_ai.agent.description` | string | Free-form description of the GenAI agent provided by the application. | `Helps with math problems`; `Generates fiction stories` |
| `gen_ai.agent.id` | string | The unique identifier of the GenAI agent. | `asst_5j66UpCpwteGg4YSxUnt7lPY` |
| `gen_ai.agent.name` | string | Human-readable name of the GenAI agent provided by the application. | `Math Tutor`; `Fiction Writer` |
| `gen_ai.operation.name` | string | The name of the operation being performed. [1] | `chat`; `text_completion`; `embeddings` |
| `gen_ai.output.type` | string | Represents the content type requested by the client. [2] | `text`; `json`; `image` |
|`gen_ai.request.choice.count` | int | The target number of candidate completions to return. | `3` |
| `gen_ai.request.encoding_formats` | string[] | The encoding formats requested in an embeddings operation, if specified. [3] | `["base64"]`; `["float", "binary"]` |
| `gen_ai.request.frequency_penalty` | double | The frequency penalty setting for the GenAI request. | `0.1` |
| `gen_ai.request.max_tokens` | int | The maximum number of tokens the model generates for a request. | `100` |
| `gen_ai.request.model` | string | The name of the GenAI model a request is being made to. | `gpt-4` |
| `gen_ai.request.presence_penalty` | double | The presence penalty setting for the GenAI request. | `0.1` |
| `gen_ai.request.seed` | int | Requests with same seed value more likely to return same result. | `100` |
| `gen_ai.request.stop_sequences` | string[] | List of sequences that the model will use to stop generating further tokens. | `["forest", "lived"]` |
| `gen_ai.request.temperature` | double | The temperature setting for the GenAI request. | `0.0` |
| `gen_ai.request.top_k` | double | The top_k sampling setting for the GenAI request. | `1.0` |
| `gen_ai.request.top_p` | double | The top_p sampling setting for the GenAI request. | `1.0` |
| `gen_ai.response.finish_reasons` | string[] | Array of reasons the model stopped generating tokens, corresponding to each generation received. | `["stop"]`; `["stop", "length"]` |
| `gen_ai.response.id` | string | The unique identifier for the completion. | `chatcmpl-123` |
| `gen_ai.response.model` | string | The name of the model that generated the response. | `gpt-4-0613` |
| `gen_ai.system` | string | The Generative AI product as identified by the client or server instrumentation. [4] | `openai` |
| `gen_ai.token.type` | string | The type of token being counted. | `input`; `output` |
| `gen_ai.tool.call.id` | string | The tool call identifier. | `call_mszuSIzqtI65i1wAUOE8w5H4` |
| `gen_ai.tool.name` | string | Name of the tool utilized by the agent. | `Flights` |
| `gen_ai.tool.type` | string | Type of the tool utilized by the agent [5] | `function`; `extension`; `datastore` |
| `gen_ai.usage.input_tokens` | int | The number of tokens used in the GenAI input (prompt). | `100` |
| `gen_ai.usage.output_tokens` | int | The number of tokens used in the GenAI response (completion). | `180` |

Fields as of Mar 25, 2025 at this OTel [commit](https://github.com/open-telemetry/semantic-conventions/blob/78c42c576a25743902192466cf7ff81889bf3630/docs/attributes-registry/gen-ai.md).

<!-- Archived by @susan-shu-c w/Elastic Security 03/25/2025 -->
<!--
Field | Type | Description /Usage | Example
-- | -- | -- | --
gen_ai | nested | This defines the attributes used to describe telemetry in the context of Generative Artificial Intelligence (GenAI) Models requests and responses.
gen_ai.analysis | nested |
gen_ai.analysis.action_recommended | keyword | Recommended actions based on the analysis.
gen_ai.analysis.finding | keyword | Detailed findings from security tools.
gen_ai.analysis.function | keyword | Name of the security or analysis function used.
gen_ai.analysis.tool_names | keyword | Name of the security or analysis tools used.
gen_ai.assistant | nested |
gen_ai.assistant.message | nested |
gen_ai.assistant.message.role | keyword | The actual role of the message author as passed in the message. | `assistant` or `bot`
gen_ai.assistant.message.content | keyword | The contents of the assistant message. | `Spans, events, metrics defined by the GenAI semantic conventions.`
gen_ai.assistant.message.tool_calls | nested | The tool calls generated by the model, such as function calls. |
gen_ai.assistant.message.tool_calls.id | text | The id of the tool call | `call_mszuSIzqtI65i1wAUOE8w5H4`
gen_ai.assistant.message.tool_calls.type | keyword | The type of the tool | `function`
gen_ai.assistant.message.tool_calls.function | nested
gen_ai.assistant.message.tool_calls.function.name | keyword | The name of the function to call | `get_link_to_otel_semconv`
gen_ai.assistant.message.tool_calls.function.arguments | keyword | The arguments to pass the the function | `{"semconv": "gen_ai"}`
gen_ai.choice | nested | This event describes model-generated individual chat response
gen_ai.choice.finish_reason | keyword | The reason the model stopped generating tokens. | `stop`, `tool_calls`, `content_filter`
gen_ai.choice.index | intiger | The index of the choice in the list of choices. | `1`
gen_ai.choice.message | nested | GenAI response message. |
gen_ai.choice.message.role | The actual role of the message author as passed in the message. | `assistant` or `bot`
gen_ai.choice.message.content | The contents of the choice message. | `Spans, events, metrics defined by the GenAI semantic conventions.`
gen_ai.choice.message.tool_calls | nested | The tool calls generated by the model, such as function calls. |
gen_ai.choice.message.tool_calls.id | text | The id of the tool call | `call_mszuSIzqtI65i1wAUOE8w5H4`
gen_ai.choice.message.tool_calls.type | keyword | The type of the tool | `function`
gen_ai.choice.message.tool_calls.function | nested
gen_ai.choice.message.tool_calls.function.name | keyword | The name of the function to call | `get_link_to_otel_semconv`
gen_ai.choice.message.tool_calls.function.arguments | keyword | The arguments to pass the the function | `{"semconv": "gen_ai"}`
gen_ai.compliance | nested |
gen_ai.compliance.request_triggered | keyword | Lists compliance-related filters that were triggered during the processing of the request, such as data privacy filters or regulatory compliance checks.
gen_ai.compliance.response_triggered | keyword | Lists compliance-related filters that were triggered during the processing of the response, such as data privacy filters or regulatory compliance checks.
gen_ai.compliance.violation_code | keyword | Code identifying the specific compliance rule that was violated.
gen_ai.compliance.violation_detected | boolean | Indicates if any compliance violation was detected during the interaction.
gen_ai.operation.name | keyword | The name of the operation being performed. | `chat`, `text_completion`
gen_ai.openai | nested | This group defines attributes for OpenAI. |
gen_ai.openai.request.response_format | keyword | The response format that is requested. | `json_object`, `json_schema`, `auto`
gen_ai.openai.request.seed | integer | Requests with same seed value more likely to return same result. | `100`
gen_ai.openai.request.service_tier | keyword | The service tier requested. May be a specific tier, detault, or auto. | `auto`, `default`
gen_ai.openai.response.service_tier | keyword | The service tier used for the response. | `scale`, `default`
gen_ai.owasp | nested |
gen_ai.owasp.description | text | Description of the OWASP risk triggered.
gen_ai.owasp.id | keyword | Identifier for the OWASP risk addressed.
gen_ai.performance | nested
gen_ai.performance.request_size | long | Size of the request payload in bytes.
gen_ai.performance.response_size | long | Size of the response payload in bytes.
gen_ai.performance.response_time | long | Time taken by the LLM to generate a response in milliseconds.
gen_ai.performance.start_response_time | long | Time taken by the LLM to send first response byte in milliseconds.
gen_ai.policy | nested
gen_ai.policy.action | keyword | Action taken due to a policy violation, such as blocking, alerting, or modifying the content.
gen_ai.policy.confidence | keyword | Confidence level in the policy match that triggered the action, quantifying how closely the identified content matched the policy criteria.
gen_ai.policy.match_detail | nested
gen_ai.policy.name | keyword | Name of the specific policy that was triggered.
gen_ai.policy.violation | boolean | Specifies if a security policy was violated.
gen_ai.request | nested | This group defines attributes for GenAI request actions. |
gen_ai.request.id | keyword | Unique identifier for the LLM request.
gen_ai.request.max_tokens | integer | The maximum number of tokens the model generates for a request. | `100`
gen_ai.request.model | nested |
gen_ai.request.model.description | text | Description of the LLM model.
gen_ai.request.model.instructions | text | Custom instructions for the LLM model.
gen_ai.request.model.role | keyword | Role of the LLM model in the interaction.
gen_ai.request.model.type | keyword | Type of LLM model.
gen_ai.request.model.version | keyword | Version of the LLM model used to generate the response.
gen_ai.request.model.id | keyword | The name of the GenAI model a request is being made to. | `gpt-4`
gen_ai.request.temperature | integer | The temperature setting for the GenAI request. | `0.0`
gen_ai.request.timestamp | date | Timestamp when the request was made.
gen_ai.request.top_p | integer | The top_p sampling setting for the GenAI request. | `1.0`
gen_ai.request.top_k | integer | The top_k sampling setting for the GenAI request. | `1.0`
gen_ai.request.stop_sequences | keyword | List of sequences that the model will use to stop generating further tokens. | `["forest", "lived"]`
gen_ai.request.frequency_penalty | integer | The frequency penalty setting for the GenAI request. | `0.1`
gen_ai.request.presence_penalty | integer | The presence penalty setting for the GenAI request. | `0.1`
gen_ai.response | nested | This group defines attributes for GenAI response actions. |
gen_ai.response.error_code | keyword | Error code returned in the LLM response.
gen_ai.response.finish_reasons | keyword | Array of reasons the model stopped generating tokens, corresponding to each generation received. | `["stop", "stop", "length"]`
gen_ai.response.id | keyword | The unique identifier for the completion. | `chatcmpl-123`
gen_ai.response.model | keyword | The name of the model that generated the response. | `gpt-4-0613`
gen_ai.response.timestamp | date | Timestamp when the response was received.
gen_ai.security | nested |
gen_ai.security.halluncination_consistency | integer | Consistency check between multiple responses.
gen_ai.security.jailbreak_score | integer | Measures similarity to known jailbreak attempts.
gen_ai.security.prompt_injection_score | integer | Measures similarity to known prompt injection attacks.
gen_ai.security.refusal_score | integer | Measures similarity to known LLM refusal responses.
gen_ai.security.regex_pattern_count | integer | Counts occurrences of strings matching user-defined regex patterns.
gen_ai.sentiment | nested |
gen_ai.sentiment.content_categories | keyword | Categories of content identified as sensitive or requiring moderation.
gen_ai.sentiment.content_inappropriate | keyword | Whether the content was flagged as inappropriate or sensitive.
gen_ai.sentiment.score | integer | Sentiment analysis score.
gen_ai.sentiment.toxicity_score | integer | Toxicity analysis score.
gen_ai.system | nested |
gen_ai.system.product | keyword | The Generative AI product as identified by the client or server instrumentation. | `openai`
gen_ai.system.message | nested | This event describes the instructions passed to the GenAI model.
gen_ai.system.message.role | keyword | The actual role of the message author as passed in the message. | `system` or `instructions`
gen_ai.system.message.content | keyword | The contents of the system message. | `You're a friendly bot that answers questions about GenAi.`
gen_ai.text | nested
gen_ai.text.complexity_score | integer | Evaluates the complexity of the text.
gen_ai.text.readability_score | integer | Measures the readability level of the text.
gen_ai.text.similarity_score | integer | Measures the similarity between the prompt and response.
gen_ai.token.type | keyword | The type of token being counted. | `input`, `output`
gen_ai.tool | nested |
gen_ai.tool.message | nested |
gen_ai.tool.message.role | keyword | The actual role of the message author as passed in the message. | `tool` or `function`
gen_ai.tool.message.content | keyword | The contents of the tool message. | `elastic.co`
gen_ai.tool.message.id | text | Tool call that this message is responding to. | `call_mszuSIzqtI65i1wAUOE8w5H4`
gen_ai.usage | nested | This group defines attributes for GenAI usage. |
gen_ai.usage.completion_tokens | integer | Number of tokens in the LLM's response.
gen_ai.usage.prompt_tokens | integer | Number of tokens in the user's request.
gen_ai.usage.input_tokens | integer | The number of tokens used in the GenAI input (prompt). | `100`
gen_ai.usage.output_tokens | integer | The number of tokens used in the GenAI response (completion). | `180`
gen_ai.user | nested | This event describes the prompt message specified by the user.
gen_ai.user.content | keyword | The contents of the user message. | `What telemetry is reported by OpenAI instrumentations?`
gen_ai.user.id | keyword | Unique identifier for the user.
gen_ai.user.rn | keyword | Unique resource name for the user.
gen_ai.user.role | keyword | The actual role of the message author as passed in the message. | `user` or `customer`

Reuse fields:
* Threat - https://www.elastic.co/guide/en/ecs/current/ecs-threat.html
* Rule - https://www.elastic.co/guide/en/ecs/current/ecs-rule.html
-->

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

* @Mikaayenson | author
* @susan-shu-c | author
* @peasead | author

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

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
