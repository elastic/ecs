# ECS PR Quality Review — quality rules

Use these rules when reviewing **schema YAML** under `schemas/**/*.yml` and related changes in a pull request. Each rule has an **ID**, **severity** (**High** / **Medium** / **Low**), and **remediation** guidance.

**Sources of truth (read before inferring):** [schemas/README.md](../../../schemas/README.md), [ecs-schema-standards.mdc](../../rules/ecs-schema-standards.mdc), [docs/reference/ecs-guidelines.md](../../../docs/reference/ecs-guidelines.md), [docs/reference/ecs-conventions.md](../../../docs/reference/ecs-conventions.md), [CONTRIBUTING.md](../../../CONTRIBUTING.md).

**Allowed field `type` values** (must match Elasticsearch mapping types used in ECS):  
`binary`, `boolean`, `keyword`, `constant_keyword`, `wildcard`, `long`, `integer`, `short`, `byte`, `double`, `float`, `half_float`, `scaled_float`, `unsigned_long`, `date`, `date_nanos`, `alias`, `object`, `flattened`, `nested`, `join`, `long_range`, `double_range`, `date_range`, `ip`, `text`, `match_only_text`, `geo_point`, `geo_shape`, `point`, `shape`.

**Allowed `level` values:** `core`, `extended` (`custom` may appear in legacy contexts; prefer `core`/`extended` for new work per repo tests and docs).

---

## 1. Types and required keys

| ID | Severity | Summary | Detection | Remediation |
|----|----------|---------|-----------|-------------|
| **TYP-H01** | High | Invalid `type` | `type` is missing or not in the allowed list above. | Set a valid ECS/ES type (see [ecs-conventions](../../../docs/reference/ecs-conventions.md) for integer/text defaults). |
| **TYP-H02** | High | Invalid `level` | `level` missing or not `core` / `extended`. | Set `level` per field role in the schema. |
| **TYP-H03** | High | Missing required field attributes | Leaf field missing `name`, `description`, `type`, or `level`. | Add all required keys per [schemas/README.md](../../../schemas/README.md). |
| **TYP-H04** | High | `alias` without `path` | `type: alias` and no `path`. | Add `path` to the canonical target field. |
| **TYP-H05** | High | `scaled_float` without `scaling_factor` | `type: scaled_float` and no `scaling_factor`. | Add `scaling_factor` (see existing fields for examples). |

---

## 2. Stability markers

| ID | Severity | Summary | Detection | Remediation |
|----|----------|---------|-----------|-------------|
| **STB-H01** | High | `alpha` and `beta` together | Same field or field set has both `alpha` and `beta`. | Remove one marker or split the change per [schemas/README.md](../../../schemas/README.md). |
| **STB-M01** | Medium | Multiline `alpha` / `beta` text | Newline inside `alpha` or `beta` string. | Use a single line (strict/cleaner expectation). |

---

## 3. Naming

| ID | Severity | Summary | Detection | Remediation |
|----|----------|---------|-----------|-------------|
| **NM-M01** | Medium | Name token shape | Leaf segment uses uppercase, spaces, or characters other than `[a-z0-9_.@]` (allow `@` only where existing convention, e.g. `@timestamp`). | Use lowercase, underscores; follow [ecs-guidelines](../../../docs/reference/ecs-guidelines.md). |
| **NM-M02** | Medium | Stuttering | Field name repeats the field-set prefix (e.g. `host.host_ip` → should be `host.ip`) or obvious repetition. | Rename to avoid stutter; document rare exceptions (e.g. `host.hostname`). |
| **NM-M03** | Medium | Dubious abbreviation | Abbreviation not in common ECS exceptions (`ip`, `os`, `geo`, `id`, `url`, `http`, `https`, `dns`, `tls`, `api`, `pid`, `uuid`, `sql`, `csv`, `as` field set name, etc.). | Prefer full words unless strongly conventional. |
| **NM-L01** | Low | Minor naming polish | Wording could align better with sibling fields (`.id` vs `.name` patterns). | Align with nearby fields in the same field set. |

---

## 4. Descriptions and `short`

| ID | Severity | Summary | Detection | Remediation |
|----|----------|---------|-----------|-------------|
| **DSC-M01** | Medium | Multi-paragraph `description` without `short` | `description` has two+ paragraphs (blank line) and no `short`. | Add a single-line `short` per [schemas/README.md](../../../schemas/README.md). |
| **DSC-M02** | Medium | `short` length / shape | `short` longer than 120 characters or contains newlines. | Trim to ≤120 chars, single line (strict mode / [ecs-schema-standards](../../rules/ecs-schema-standards.mdc)). |
| **DSC-M03** | Medium | Vague or self-referential description | Description only restates the field name with no semantics, or contradicts `type`/`example`. | Clarify meaning, units, population rules, and boundaries. |
| **DSC-L01** | Low | Long single-paragraph description | Very long description without `short` (optional clarity for UIs). | Add `short` for scanability. |

---

## 5. Examples, `pattern`, `expected_values`

| ID | Severity | Summary | Detection | Remediation |
|----|----------|---------|-----------|-------------|
| **EX-M01** | Medium | Unquoted composite `example` | `example` is YAML array or mapping (not a quoted string) where composite should be stringified for generators. | Quote as a string (see [schemas/README.md](../../../schemas/README.md)). |
| **EX-M02** | Medium | `example` vs `pattern` | `pattern` set and example string does not `re.match` the pattern. | Fix example or pattern so they agree ([`cleaner.check_example_value`](../../../scripts/schema/cleaner.py)). |
| **EX-M03** | Medium | `example` vs `expected_values` | `expected_values` list present and example not in list (after array-normalize for `normalize: array`). | Align example with a listed value or adjust `expected_values`. |
| **EX-L01** | Low | Missing `example` on new leaf | New leaf field has no `example` where one would aid implementers. | Add a realistic `example`. |

---

## 6. Structural: `object`, `flattened`, reuse

| ID | Severity | Summary | Detection | Remediation |
|----|----------|---------|-----------|-------------|
| **STR-M01** | Medium | `object` / `flattened` without children | `type` is `object` or `flattened`, no child `fields`, PR text does not justify opaque shape per [schemas/README.md](../../../schemas/README.md). | Model explicit children OR document homogeneous opaque maps (e.g. string keys/values). |
| **STR-H01** | High | Breaking reuse assumptions | Diff changes `reusable.expected`/`top_level` in ways that break established mounting or duplicates trees incorrectly. | Re-check [schemas/README.md](../../../schemas/README.md) reuse section and RFC needs. |

---

## 7. Duplication and conflicts vs inventory

The review agent receives a **`schema-inventory.tsv`** (or similar) built from **`schemas/*.yml` at the PR base**. It lists flattened field names (`agent.name`, `@timestamp`, …) and types/descriptions snippets for comparison.

| ID | Severity | Summary | Detection | Remediation |
|----|----------|---------|-----------|-------------|
| **DUP-H01** | High | Canonical name collision | New/changed flattened field path duplicates an inventory path that already refers to another distinct definition (excluding identical line from same merged entry). If PR only moves within same RFC flow, reconcile in schema. | Rename or consolidate; avoid conflicting definitions across field sets/locations. |
| **DUP-M01** | Medium | Semantic overlap | New field’s description/examples overlap an existing inventory field (`host.ip` vs new `host.ipv4`) without differentiation. | Reference existing fields, extend with clearer names, or merge concepts. |
| **DUP-M02** | Medium | Duplicate `allowed_values` / category | New `allowed_values` entry name collides or duplicates semantics of an existing entry. | Merge or rename; consider consumers of categorization docs. |

---

## 8. Generated artifacts and docs

| ID | Severity | Summary | Detection | Remediation |
|----|----------|---------|-----------|-------------|
| **GEN-H01** | High | Hand-edited generated reference | Diff touches `generated/**` or generator-only `docs/reference/ecs-*.md` without corresponding `schemas/**` (or documented generator-only reason). | Revert manual edits; run `make` / `make check` per [CONTRIBUTING.md](../../../CONTRIBUTING.md). |
| **GEN-M01** | Medium | Changelog expectation | Schema or `scripts/` change with no `CHANGELOG.next.md` update when one is expected per [ecs-pr-completeness](../../rules/ecs-pr-completeness.mdc). | Add entry with `#NNNN` when required. |

---

## 9. OpenTelemetry mappings

| ID | Severity | Summary | Detection | Remediation |
|----|----------|---------|-----------|-------------|
| **OTL-M01** | Medium | Likely semconv alignment missing | Field clearly parallels a well-known OTel attribute (naming/type) and has no `otel:` block; optional but recommended in [CONTRIBUTING.md](../../../CONTRIBUTING.md). | Add `otel:` with correct `relation` or `relation: na` with justification if intentionally unmapped. |

---

## 10. Severity guidelines for the agent

- **High:** Breaks schema contract, will or should fail generator/tests, illegal attributes, dangerous collisions, or edits generated-only outputs incorrectly.
- **Medium:** Violates ECS conventions, strict cleaner rules, unclear docs, likely maintainer pushback.
- **Low:** Polish, optional examples, stylistic consistency, non-blocking suggestions.

When uncertain between two severities, prefer the **higher** one in the checklist and explain why in one sentence.
