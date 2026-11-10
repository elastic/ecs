---
name: ecs-rfc-implement
description: >-
  Implements a merged ECS RFC by extracting field definitions from the RFC
  markdown or its companion YAML fragment, writing proper schemas/*.yml,
  running the build pipeline, and opening a follow-up PR with all generated
  artifacts. Use when an RFC PR has been merged and its fields need to be
  applied to the ECS schema, or when the user says "implement RFC",
  "apply RFC fields", or references a merged RFC PR number.
---

# ECS RFC implementation

Takes a merged RFC and turns it into a complete schema change: `schemas/*.yml` update, generated artifacts, changelog entry, and a PR.

## Inputs

The agent needs **one** of:

- A **PR number** (e.g. `#2598`) — the merged RFC PR.
- An **RFC number** (e.g. `0054`) — looked up directly under `rfcs/text/`.
- An **RFC file path** (e.g. `rfcs/text/0054-extend-entity-fields.md`).

## Execution steps

### 1. Locate the RFC and gather context

1. If given a PR number, run `gh pr view <number> --json title,body,files` to discover the RFC file path(s).
2. Find the RFC markdown: `rfcs/text/<NNNN>-*.md`.
3. Check for an accompanying YAML folder: `rfcs/text/<NNNN>/`. List any `.yml` / `.yaml` files inside.
4. Read the RFC markdown in full. Identify:
   - **Target field set(s)** (e.g. `entity`, `gen_ai`).
   - **Target maturity** (`alpha` or `beta`).
   - Whether the RFC references an existing `schemas/*.yml` (extension) or proposes a brand-new field set.

### 2. Extract field definitions

**Branch A — YAML fragment exists** (e.g. `rfcs/text/0052/gen_ai.yaml`):

1. Read the fragment. It typically has `- name: <fieldset>` with a `fields:` list but may lack the full field-set header (`title`, `group`, `short`, `description`, `type: group`).
2. Validate every field has at minimum: `name`, `type`, `level`, `description`.
3. Note which field set the fragment belongs to (from its `name:` key).

**Branch B — No YAML; fields are in the RFC prose**:

1. Parse the RFC for field tables (markdown `| Field | Type | ... |`) and/or YAML code blocks.
2. For each proposed field, extract all available attributes. Required: `name`, `type`, `level`, `description`. Optional: `short`, `example`, `alpha`/`beta`, `otel`, `normalize`, `multi_fields`, `index`, `format`, `pattern`, `expected_values`, `allowed_values`.
3. **Only extract leaf fields.** If the RFC describes a namespace grouping (e.g. `entity.relationships` as a container for `entity.relationships.owns`, `entity.relationships.administers`), do **not** create an entry for the parent -- only the concrete leaf fields. The generator creates intermediate objects automatically from dotted names.
4. Infer `level: extended` when the RFC does not state the level explicitly (most new fields are `extended`).
5. Write a standalone YAML fragment under `rfcs/text/<NNNN>/<fieldset>.yml` so the RFC folder has a machine-readable artifact. Follow the fragment format of [`rfcs/text/0052/gen_ai.yaml`](../../../rfcs/text/0052/gen_ai.yaml).

### 3. Detect repeated child-field patterns — extract reusable field set

After extracting field definitions, check whether **two or more parent fields** share the **same set of typed child fields**. If N >= 2 parent fields each declare the same child field names with the same types, extract the shared children into a **new reusable field set**.

**How to create it:**

1. Choose a name for the shared structure. Follow ECS naming: lowercase, underscores, **singular**, no dashes.

2. Create `schemas/<new_fieldset>.yml` with:
   - The Apache 2.0 license header.
   - **`reusable.top_level: false`** — always.
   - `reusable.expected` listing each parent location using `at`/`as` syntax with `short_override`.
   - The shared child fields defined once under `fields:`.

3. **`at` / `as` routing rule:** `at` must resolve to an **existing field set name** — it cannot be a dotted path into a field set's internals. Place the full nesting path in `as` instead. For example, use `at: entity` + `as: relationships.owns`, **not** `at: entity.relationships` + `as: owns`. The generator creates intermediate objects automatically from the dotted `as` path — do **not** add an explicit parent object field for the intermediate namespace in the parent schema.

4. In the parent field set's schema, do **not** define the reused children inline — the `reusable.expected` entries produce them automatically.

5. Add the new field set to `schemas/subsets/main.yml` in alphabetical order with `fields: "*"`.

**Reference:** same mechanism as `risk` (reused under `host`, `user`), `geo` (reused under `source`, `destination`, etc.). See [`schemas/risk.yml`](../../../schemas/risk.yml) and [`schemas/geo.yml`](../../../schemas/geo.yml).

### 4. Determine target schema file(s)

Check `schemas/` for an existing file matching the field set name:

- **Exists** (e.g. `schemas/entity.yml`) → this is an **extension**. Read the file; note the existing field-set header and current field list.
- **Does not exist** → this is a **new field set**. You will create `schemas/<fieldset>.yml`.

### 5. Write or update `schemas/*.yml`

#### Extension of an existing field set

- Append new fields to the `fields:` list.
- Preserve alphabetical ordering of fields by `name`.
- Do **not** alter existing fields or the field-set header unless the RFC explicitly redefines them (e.g. adds `reusable` entries).
- If the RFC adds new `reusable.expected` entries, merge them into the existing `reusable` block.

#### New field set

Generate a complete file. Use the **Apache 2.0 license header** (copy the 16-line block from any existing schema, e.g. `schemas/gen_ai.yml`). Then the YAML document:

```yaml
---
- name: <fieldset>
  title: <Title Case>
  group: 2
  short: <single-line ≤120 chars>
  description: >
    <multi-paragraph description from RFC>
  type: group
  # reusable: ... (only if RFC specifies nesting)
  # alpha: / beta: ... (per target maturity)
  fields:
    - name: ...
      level: extended
      type: keyword
      description: ...
```

#### Dotted names — no explicit parent objects

**Only define leaf fields.** Use dotted `name` values for hierarchy; the generator creates intermediate objects automatically. Never add a standalone parent entry just to introduce a namespace.

Good — leaf fields only:

```yaml
    - name: relationships.owns
      type: object
      ...
    - name: relationships.administers
      type: object
      ...
```

Bad — redundant parent entry:

```yaml
    # WRONG: do not create this; the generator infers it
    - name: relationships
      type: object
      description: ...

    - name: relationships.owns
      type: object
      ...
```

**Clean up existing childless parents.** When the target schema already contains a childless `object` field that now gains leaf children from the RFC, **delete** the old parent entry. For example, if `schemas/entity.yml` already has a bare `- name: lifecycle` / `type: object` with no child fields, and the RFC adds `lifecycle.last_activity`, remove the `lifecycle` entry — the dotted leaf name makes the generator create the intermediate object. Only do this when:
1. The existing entry has `type: object` (or `flattened`), **and**
2. It has **no** existing child fields using its name as a dotted prefix, **and**
3. The RFC is now adding leaf fields under that prefix.

Real-world reference: `schemas/gen_ai.yml` defines `tool.call.id`, `tool.call.arguments`, `request.choice.count` etc. with no explicit `tool`, `tool.call`, or `request` parent entries.

#### Field-level rules (from [schemas/README.md](../../../schemas/README.md) and the [ecs-schema-standards rule](../../rules/ecs-schema-standards.mdc))

| Attribute | Rule |
|-----------|------|
| `short` | Required if `description` has multiple paragraphs. Single line, ≤120 chars. |
| `example` | Composite values (arrays, objects) must be **quoted YAML strings**. Must match `pattern` if set. |
| `alpha` / `beta` | Mutually exclusive. Use the RFC's target maturity. If the field set itself is marked, do not redundantly mark each field. |
| `otel` | Include when the RFC provides an OTel mapping. `relation` is required (`match`, `equivalent`, `related`, `conflict`, `metric`, `otlp`, `na`). |
| `normalize: [array]` | When the RFC indicates a list/multi-valued field. |
| `object` / `flattened` without children | Must be justified per RFC. See [schemas/README.md § object/flattened](../../../schemas/README.md). |

### 6. Update subset (if new field set)

If you **created** a new `schemas/<fieldset>.yml`:

1. Open [`schemas/subsets/main.yml`](../../../schemas/subsets/main.yml).
2. Add an entry in **alphabetical order** among the top-level field set names:
   ```yaml
     <fieldset>:
       fields: "*"
   ```

If extending an existing field set that already has `fields: "*"`, no change is needed.

### 7. Add CHANGELOG entry

Open [`CHANGELOG.next.md`](../../../CHANGELOG.next.md). Under **`Schema Changes` > `Added`**, insert (ordered by PR number):

```
* Add <brief description of fields/field set> from RFC <NNNN>. #<PR-number>
```

### 8. Run the build pipeline

```bash
cd /path/to/ecs
make ve          # create/update virtualenv (idempotent)
make generate    # regenerate all artifacts (runs generator.py --strict)
make test        # run unit tests
```

**If errors occur:**

- **Strict-mode violations** (e.g. `short` >120 chars, unquoted composite `example`, `example` not matching `pattern`): fix the schema YAML and re-run `make generate`.
- **Test failures**: read the error, fix the schema, re-run `make test`.
- Loop until both commands succeed cleanly.

After success, verify with `git diff --stat` that the changed files are in expected locations: `schemas/`, `generated/`, `docs/reference/`, and `CHANGELOG.next.md`.

### 9. Commit and create PR

1. Create and switch to a new branch:
   ```bash
   git checkout -b rfc-<NNNN>-implement
   ```

2. Stage and commit:
   ```bash
   git add schemas/ rfcs/text/<NNNN>/ generated/ docs/reference/ CHANGELOG.next.md schemas/subsets/
   git commit -m "$(cat <<'EOF'
   Implement RFC <NNNN>: <short title>

   Apply field definitions from RFC <NNNN> to schemas/*.yml,
   regenerate all artifacts, and add changelog entry.

   Ref: #<original-PR-number>
   EOF
   )"
   ```

3. Push and open a PR:
   ```bash
   git push -u origin HEAD
   gh pr create --title "Implement RFC <NNNN>: <short title>" --body "$(cat <<'EOF'
   ## Summary

   Applies the field definitions from RFC <NNNN> (`rfcs/text/<NNNN>-*.md`) to the
   ECS schema and regenerates all artifacts.

   - Schema changes in `schemas/<fieldset>.yml`
   - All `generated/` and `docs/reference/` artifacts rebuilt via `make`
   - Changelog entry added

   ## References

   - RFC: `rfcs/text/<NNNN>-*.md`
   - RFC PR: #<original-PR-number>

   ## Checklist

   - [x] `schemas/*.yml` updated with proposed fields
   - [x] `make generate` run and `generated/` committed
   - [x] `make test` passes
   - [x] `CHANGELOG.next.md` entry added
   - [x] `docs/reference/` regenerated and committed
   EOF
   )"
   ```

4. Return the PR URL.

## Important repo facts

- **Source of truth**: `schemas/*.yml`. Never hand-edit `generated/` or `docs/reference/ecs-*.md`.
- **Build command**: `make` (wraps `scripts/generator.py --strict`). Regenerates ES templates, Beats YAML, CSV, `ecs_flat.yml`/`ecs_nested.yml`, and reference docs.
- **CI parity**: `make check` = generate + test + `git diff` must be empty.
- **OTel mapping**: optional but encouraged. Not a merge gate.
- **License header**: every `schemas/*.yml` file must start with the 16-line Apache 2.0 block.

## Reference files

- Schema attribute reference: [schemas/README.md](../../../schemas/README.md)
- Schema standards rule: [ecs-schema-standards](../../rules/ecs-schema-standards.mdc)
- RFC process: [rfcs/PROCESS.md](../../../rfcs/PROCESS.md)
- RFC guide skill: [ecs-rfc-guide](../ecs-rfc-guide/SKILL.md)
- Example full schema: [`schemas/gen_ai.yml`](../../../schemas/gen_ai.yml), [`schemas/entity.yml`](../../../schemas/entity.yml)
- Example RFC YAML fragment: [`rfcs/text/0052/gen_ai.yaml`](../../../rfcs/text/0052/gen_ai.yaml)
- Subset file: [`schemas/subsets/main.yml`](../../../schemas/subsets/main.yml)
- Changelog: [`CHANGELOG.next.md`](../../../CHANGELOG.next.md)
- Generator entry point: [`scripts/generator.py`](../../../scripts/generator.py)
