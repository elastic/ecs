---
name: ecs-pr-review
description: >-
  Reviews ECS pull requests for schema quality before human review: naming,
  description clarity, type strictness, example/pattern/expected_values
  consistency, OTel hints, and duplication/conflict checks against a base schema
  inventory. Produces severity-graded (High/Medium/Low) actionable findings.
---

# ECS PR quality review

This skill reviews **schema and related changes** in an ECS pull request. It complements **ecs-pr-triage** (routing): triage classifies *where* a change should go; this skill checks *how well* fields are defined.

## Inputs

Use what is available in context, or fetch via `gh`:

- `gh pr view <N> --repo <owner/repo> --json title,body,files,additions,deletions,baseRefName,headRefName`
- `gh pr diff <N> --repo <owner/repo>`
- **Schema inventory** at `schema-inventory.tsv` (or equivalent) when provided — flattened field paths from the **base** branch for collision/duplicate reasoning.

## Execution steps

### 1. Scope the review

- Identify files in the diff; prioritize `schemas/**/*.yml`.
- Note any changes under `generated/`, `docs/reference/ecs-*.md`, `scripts/`, `rfcs/`, or `CHANGELOG.next.md` for process rules (see [quality-rules.md](quality-rules.md) **GEN-** rules).

### 2. Parse schema-relevant hunks

- For each `schemas/*.yml` hunk, extract **new or modified field entries** (including nested `fields:`) and the **field set** context (`name`, `root`, `reusable` if present).
- Build the **flattened field path** for each leaf the same way as ECS docs (e.g. `agent.version`, `process.parent.pid`, `@timestamp` for root `base`).

### 3. Apply quality rules

Walk [quality-rules.md](quality-rules.md) **by category** (types, stability, naming, descriptions, examples, structure, duplicates, generated files, OTel):

- Map each issue to a **Rule ID** (e.g. `TYP-H01`, `NM-M02`).
- Assign **High**, **Medium**, or **Low** per the table and §10 of [quality-rules.md](quality-rules.md).
- **Evidence** must cite the diff line or inventory row (field path + file).

### 4. Duplication and conflicts (inventory)

With **schema-inventory.tsv**:

- **Columns (expected):** `flat_name`, `type`, `level`, `fieldset`, `source_file`, `description_snippet` (tab-separated).
- **DUP-H01 / DUP-M01:** compare new/changed paths and semantics against inventory; flag collisions and near-duplicates.
- If inventory is missing, still run **structural** checks from the diff only, and state that collision checks were **limited**.

### 5. Write the report

Fill [report-template.md](report-template.md):

- Start with `# ECS PR Quality Review (automated)` as the title line (H1).
- Immediately after the title block, include **`Overall:`** with **`High: N | Medium: M | Low: L`** (counts inferred from findings).
- Include **`### Summary details`** as 2–4 bullets capturing top themes next (GitHub “summary details” section content).
- Use `<details><summary>…</summary>` **per severity bucket** as in the template.
- End with contributor pointers (CONTRIBUTING, guidelines, schemas README).

### 6. Behaviour constraints

- **No merge authority:** do not approve, request GitHub Review states, or block CI.
- **Actionable fixes:** each finding ends with concrete YAML or process steps.
- Prefer **fewer, accurate** findings over noisy low-value **Low** items.

## Related assets

- [quality-rules.md](quality-rules.md) — canonical rule IDs and severities.
- [report-template.md](report-template.md) — exact output structure.

## Repo rules cross-reference

- [ecs-schema-standards.mdc](../../rules/ecs-schema-standards.mdc)
- [ecs-pr-completeness.mdc](../../rules/ecs-pr-completeness.mdc)
- **Routing / RFC:** still use [ecs-pr-triage](../ecs-pr-triage/SKILL.md) when the question is *Direct PR vs RFC*.
