# ECS PR classification — decision rules

Use after inspecting the diff (files touched, approximate size, semantics). See [rfcs/README.md](../../../rfcs/README.md) and [CONTRIBUTING.md](../../../CONTRIBUTING.md) for project wording.

## 1. RFC required (any match → **Needs RFC**)

| Trigger | Examples / notes |
|--------|-------------------|
| New top-level field set | New `schemas/<name>.yml` (new `name:` at field-set level) |
| Breaking change | Removing fields; changing `type`; narrowing/breaking semantics; moving fields; `extended` → `core` promotions; incompatible `allowed_values` / categorization |
| New reuse topology | New `reusable.expected` entries that introduce nesting in new places (e.g. new `{at, as}` role) |
| Novel / unaddressed use case | Domain or signal type not clearly covered by existing field sets; “we need a place for X” without an obvious existing home |
| ECS-wide scope | Changes to core taxonomy (`event.*` categorization), compliance story, or conventions affecting most integrations |
| Large batch | Rough heuristic: **> ~5** new leaf fields in one PR (especially across concepts) — treat as substantial unless clearly trivial changes |

## 2. Direct PR OK (typically **Direct PR**)

All should be low controversy and incremental:

| Pattern | Examples |
|---------|----------|
| Bugfix / clarity | Typos, wrong examples, description fixes, strict-mode fixes (`short`, quoted examples) |
| Small additive extension | 1–2 new fields in an **existing** field set that mirror established patterns (e.g. new OTel-aligned attribute in `gen_ai.*`) |
| Tooling only | `scripts/`, generator templates, tests, Makefile |
| Non-generated docs | `docs/` that are not generator output (verify path); README, CONTRIBUTING cross-links |
| Changelog / version housekeeping | `CHANGELOG.next.md`, release-note scaffolding (if consistent with repo practice) |
| Release process | Version bumps (`version` file), moving/updating release notes, updating `docs/` release notes, `CHANGELOG` rotation — standard release mechanics |
| CI / automation | `.github/workflows/` (non-breaking) |

**Caveat:** If a “small” addition introduces **new** semantics (new tool protocol, new entity type), escalate to **Needs RFC** or **Needs Discussion**.

## 3. Needs discussion (maintainer judgment)

Use when not clearly 1 or 2:

| Situation | Why ambiguous |
|-----------|-----------------|
| **3–5** new fields in one field set | May be one coherent extension or may need design review |
| New `allowed_values` on `event.category`, `event.type`, `event.kind`, etc. | Affects categorization and many consumers |
| Maturity changes | Field set or field `alpha`/`beta` ↔ GA promotions |
| `object` / `flattened` without children | Requires justification per [schemas/README.md](../../../schemas/README.md) |
| Deprecation only | May still need communication / version strategy |

## 4. Change type labels

- **Schema Change:** any `schemas/*.yml` or RFC YAML intended for schema.
- **Tooling:** `scripts/`, `Makefile`, generator tests, templates under `scripts/templates/`.
- **Documentation:** `docs/` (exclude generated field reference if policy is generator-only — flag direct edits to generated files as errors).
- **Mixed:** combinations of the above.

## 5. Historical RFCs (orientation only)

Many files under `rfcs/text/` predate the single **Proposal** stage; use them as examples of depth (fields, source data, concerns), not as stage labels. Prefer [rfcs/PROCESS.md](../../../rfcs/PROCESS.md) for current process.
