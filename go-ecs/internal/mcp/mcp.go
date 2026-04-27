// Licensed to Elasticsearch B.V. under one or more agreements.
// Elasticsearch B.V. licenses this file to you under the Apache 2.0 License.
// See the LICENSE file in the project root for more information.

package mcp

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log/slog"

	"github.com/modelcontextprotocol/go-sdk/mcp"

	"github.com/elastic/ecs/go-ecs/internal/store"

	_ "embed"
)

//go:embed ecs_guide.md
var guidePromptText string

const (
	defaultFTSLimit    = 25
	maxMatchFieldNames = 500
)

type execQueryArgs struct {
	Statement string `json:"statement" jsonschema:"SQLite query to execute"`
}

type matchFieldsArgs struct {
	FieldNames []string `json:"field_names" jsonschema:"List of dotted field names to check against ECS (max 500)"`
	Version    string   `json:"version" jsonschema:"The ECS version"`
}

type searchFieldsArgs struct {
	Query   string `json:"query" jsonschema:"Search query - plain keywords, dotted field names, or camelCase identifiers (e.g. process terminal, crowdstrike.fdr.ProcessTTYAttached, \"source address\", network AND bytes)"`
	Version string `json:"version" jsonschema:"The ECS version"`
	Limit   int    `json:"limit,omitempty" jsonschema:"Maximum number of results to return (default 25)"`
}

type tools struct {
	ddl string
	db  *sql.DB
}

func (t *tools) getSQLSchema(_ context.Context, _ *mcp.CallToolRequest, _ any) (*mcp.CallToolResult, any, error) {
	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{Text: t.ddl},
		},
	}, nil, nil
}

func (t *tools) executeQuery(ctx context.Context, _ *mcp.CallToolRequest, args execQueryArgs) (*mcp.CallToolResult, any, error) {
	slog.InfoContext(ctx, "Executing query", slog.String("statement", args.Statement))

	rows, err := t.db.QueryContext(ctx, args.Statement)
	if err != nil {
		slog.ErrorContext(ctx, "Error executing query", slog.String("statement", args.Statement), slog.String("error", err.Error()))
		return mcpErrorf("failed to execute query: %v", err), nil, nil
	}
	defer rows.Close()

	columns, err := rows.Columns()
	if err != nil {
		slog.ErrorContext(ctx, "Error getting columns", slog.String("error", err.Error()))
		return mcpErrorf("failed to get columns: %v", err), nil, nil
	}

	var result []map[string]any
	for rows.Next() {
		values := make([]any, len(columns))
		pointers := make([]any, len(columns))
		for i := range values {
			pointers[i] = &values[i]
		}

		if err = rows.Scan(pointers...); err != nil {
			slog.ErrorContext(ctx, "Error scanning row", slog.String("error", err.Error()))
			return mcpErrorf("failed to scan row: %v", err), nil, nil
		}

		row := make(map[string]any)
		for i, column := range columns {
			val := values[i]
			if b, ok := val.([]byte); ok {
				row[column] = string(b)
			} else {
				row[column] = val
			}
		}
		result = append(result, row)
	}

	jsonRows, err := json.Marshal(result)
	if err != nil {
		slog.ErrorContext(ctx, "Error marshaling results", slog.String("error", err.Error()))
		return mcpErrorf("failed to marshal result: %v", err), nil, nil
	}

	slog.InfoContext(ctx, "Query executed successfully", slog.Int("row_count", len(result)))
	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{Text: string(jsonRows)},
		},
	}, nil, nil
}

func (t *tools) matchFields(ctx context.Context, _ *mcp.CallToolRequest, args matchFieldsArgs) (*mcp.CallToolResult, any, error) {
	if len(args.FieldNames) == 0 {
		return mcpErrorf("field_names must not be empty"), nil, nil
	}
	if len(args.FieldNames) > maxMatchFieldNames {
		return mcpErrorf("field_names exceeds maximum of %d", maxMatchFieldNames), nil, nil
	}

	q := store.New(t.db)
	matched, err := q.MatchFields(ctx, args.Version, args.FieldNames)
	if err != nil {
		return mcpErrorf("failed to match fields: %v", err), nil, nil
	}

	type result struct {
		Name        string `json:"name"`
		IsECS       bool   `json:"is_ecs"`
		Type        string `json:"type"`
		Description string `json:"description"`
	}
	results := make([]result, len(args.FieldNames))
	for i, name := range args.FieldNames {
		if m, ok := matched[name]; ok {
			results[i] = result{Name: name, IsECS: true, Type: m.Type, Description: m.Description}
		} else {
			results[i] = result{Name: name}
		}
	}

	jsonData, err := json.Marshal(results)
	if err != nil {
		return mcpErrorf("failed to marshal results: %v", err), nil, nil
	}

	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{Text: string(jsonData)},
		},
	}, nil, nil
}

func (t *tools) searchFields(ctx context.Context, _ *mcp.CallToolRequest, args searchFieldsArgs) (*mcp.CallToolResult, any, error) {
	limit := args.Limit
	if limit <= 0 {
		limit = defaultFTSLimit
	}

	q := store.New(t.db)
	matched, err := q.SearchFields(ctx, args.Version, args.Query, limit)
	if err != nil {
		return mcpErrorf("failed to search fields: %v", err), nil, nil
	}

	jsonData, err := json.Marshal(matched)
	if err != nil {
		return mcpErrorf("failed to marshal results: %v", err), nil, nil
	}

	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{Text: string(jsonData)},
		},
	}, nil, nil
}

// AddTools registers the ECS MCP tools on the server.
func AddTools(s *mcp.Server, ddl string, db *sql.DB) {
	t := &tools{
		ddl: ddl,
		db:  db,
	}

	mcp.AddTool(s, &mcp.Tool{
		Annotations: &mcp.ToolAnnotations{
			ReadOnlyHint: true,
		},
		Description: "Call this tool first. Returns the complete catalog of available tables and columns",
		Name:        "ecs_get_sql_tables",
		Title:       "Get ECS SQL tables",
	}, t.getSQLSchema)

	mcp.AddTool(s, &mcp.Tool{
		Annotations: &mcp.ToolAnnotations{
			ReadOnlyHint: true,
		},
		Description: "Call this tool to execute an arbitrary SQLite query. Be sure you have called ecs_get_sql_tables() first to understand the structure of the data.",
		Name:        "ecs_execute_sql_query",
		Title:       "Execute SQL query",
	}, t.executeQuery)

	mcp.AddTool(s, &mcp.Tool{
		Annotations: &mcp.ToolAnnotations{
			ReadOnlyHint: true,
		},
		Description: "Check whether field names exist in ECS (Elastic Common Schema).",
		Name:        "ecs_match_fields",
		Title:       "Match ECS fields",
	}, t.matchFields)

	mcp.AddTool(s, &mcp.Tool{
		Annotations: &mcp.ToolAnnotations{
			ReadOnlyHint: true,
		},
		Description: "Full-text search across ECS (Elastic Common Schema) field definitions.",
		Name:        "ecs_search_fields",
		Title:       "Search ECS fields",
	}, t.searchFields)
}

// AddPrompts registers all MCP prompts on the server.
func AddPrompts(s *mcp.Server) {
	s.AddPrompt(&mcp.Prompt{
		Name:        "ecs_guide",
		Title:       "ECS Guide",
		Description: "How to use the ecs tools together to explore Elastic Common Schema (ECS).",
	}, guidePromptHandler)
}

func guidePromptHandler(_ context.Context, _ *mcp.GetPromptRequest) (*mcp.GetPromptResult, error) {
	return &mcp.GetPromptResult{
		Description: "Guide for using the ecs MCP tools",
		Messages: []*mcp.PromptMessage{
			{
				Role:    "user",
				Content: &mcp.TextContent{Text: guidePromptText},
			},
		},
	}, nil
}

func mcpErrorf(format string, args ...any) *mcp.CallToolResult {
	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{
				Text: fmt.Sprintf("ERROR: "+format, args...),
			},
		},
	}
}
