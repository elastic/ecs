# ECS PR Quality Review — report template

Copy and fill for every automated review run. Produce **filled GitHub-flavored Markdown** (not placeholders). Wrap each severity bucket in `<details>` for the PR comment unless the tooling posts sections separately.

````markdown
# ECS PR Quality Review (automated)

**PR:** #[N] — [title]

**Overall:** **High:** [H] | **Medium:** [M] | **Low:** [L]  
**Scope:** Focus on changed `schemas/**/*.yml` and schema-related tooling/docs in this PR — other files may be listed only if relevant.

### Summary details

Brief bullet list ([2–4] bullets):
- Highest-severity themes (e.g. “invalid type”, “collision with inventory”, “missing short”).
- Whether `make check` / strict generator would likely fail.
- One line on duplication or overlap with existing fields (or “none found”).

---

<details>
<summary>High Severity ([H] findings)</summary>

_Use `### HX — [Rule-ID]: [short title]` per finding (X numbering within this section)._

### H1 — [RULE-ID]: [Short title]

- **Field / path:** `[flat field name or field set]`  
- **File:** `[path]`  
- **Rule:** One sentence tying to ecs-pr-review quality-rules.  
- **Evidence:** Quote or paraphrase the diff / inventory line.  
- **Fix:** Concrete steps (edit keys, rename, revert generated file, etc.).

_(Repeat for each High finding.)_

_If none: **No High-severity findings.**_

</details>

<details>
<summary>Medium Severity ([M] findings)</summary>

### M1 — [RULE-ID]: [Short title]

- **Field / path:** `...`  
- **File:** `...`  
- **Rule:** ...  
- **Evidence:** ...  
- **Fix:** ...

_(Repeat.)_

_If none: **No Medium-severity findings.**_

</details>

<details>
<summary>Low Severity ([L] findings)</summary>

### L1 — [RULE-ID]: [Short title]

- **Field / path:** `...`  
- **File:** `...`  
- **Suggestion:** ...  

_(Repeat.)_

_If none: **No Low-severity findings.**_

</details>

---

### Notes for contributors

- Regenerate ECS artifacts after schema edits: **`make`** (or `make check` before push) per [CONTRIBUTING.md](../../../CONTRIBUTING.md).
- Naming and types: [ecs-guidelines](../../../docs/reference/ecs-guidelines.md), [ecs-conventions](../../../docs/reference/ecs-conventions.md), [schemas/README](../../../schemas/README.md).
- Automated review does **not** replace maintainer review or CI.

````
