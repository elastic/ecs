# 0060: Add gen_ai.tool.source.* and gen_ai.usage.cache_*.input_tokens

- Stage: **Proposal**
- Date: **TBD**
- Target maturity: **beta**

## Summary

Add five fields to the existing `gen_ai` fieldset:

- `gen_ai.tool.source.name`, `gen_ai.tool.source.type` and `gen_ai.tool.source.address`, which record where a tool came from (an MCP server, a gateway target, a registry entry or a request-defined tool). `gen_ai.tool.*` identifies a tool by name only, and nothing in ECS says which source offered it.
- `gen_ai.usage.cache_read.input_tokens` and `gen_ai.usage.cache_write.input_tokens`, which exist in the OpenTelemetry GenAI semantic conventions but not in ECS, and which several providers already log.

The tool source fields are new to both ECS and OTel; the cache token fields match OTel attributes of the same name.

## Usage

**Tool source.** Two cases cannot be detected today:

1. *Look-alike tool.* A second MCP server offers `fetch_order_detials` next to the legitimate `fetch_order_details`. Both appear in `gen_ai.tool.definitions` with a name and description, and nothing says they come from different servers.
2. *Changed definition.* A tool keeps its name, but its description or source changes between sessions, which is indistinguishable from the same tool being re-advertised.

Detections for tool-definition poisoning and for tool impersonation or typosquatting (both under the OWASP Tool Misuse & Exploitation risk, ASI02) key on "same or similar name, different source" or "same source, changed definition". Both need a source identity, and this field is the prerequisite for detecting them across integrations rather than per integration.

**Cache tokens.** Cache read and write volume separates normal cost from abusive or anomalous usage, and a cache write followed by reads can indicate a large reused context. Bedrock invocation logs report both cache reads and cache writes, and the OpenAI Responses API reports cache reads, but neither has an ECS field to land in.

## Fields

Proposed definitions (also in [`rfcs/text/0060/gen_ai.yaml`](./0060/gen_ai.yaml)):

```yaml
- name: tool.source.name
  type: keyword
  description: >
    The name of the source the tool came from, such as an MCP server name,
    a gateway target or a registry id. Identifies where a tool was offered
    from, as opposed to `gen_ai.tool.name`, which identifies the tool itself.
  example: XYZPROD001
  level: extended
  beta: This field is beta and subject to change.
  otel:
    - relation: na

- name: tool.source.type
  type: keyword
  description: >
    The type of the source the tool came from. This describes where the tool
    was offered from, not how it executes (see `gen_ai.tool.type`).
  example: gateway_target
  expected_values:
    - mcp_server
    - gateway_target
    - registry
    - inline
  level: extended
  beta: This field is beta and subject to change.
  otel:
    - relation: na

- name: tool.source.address
  type: keyword
  description: >
    The address of the source the tool came from, when the source is
    addressable, such as the URL of an MCP server.
  example: https://mcp.example.com/sse
  level: extended
  beta: This field is beta and subject to change.
  otel:
    - relation: related
      attribute: server.address
      note: >
        In OTel, `server.address` (with `server.port`) on an MCP client span is the address of the server
        being called. `gen_ai.tool.source.address` is the address of the source the tool was offered from,
        which is not always the endpoint of the GenAI service.

- name: usage.cache_read.input_tokens
  type: long
  description: >
    The number of input tokens served from a provider-managed cache.
    This value SHOULD be included in `gen_ai.usage.input_tokens`.
  example: 1024
  level: extended
  beta: This field is beta and subject to change.
  otel:
    - relation: match

- name: usage.cache_write.input_tokens
  type: long
  description: >
    The number of input tokens written to a provider-managed cache.
    This value SHOULD be included in `gen_ai.usage.input_tokens`.
  example: 2048
  level: extended
  beta: This field is beta and subject to change.
  otel:
    - relation: match
```

The five fields are additive keywords and longs under the existing `gen_ai` group. No `object` or `flattened` fields are added. The cache fields use `long`, as required by the integer convention applied in #2646.

The tool source also applies to each entry of the existing `gen_ai.tool.definitions` field, which is `flattened`. The source goes under a `source` key in the entry, so that field needs no schema change:

```json
"gen_ai.tool.definitions": [
  {"name": "fetch_order_details", "description": "…", "type": "function",
   "source": {"name": "XYZPROD001", "type": "gateway_target"}}
]
```

**Field relationships.**

- `gen_ai.tool.source.type` is distinct from `gen_ai.tool.type` (`function`, `extension`, `datastore`): the first says where the tool came from, the second how it executes.
- `gen_ai.tool.source.address` is `related` to the OTel `server.address` / `server.port` of MCP client spans. The OTel `mcp.*` attributes (`mcp.method.name`, `mcp.session.id`, `mcp.resource.uri`, `mcp.protocol.version`) define no server name.
- `gen_ai.tool.source.name` has no OTel equivalent; see Concerns.

## Source data

The documents below are trimmed to the relevant fields. The AgentCore, ChatGPT Enterprise, OTel MCP span and OpenAI documents are illustrative: they are shaped from the field descriptions in the integration sub-issues (elastic/integrations#20889, #20898, #20744) and from the OTel MCP conventions. The table of other integrations is taken from their sub-issues (#20745, #20741, #20742, #20898). The Bedrock document is an excerpt of a real invocation log with account, identity and request identifiers redacted.

### AWS Bedrock AgentCore gateway log (elastic/integrations#20889)

The gateway log message already carries the source, but the integration maps only the tool name today. The target is dropped, and the tool name embeds the `DocumentRetrieval___` prefix, which should be split off.

```json
{
  "message": "Processing request for tool DocumentRetrieval___fetch_order_details from target XYZPROD001"
}
```

ECS event with the proposed fields:

```json
{
  "gen_ai": {
    "provider.name": "aws.bedrock",
    "operation.name": "execute_tool",
    "tool": {
      "name": "fetch_order_details",
      "source": { "name": "XYZPROD001", "type": "gateway_target" }
    }
  },
  "event": { "action": "invoke_gateway" }
}
```

### MCP tool calls in other integrations

Several integrations already carry the source, folded into the tool name or in an integration-specific field:

| Integration | Source data in the native event |
|---|---|
| LiteLLM (#20745) | `mcp_namespaced_tool_name` in `/spend/logs/v2` (MCP tool calls only) |
| `claude_code` (#20741) | `mcp_tool_name` and `mcp_server_name`, both parsed from the `tool_parameters` JSON blob by the ingest pipeline |
| `claude_cowork` (#20742) | `mcp_tool.name`, a direct structured attribute |
| ChatGPT Enterprise (#20898) | `app_name` (e.g. `Slack`, `gdrive`) and `app_type` (`MCP` or `SERVICE`) |

For example, a ChatGPT Enterprise connector call:

```json
{ "app_name": "Slack", "app_type": "MCP" }
```

maps to:

```json
{
  "gen_ai": {
    "tool": {
      "name": "Slack",
      "type": "extension",
      "source": { "name": "Slack", "type": "mcp_server" }
    }
  }
}
```

### OTel MCP client span

OTel MCP client spans carry the address of the server but not its name, so `gen_ai.tool.source.address` can be mapped and `gen_ai.tool.source.name` needs a source from the integration or collector configuration.

```json
{
  "attributes": {
    "mcp.method.name": "tools/call",
    "mcp.session.id": "…",
    "gen_ai.operation.name": "execute_tool",
    "gen_ai.tool.name": "fetch_order_details",
    "server.address": "mcp.example.com",
    "server.port": 443
  }
}
```

### AWS Bedrock model invocation log (cache tokens)

Bedrock invocation logs carry the cache counts, which today land only under `aws_bedrock.invocation.input.*`. Excerpt of a real log, redacted (the cache counts are zero in this sample):

```json
{
  "aws_bedrock.invocation.model_id": "us.anthropic.claude-sonnet-5-5",
  "aws_bedrock.invocation.input.input_token_count": 436,
  "aws_bedrock.invocation.input.cacheReadInputTokenCount": 0,
  "aws_bedrock.invocation.input.cacheWriteInputTokenCount": 0,
  "aws_bedrock.invocation.output.output_token_count": 33,
  "event.action": "Converse"
}
```

ECS event with the proposed fields:

```json
{
  "gen_ai": {
    "usage": {
      "input_tokens": 436,
      "output_tokens": 33,
      "cache_read.input_tokens": 0,
      "cache_write.input_tokens": 0
    }
  }
}
```

### OpenAI Responses API (elastic/integrations#20744)

The OpenAI integration proposal already requests the cache read value, from `usage.input_tokens_details.cached_tokens` of the response object:

```json
{
  "usage": {
    "input_tokens": 2100,
    "input_tokens_details": { "cached_tokens": 1024 },
    "output_tokens": 80
  }
}
```

```json
{
  "gen_ai": {
    "usage": {
      "input_tokens": 2100,
      "output_tokens": 80,
      "cache_read.input_tokens": 1024
    }
  }
}
```

## Scope of impact

* **Ingestion:** Additive only. The tool source fields would be populated by `aws_bedrock_agentcore` (gateway target), LiteLLM, `claude_code`, `claude_cowork` and `openai_chatgpt_enterprise` where the MCP server or app is known, by OTel GenAI / MCP ingestion (the address from `server.address`), and by other integrations where the source is known, for example `inline` for request-defined tools. The cache token fields would be populated by `aws_bedrock` and `openai`. All of this is tracked under elastic/integrations#20737.
* **Usage:** Enables detections for tool-definition poisoning and tool impersonation, and per-model cost and abuse baselines. No breaking change to existing `gen_ai.*` consumers.
* **ECS project:** Five new fields in `schemas/gen_ai.yml`, with regenerated docs, OTel alignment documentation and artifacts in the follow-on schema change.

## Concerns

* **`server.*` is not the tool source:** `server.address` is a network field whose meaning depends on the event: the model endpoint on a GenAI request, the MCP server on an MCP client span. Tools listed in one event can come from several sources, so one event-level field cannot describe them. Resolution: use a dedicated `gen_ai.tool.source.address`, populated from `server.address` / `server.port` where an MCP client span provides it, and declare the relation to `server.address` as `related`, with a note, instead of reusing the field.
* **`gen_ai.tool.source.name` has no OTel equivalent:** The OTel `mcp.*` attributes define no server name. Resolution: propose `gen_ai.tool.source.*` upstream in `open-telemetry/semantic-conventions-genai`, where `gen_ai.skill.source.uri` is a naming precedent, and declare `otel: na` for the name and type until then.
* **`gen_ai.tool.source.type` could be confused with `gen_ai.tool.type`:** The OTel values (`function`, `extension`, `datastore`) describe how the tool executes. Resolution: keep the fields separate and state the difference in the field descriptions.
* **Naming overlap with the `source.*` fieldset:** ECS already has `source.*` for the network source of an event (for example `source.address`), so `gen_ai.tool.source.*` could be confused with it. Resolution: the fields sit under `gen_ai.tool.`, so the names cannot collide. The exact name is open for review, and an alternative such as `gen_ai.tool.origin.*` would not change the proposal.
* **Overlap of cache tokens with `gen_ai.usage.input_tokens`:** OTel states that cache values SHOULD be included in `input_tokens`. Resolution: copy that statement into both descriptions so consumers do not add the cache values on top of the input count. `gen_ai.token.type` does not cover them.
* **Cardinality and sensitivity of the source address:** Source addresses can be internal URLs. Resolution: the field is `level: extended`, optional, and populated only when the source is addressable.
* **The tracking epic expected no new fields:** elastic/integrations#20737 anticipated none (comment of 2026-09-04). Resolution: no existing field can carry a tool source, and the cache token fields already exist in OTel.

## People

The following are the people that consulted on the contents of this RFC.

* @angelosoliveira | author

## References

* [ECS RFC process](https://github.com/elastic/ecs/blob/main/rfcs/PROCESS.md)
* [Epic: ECS GenAI Field Support for Security Detections](https://github.com/elastic/integrations/issues/20737)
* [elastic/integrations#20889: aws_bedrock_agentcore](https://github.com/elastic/integrations/issues/20889), [#20744: openai](https://github.com/elastic/integrations/issues/20744), [#20745: litellm](https://github.com/elastic/integrations/issues/20745), [#20741: claude_code](https://github.com/elastic/integrations/issues/20741), [#20742: claude_cowork](https://github.com/elastic/integrations/issues/20742), [#20898: openai_chatgpt_enterprise](https://github.com/elastic/integrations/issues/20898)
* [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
* [ECS #2646: GenAI numbers datatype](https://github.com/elastic/ecs/pull/2646)
* Related RFCs: [0050](./0050-gen_ai-security-fields.md), [0052](./0052-gen_ai-additional-fields.md), [0058](./0058-gen_ai-conversation-id.md)

### RFC Pull Requests

* Proposal: https://github.com/elastic/ecs/pull/2711
