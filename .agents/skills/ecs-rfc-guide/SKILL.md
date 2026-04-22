---
name: ecs-rfc-guide
description: >-
  Guides contributors through the Elastic Common Schema (ECS) RFC (Proposal)
  process: template sections, target maturity (alpha/beta), rfcs/text artifacts,
  and OTel alignment. Use when a change needs an RFC, when drafting or
  reviewing RFC PRs, or when the user asks how to propose new ECS field sets or
  substantial schema changes.
---

# ECS RFC (Proposal) guide

## When this applies

Use after **ecs-pr-triage** (or equivalent judgment) says **Needs RFC**, or when the user is starting a **new field set**, **breaking** change, **novel use case**, or **ECS-wide** design.

Authoritative process: [rfcs/PROCESS.md](../../../rfcs/PROCESS.md). Template: [rfcs/0000-rfc-template.md](../../../rfcs/0000-rfc-template.md). High-level triggers: [rfcs/README.md](../../../rfcs/README.md).

## Current process (short)

1. Single **Proposal** stage — template must keep `Stage: **Proposal**`.
2. Contributor opens a **PR** that adds the RFC markdown under `rfcs/` (name like `0000-<dash-separated-name>.md` until numbered).
3. Specify **Target maturity:** `alpha`, `beta`, or `mixture` (see [Field stability](../../../docs/reference/ecs-principles-design.md#_field_stability)).
4. ECS team reviews holistically; on approval they assign the **RFC number** and merge.
5. Schema landings at agreed maturity may follow in the same or follow-up PRs (per team practice).

## Template walkthrough

Copy [rfcs/0000-rfc-template.md](../../../rfcs/0000-rfc-template.md). Remove HTML comments as sections are filled.

| Section | What “good” looks like |
|--------|-------------------------|
| **Summary** | 2–5 sentences: what, why, impact. |
| **Usage** | End-to-end: producer → storage → queries/dashboards/detections. |
| **Fields** | Every proposed field: name, type, description, level/maturity, example. Prefer YAML blocks. If `object`/`flattened` without children, justify shape and conflict avoidance (see [schemas/README.md](../../../schemas/README.md)). |
| **Source data** | ≥2 real examples (JSON/logs); link or place large payloads under `rfcs/text/<n>/`. |
| **Scope of impact** | Ingestion (Beats/Agents), Kibana/apps, ECS repo (docs/tooling). |
| **Concerns** | Risks + **resolved** mitigations; OTel overlap; naming; adoption. |
| **People** | Author, SMEs, reviewers. |
| **References** | Prior art, semconv links, related issues/PRs. |

## `rfcs/text/<number>/` folder

When the RFC adds or changes fields:

- Create **`rfcs/text/<number>/`** with standalone **YAML** snippets, large JSON examples, or mappings — especially when the markdown would be huge.
- Use the **next free** folder number (scan `rfcs/text/`; duplicates get fixed at merge per template notes).
- Align filenames with affected field sets (e.g. `faas.yml`, `gen_ai.yaml`) for reviewer navigation.

## OTel alignment (donation period)

- Prefer names/types compatible with [OpenTelemetry Semantic Conventions](https://github.com/open-telemetry/semantic-conventions).
- Call out **match**, **equivalent**, **related**, **conflict** explicitly; plan parallel semconv PR if needed (does not need to merge before ECS RFC PR).
- When implementing later in `schemas/*.yml`, each field needs valid `otel:` metadata per [CONTRIBUTING.md](../../../CONTRIBUTING.md).

## Maturity choice (alpha vs beta)

- **Alpha** — earlier, may change more; good for exploratory or fast-moving domains.
- **Beta** — clearer adoption path; still subject to change before GA.
- **Mixture** — some fields alpha, some beta; explain per field or group.

Promotion after merge is **out of band** from the RFC (team process per PROCESS.md).

## PR hygiene

- Link the **Proposal PR** at the bottom of the RFC (`### RFC Pull Requests`).
- Do **not** replace process with old multi-stage labels found in historical RFCs under `rfcs/text/*.md`; those are legacy examples only.

## Example RFCs (depth reference)

- **FaaS + service reuse:** [rfcs/text/0027-faas-fields.md](../../../rfcs/text/0027-faas-fields.md) + folder `rfcs/text/0027/`.
- **GenAI security fields:** [rfcs/text/0050-gen_ai-security-fields.md](../../../rfcs/text/0050-gen_ai-security-fields.md).
- Use these for **structure** (fields, usage, source data, concerns), not for **stage** metadata.

## Handoff to implementation

After approval, contributors implement in `schemas/*.yml`, run **`make`**, add **CHANGELOG.next.md**, and open or update a normal schema PR if the RFC did not already include merged YAML.

## Related

- Triage and routing: **ecs-pr-triage** skill; [ecs-contribution-routing rule](../../rules/ecs-contribution-routing.mdc).
- YAML details: [ecs-schema-standards rule](../../rules/ecs-schema-standards.mdc).
