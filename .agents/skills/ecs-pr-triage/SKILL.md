---
name: ecs-pr-triage
description: >-
  Triages an ECS pull request. Analyzes the PR diff and metadata, classifies the
  change (schema / tooling / docs / mixed), routes it to the correct contribution
  path (direct PR vs RFC Proposal vs needs-discussion), checks PR completeness,
  and produces a structured Triage Report.
---

# ECS PR triage

This skill triages an ECS pull request. It can be invoked manually, by CI, or by any other automation. The agent needs access to the PR diff, changed file list, PR description, and metadata — either already present in context or fetched via tools (e.g. `gh`). It analyzes that context, makes a routing decision, and delivers a triage report.

## Execution steps

### 1. Inventory the PR context

From the PR context available to you (or fetched via `gh pr view`, `gh pr diff`, etc.), extract:

- **PR number, title, author.**
- **Changed file paths** — bucket every path into one of these categories:
  - `schemas/` — source schema YAML (the key signal for routing)
  - `generated/` — build outputs (should only change as a side effect of schema + `make`)
  - `scripts/` — generator tooling, tests, templates
  - `docs/` — hand-authored docs vs generated reference (`docs/reference/ecs-*.md`)
  - `rfcs/` — RFC markdown and supporting YAML
  - `.github/` — CI workflows, templates, issue config
  - Root config — `Makefile`, `version`, `CHANGELOG.next.md`, etc.
- **PR description body** — check which of the 7 template sections from `.github/PULL_REQUEST_TEMPLATE.md` are filled vs empty/placeholder.
- **Diff content** — scan for signals: new field set files, field removals, `type:` changes, new `reusable` entries, `allowed_values` additions, `alpha`/`beta` changes, etc.

### 2. Classify the change

Walk the decision tree in [classification-rules.md](classification-rules.md) **in priority order**:

1. **Check §1 (RFC triggers)** — any match means classification is **Needs RFC**.
   Triggers: new `schemas/*.yml` file, breaking changes (field removal, type change, semantic redefinition), new reuse topology, novel use case, ECS-wide scope, >10 new leaf fields.
2. **Check §3 (ambiguous)** — any match (without §1) means classification is **Needs Discussion**.
   Includes: 3–10 new fields in one field set, new `allowed_values` on categorization fields (`event.category`, `event.type`, `event.kind`), maturity promotions, unjustified `object`/`flattened`.
3. **Otherwise §2** — all remaining low-risk patterns → classification is **Direct PR**.

Assign labels:
- **Change type:** `Schema Change` | `Tooling` | `Documentation` | `Mixed`
- **Scope:** `Minor` | `Moderate` | `Substantial`

### 3. Check completeness

Evaluate against the checklist in [ecs-pr-completeness rule](../../rules/ecs-pr-completeness.mdc):

- PR description: all 7 template sections answered (not empty/placeholder).
- `CHANGELOG.next.md` entry present, in the correct section (Schema Changes vs Tooling and Artifact Changes), includes `#NNNN`.
- If schema change: `generated/` and `docs/reference/` artifacts present in the diff (evidence that `make` was run and outputs committed).
- If new/changed fields relate to OTel semconv: `otel:` metadata present on those fields.
- No hand-edits to files that should only be generator output (`docs/reference/ecs-*.md`, `generated/`).

Mark each item as **met** or **missing**.

### 4. Produce the triage report

Fill [report-template.md](report-template.md) completely. Rules:

- **Cite specific triggers.** E.g. "New file `schemas/foo.yml` detected → RFC required per classification-rules §1."
- **List every missing checklist item** with clear remediation (e.g. "Add a `CHANGELOG.next.md` entry under Schema Changes > Added with `#NNNN`").
- **If Needs RFC:** point the contributor to `rfcs/PROCESS.md` and the RFC template at `rfcs/0000-rfc-template.md`. Reference the **ecs-rfc-guide** skill for a detailed walkthrough.
- **If Needs Discussion:** state exactly what is ambiguous and what a maintainer should weigh in on.

## Decision defaults

- **Conservative:** when borderline, prefer **Needs Discussion** or **Needs RFC** over **Direct PR**. Under-triaging is worse than over-triaging.
- **No approval authority:** the agent triages and reports. It does not approve, request changes, or merge.

## Important repo facts

- **Source of truth for fields:** `schemas/*.yml`. Hand-edits to `generated/` or `docs/reference/ecs-*.md` without a corresponding schema change are errors — flag them.
- **Build pipeline:** `make` regenerates all artifacts; `make test` runs unit tests; `make check` runs generate + test + diff (CI parity).
- **RFC process:** single Proposal stage per `rfcs/PROCESS.md`; template at `rfcs/0000-rfc-template.md`.
- **OTel donation:** new semconv-related fields need `otel:` metadata per `CONTRIBUTING.md`.

## Related assets

- [classification-rules.md](classification-rules.md) — full decision tree with thresholds and examples.
- [report-template.md](report-template.md) — output format to fill.
- [ecs-rfc-guide skill](../ecs-rfc-guide/SKILL.md) — reference for contributors when RFC is needed.
- Rules: [ecs-contribution-routing](../../rules/ecs-contribution-routing.mdc), [ecs-schema-standards](../../rules/ecs-schema-standards.mdc), [ecs-pr-completeness](../../rules/ecs-pr-completeness.mdc).
