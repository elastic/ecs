# ecs-mcp

A [Model Context Protocol](https://modelcontextprotocol.io/) server that exposes the
[Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current/index.html) to
LLM-powered tools. It loads every tagged ECS release into a local SQLite database and
serves tools for searching, matching, and querying the schema at a specific version —
so agents can reliably align vendor or custom fields with ECS without hallucinating
field names.

## Features

- **All tagged ECS releases in one database** — reads every tag (>= v1.12.0) from a
  local checkout of `elastic/ecs` and loads each release into a single SQLite database
  with a full-text search index over field names and descriptions. Tool callers select
  which version to query at call time.
- **MCP tools for exploration** — inspect the database schema, run ad-hoc SQL, check
  whether a list of field names exists in a given ECS version, or full-text search
  field definitions for that version.
- **MCP prompt: `ecs_guide`** — a ready-to-use guide that primes the model on how to
  combine the tools effectively, including how to select a version.
- **Flexible transports** — runs over stdio (for local MCP clients) or streamable HTTP
  with optional TLS (for shared deployments).

## Installation

### Build from source

Requires Go 1.26 or later.

```sh
git clone https://github.com/elastic/ecs
cd ecs
make ecs-mcp
```

The resulting `ecs-mcp` binary is self-contained.

### Running the server

On startup the server reads all tagged ECS releases from the local checkout at
`-dir` (cloned on first run if the path does not yet exist) and loads each one
into the database. The server then runs over stdio by default:

```sh
./ecs-mcp -dir /path/to/ecs
```

`-dir` is required.

Useful flags (also settable via environment variable):

| Flag        | Env                 | Description                                                                                                 |
|-------------|---------------------|-------------------------------------------------------------------------------------------------------------|
| `-dir`      | `ECS_MCP_DIR`       | Path to a local checkout of `elastic/ecs`. Cloned on if it does not exist. **Required.**                    |
| `-db`       | —                   | Path to a SQLite file to persist the loaded schema. When omitted, a temp DB is created and removed on exit. |
| `-listen`   | `ECS_MCP_LISTEN`    | Run an HTTP server on this address (e.g. `localhost:8443`) instead of stdio.                                |
| `-cert`     | `ECS_MCP_CERT_FILE` | TLS certificate for HTTP mode. Default `cert.pem`.                                                          |
| `-key`      | `ECS_MCP_KEY_FILE`  | TLS key for HTTP mode. Default `key.pem`.                                                                   |
| `-insecure` | `ECS_MCP_INSECURE`  | Disable TLS in HTTP mode.                                                                                   |
| `-debug`    | `ECS_MCP_DEBUG`     | Enable debug logging.                                                                                       |
| `-version`  | —                   | Print version information and exit.                                                                         |

## MCP server setup

### Claude / Claude Code

Add an entry to your MCP client config (`claude_desktop_config.json` for the desktop app,
`~/.claude.json` or a project `.mcp.json` for Claude Code):

```json
{
  "mcpServers": {
    "ecs": {
      "command": "/absolute/path/to/ecs-mcp",
      "args": ["-dir", "/absolute/path/to/ecs"]
    }
  }
}
```

Or from the Claude Code CLI:

```sh
claude mcp add ecs /absolute/path/to/ecs-mcp -- -dir /absolute/path/to/ecs
```

Restart the client and confirm the `ecs` server is connected. The `ecs_guide` prompt and
`ecs_*` tools should be available.

### Cursor

Add the server to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "ecs": {
      "command": "/absolute/path/to/ecs-mcp",
      "args": ["-dir", "/absolute/path/to/ecs"]
    }
  }
}
```

Reload Cursor and verify the server shows as connected under Settings → MCP.

### HTTP transport

To share one instance across multiple clients, run with `-listen`:

```sh
./ecs-mcp -listen :8443 -cert cert.pem -key key.pem
# or, run without HTTPS:
./ecs-mcp -listen :8080 -insecure
```

Then point clients that support streamable HTTP MCP at `https://host:8443/`.

## MCP tools

Every tool that returns field data requires an ECS `version` argument (e.g.
`"9.3.0"`), since the database holds every tagged release. To list the versions
that are loaded, run `SELECT DISTINCT version FROM fields ORDER BY version;`
via `ecs_execute_sql_query`.

| Tool | Arguments | Purpose |
|---|---|---|
| `ecs_get_sql_tables` | — | Returns the full DDL for the loaded ECS database — the catalog of tables, columns, and types. Call this first so subsequent queries target real columns. |
| `ecs_execute_sql_query` | `statement` | Executes an arbitrary read-only SQLite query against the ECS database. Useful for targeted lookups, fieldset membership checks, filtering by `level`, etc. Queries against `fields`/`fieldsets`/`expected_event_types` should filter by `version`, otherwise rows from every loaded release are merged. |
| `ecs_match_fields` | `version`, `field_names` | Given up to 500 dotted field names and an ECS `version`, returns each annotated with whether it exists in that version of ECS, plus the ECS type and description for matches. Ideal for bulk alignment checks. |
| `ecs_search_fields` | `version`, `query`, optional `limit` | Full-text search across ECS field names and descriptions for the given `version`. Accepts plain keywords, dotted paths, or camelCase identifiers — `crowdstrike.fdr.ProcessTTYAttached` is tokenized automatically and surfaces `process.tty`-family fields. |

In addition, the server registers the `ecs_guide` prompt, which returns a short
walkthrough of how to combine the tools when mapping fields to ECS, including
how to select a version.
