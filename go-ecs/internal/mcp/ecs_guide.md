You have access to a set of tools for exploring Elastic Common Schema (ECS). Here is how to use them effectively.

## Overview

The server loads every tagged ECS release (>= v1.12.0) from the configured ECS
repository into a single SQLite database. Every field, fieldset, and expected
event type row is tagged with the ECS `version` it came from, so all of the
tools — except `ecs_get_sql_tables` — require a `version` to disambiguate which
release of ECS to consult.

Pick one version per workflow and reuse it. Do not mix results from different
versions in the same mapping.

## Tools

- **ecs_get_sql_tables** — Returns the complete database schema with all table definitions, columns, and types. Note that `fields`, `fieldsets`, and `expected_event_types` all carry a `version` column.
- **ecs_match_fields** — Check whether field names exist in a specific ECS version. Requires `version` (e.g. `"9.3.0"`) and a list of dotted field names. Returns each annotated with whether it exists in that version, plus the ECS data type and description for matches.
- **ecs_search_fields** — Full-text search across ECS field definitions for a specific version. Requires `version` and a `query`. Plain keywords, dotted field names, or camelCase identifiers are automatically split into search tokens — e.g., `crowdstrike.fdr.ProcessTTYAttached` finds `process.tty` and related fields.
- **ecs_execute_sql_query** — Executes arbitrary read-only SQLite queries. The most powerful tool for both discovery and analytics. You MUST filter by `version` in every query that touches `fields`, `fieldsets`, `field_fieldsets`, or `expected_event_types` — otherwise you will get rows merged across every loaded ECS release.

## Discovering available versions

To see which ECS versions are loaded, run:

```sql
SELECT DISTINCT version FROM fields ORDER BY version;
```

If the user does not specify a version, ask — do not default silently. If they
name a product that pins a specific ECS release (e.g. a Fleet integration that
declares `ecs.reference: git@v9.3.0`), use that version.

## ECS Field Mapping Workflow

When reviewing whether package fields align with ECS:

1. **Choose a version** — Confirm or ask the user which ECS version to map against, then reuse it for every tool call in the workflow.
2. **Discover** — Use `ecs_search_fields` (with `version`) to find ECS fields related to a concept. For example, given a custom field like `crowdstrike.fdr.ProcessTTYAttached`, search for "process tty" or "terminal" to discover that `process.tty` exists in ECS.
3. **Match** — Use `ecs_match_fields` (with `version`) and a list of field names from a package to identify which ones already exist in ECS for that version.
4. **Recommend** — Fields that match ECS should use `external: ecs` in their field definition to inherit the upstream ECS definition and avoid drift.

## Tips

- The `fields` table has flattened dotted-path field names with resolved ECS definitions. Always scope `SELECT` statements with `WHERE version = '<version>'`.
- To join `fields` to `fieldsets` via `field_fieldsets`, filter both `fields.version` and `fieldsets.version` to the same release — rows are not cross-linked between versions.
- The docs FTS index uses porter stemming, so "authenticate" also matches "authentication".
