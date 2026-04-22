# PR Triage Report template

Copy and fill in for every triage. Replace bracketed placeholders.

```markdown
## PR Triage Report

**PR:** #[N] — [title]
**Classification:** Direct PR | Needs RFC | Needs Discussion
**Change type:** Schema Change | Tooling | Documentation | Mixed
**Scope:** Minor | Moderate | Substantial

### Summary
[One short paragraph: what changed and why it matters for routing.]

### Files changed
- **Schemas:** [list or "none"]
- **Generated:** [list or "none" — note if missing when schemas changed]
- **Tooling/scripts/tests:** [list or "none"]
- **Docs (hand-authored):** [list or "none"]
- **CI / GitHub:** [list or "none"]
- **RFCs:** [list or "none"]

### Routing decision
[Why Direct PR is OK, or why an RFC is required, or what needs maintainer input. Cite specific triggers from classification-rules.md.]

### Risk notes
- **Breaking / deprecation:** [yes/no + detail]
- **OTel / semconv:** [alignment, gaps, or N/A]
- **Scope / reuse:** [new fieldset, reuse, categorization fields, etc.]

### Completeness checklist
- [ ] PR description (all sections)
- [ ] CHANGELOG.next.md (correct section, `#NNNN`)
- [ ] `make` + committed generated outputs (if schema change)
- [ ] OTel `otel:` on new/changed semconv-related fields
- [ ] Tests / `make check` (per CONTRIBUTING)
- [ ] CLA (contributor)

### Recommended next actions
1. [For contributor or maintainers]
2. […]
```
