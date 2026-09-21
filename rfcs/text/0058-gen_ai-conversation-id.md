# 0058: Add gen_ai.conversation.id

- Stage: **Proposal**
- Date: **TBD**
- Target maturity: **beta**

## Summary

Add `gen_ai.conversation.id` to the existing `gen_ai` fieldset so GenAI telemetry can correlate turns, tool calls, and detections that belong to the same conversation (session/thread). The field already exists in the OpenTelemetry GenAI semantic conventions as a string attribute; ECS already mirrors adjacent identifiers such as `gen_ai.agent.id` and `gen_ai.response.id` but does not yet define this conversation-level key.

## Usage

Security and observability pipelines emit one or more events per model turn. Without a stable conversation key, analysts must reconstruct multi-turn attacks (prompt injection across turns, tool misuse spanning a session, policy violations in Agent Builder / assistant chats) by guesswork or vendor-specific headers.

With `gen_ai.conversation.id`:

- Detection rules and hunts can group alerts and traces for a single chat session.
- Kibana Agent Builder and related eval/trace tooling can join workflow step `conversation_id` values to OTel/ECS attributes already named `gen_ai.conversation.id`.
- OTel-instrumented GenAI apps map the attribute 1:1 into ECS without inventing a custom field.

## Fields

Proposed definition (also in [`rfcs/text/0058/gen_ai.yaml`](./0058/gen_ai.yaml)):

```yaml
- name: conversation.id
  type: keyword
  description: >
    The unique identifier for a conversation (session, thread), used to store
    and correlate messages within this conversation.
  example: conv_5j66UpCpwteGg4YSxUnt7lPY
  level: extended
  beta: This field is beta and subject to change.
  otel:
    - relation: match
```

This is a single additive keyword under the existing `gen_ai` group. No child objects or `flattened` fields are required.

## Source data

### OTel GenAI attribute

OTel documents `gen_ai.conversation.id` as the unique identifier for a conversation (session, thread), example `conv_5j66UpCpwteGg4YSxUnt7lPY` ([GenAI attributes registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)).

```json
{
  "attributes": {
    "gen_ai.conversation.id": "conv_5j66UpCpwteGg4YSxUnt7lPY",
    "gen_ai.operation.name": "chat",
    "gen_ai.request.model": "gpt-4o",
    "gen_ai.response.id": "chatcmpl-123"
  }
}
```

### Kibana Agent Builder / assistant converse API

Agent Builder converse responses expose a `conversation_id` that is already correlated in Security evals to `attributes.gen_ai.conversation.id`.

```json
{
  "conversation_id": "conv_5j66UpCpwteGg4YSxUnt7lPY",
  "response": {
    "message": "Here is a summary of the alert triage steps."
  }
}
```

### Security detection / trace join (illustrative ECS event)

```json
{
  "@timestamp": "2026-09-21T12:00:00.000Z",
  "event": {
    "kind": "event",
    "category": ["api"],
    "type": ["info"]
  },
  "gen_ai": {
    "conversation.id": "conv_5j66UpCpwteGg4YSxUnt7lPY",
    "operation.name": "chat",
    "provider.name": "openai",
    "request.model": "gpt-4o",
    "response.id": "chatcmpl-123"
  },
  "user": {
    "name": "analyst"
  }
}
```

## Scope of impact

* **Ingestion:** Additive only. OTel Collector / EDOT paths that already export `gen_ai.conversation.id` can land the field without remapping. Custom integrations may add a one-line copy from vendor session/thread ids.
* **Usage:** Enables session-scoped detections, dashboards, and alert correlation. No breaking change to existing `gen_ai.*` consumers.
* **ECS project:** One new field in `schemas/gen_ai.yml` after Proposal acceptance; docs/generated artifacts updated in the follow-on schema PR (or automation on merge).

## Concerns

* **Overlap with `gen_ai.response.id`:** Response id identifies a single completion; conversation id spans many turns. Resolution: keep both; document conversation as session/thread scope.
* **Overlap with tracing `trace.id`:** A conversation may span multiple traces. Resolution: conversation id is application-level session identity, not a substitute for W3C trace context.
* **Cardinality:** Keyword session ids are high-cardinality by design (same class as `gen_ai.agent.id` / `gen_ai.response.id`). Resolution: `level: extended`; producers SHOULD use stable opaque ids, not free-text titles.

## People

* @Mikaayenson | author

## References

* [ECS RFC process](https://github.com/elastic/ecs/blob/main/rfcs/PROCESS.md)
* [OTel GenAI attributes — `gen_ai.conversation.id`](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)
* Related RFCs: [0050](./0050-gen_ai-security-fields.md), [0052](./0052-gen_ai-additional-fields.md)

### RFC Pull Requests

* Proposal: (this PR)
