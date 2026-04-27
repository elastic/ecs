// Licensed to Elasticsearch B.V. under one or more agreements.
// Elasticsearch B.V. licenses this file to you under the Apache 2.0 License.
// See the LICENSE file in the project root for more information.

package store

import (
	"context"
	"strings"
)

// MatchedField is the subset of a field's metadata returned when confirming
// that a name corresponds to an ECS field.
type MatchedField struct {
	Type        string
	Description string
}

// SearchResult is a single row returned from a full-text search over ECS
// fields.
type SearchResult struct {
	Name        string `json:"name"`
	Type        string `json:"type"`
	Description string `json:"description"`
	IsArray     bool   `json:"is_array"`
}

// MatchFields looks up the given field names in the ECS catalog and returns a
// map keyed by name for those that exist. Names that do not correspond to an
// ECS field are omitted from the result.
func (q *Queries) MatchFields(ctx context.Context, version string, names []string) (map[string]MatchedField, error) {
	if len(names) == 0 {
		return nil, nil
	}

	var sb strings.Builder
	sb.WriteString("SELECT name, type, description FROM fields WHERE version = ? AND name ")
	if len(names) > 1 {
		sb.WriteString("IN (")
		sb.WriteString(strings.Repeat("?,", len(names)-1))
		sb.WriteString("?)")
	} else {
		sb.WriteString("= ?")
	}

	stmt := sb.String()
	args := make([]any, len(names)+1)
	args[0] = version
	for i, v := range names {
		args[i+1] = v
	}

	rows, err := q.db.QueryContext(ctx, stmt, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	matches := make(map[string]MatchedField)
	for rows.Next() {
		var name string
		var match MatchedField
		if err = rows.Scan(&name, &match.Type, &match.Description); err != nil {
			return nil, err
		}
		matches[name] = match
	}
	if rows.Err() != nil {
		return nil, err
	}

	return matches, nil
}

// SearchFields runs a full-text search over ECS field names and descriptions
// and returns up to limit results ordered by FTS5 rank. If limit is zero or
// negative, a default of 25 is used. The query is normalized before matching
// (dots are stripped, camelCase tokens are split, and plain terms are joined
// with OR) so that dotted field names and camelCase identifiers match as
// expected.
func (q *Queries) SearchFields(ctx context.Context, version string, query string, limit int) ([]SearchResult, error) {
	if limit <= 0 {
		limit = 25
	}

	//Normalize the query for FTS5 matching:
	//1. Sanitize (replace dots with spaces)
	//2. Split camelCase tokens (e.g. "ProcessTTYAttached" → "Process TTY Attached")
	//3. Join plain terms with OR for additive discovery ranking
	sanitized := sanitizeFTSQuery(query)
	sanitized = splitCamelCase(query)
	sanitized = implicitOR(query)

	stmt := `SELECT ef.name, ef.type, ef.description, ef.is_array
FROM fields_fts
JOIN fields ef ON ef.id = fields_fts.rowid
WHERE ef.version = ? AND fields_fts MATCH ?
ORDER BY rank
LIMIT ?`

	rows, err := q.db.QueryContext(ctx, stmt, version, sanitized, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []SearchResult
	for rows.Next() {
		var result SearchResult
		if err = rows.Scan(&result.Name, &result.Type, &result.Description, &result.IsArray); err != nil {
			return nil, err
		}
		results = append(results, result)
	}
	if rows.Err() != nil {
		return nil, err
	}

	return results, nil
}

// sanitizeFTSQuery replaces characters that cause FTS5 syntax errors
// with spaces. Dots in particular are common in field names like
// "source.nat.ip" and would otherwise cause "syntax error near '.'".
func sanitizeFTSQuery(query string) string {
	return strings.ReplaceAll(query, ".", " ")
}

// splitCamelCase splits camelCase and PascalCase tokens within a query
// into separate words. For example "ProcessTTYAttached" becomes
// "Process TTY Attached" and "sourceIP" becomes "source IP".
// Tokens that are already all-lowercase or all-uppercase are unchanged.
// Underscores are also treated as word boundaries.
func splitCamelCase(query string) string {
	tokens := strings.Fields(query)
	changed := false
	for i, tok := range tokens {
		split := splitCamelCaseToken(tok)
		if split != tok {
			tokens[i] = split
			changed = true
		}
	}
	if !changed {
		return query
	}
	return strings.Join(tokens, " ")
}

func splitCamelCaseToken(s string) string {
	// Replace underscores with spaces first.
	s = strings.ReplaceAll(s, "_", " ")
	if strings.Contains(s, " ") {
		// Recursively process each sub-token from underscore splitting.
		parts := strings.Fields(s)
		for i, p := range parts {
			parts[i] = splitCamelCaseToken(p)
		}
		return strings.Join(parts, " ")
	}

	var buf strings.Builder
	runes := []rune(s)
	for i, r := range runes {
		if i > 0 && isUpperRune(r) {
			prev := runes[i-1]
			if isLowerRune(prev) {
				// lowUpp boundary: "sourceIP" → "source IP"
				buf.WriteRune(' ')
			} else if isUpperRune(prev) && i+1 < len(runes) && isLowerRune(runes[i+1]) {
				// UPPUpp+low boundary: "TTYAttached" → "TTY Attached"
				buf.WriteRune(' ')
			}
		}
		buf.WriteRune(r)
	}
	return buf.String()
}

func isUpperRune(r rune) bool { return r >= 'A' && r <= 'Z' }
func isLowerRune(r rune) bool { return r >= 'a' && r <= 'z' }

// fts5Operators are the reserved keywords in FTS5 query syntax.
var fts5Operators = map[string]bool{
	"AND":  true,
	"OR":   true,
	"NOT":  true,
	"NEAR": true,
}

// implicitOR rewrites a plain FTS5 query so space-separated terms use OR
// instead of FTS5's default implicit AND. This makes discovery searches
// additive: fields matching more terms rank higher, but a single matching
// term is enough to return a result.
//
// Queries that already contain FTS5 operators (AND, OR, NOT, NEAR),
// phrase quotes, or prefix wildcards are returned unchanged.
func implicitOR(query string) string {
	// If the query contains FTS5 syntax characters, pass through as-is.
	if strings.ContainsAny(query, `"()*`) {
		return query
	}

	tokens := strings.Fields(query)
	for _, tok := range tokens {
		if fts5Operators[tok] {
			return query
		}
	}

	if len(tokens) <= 1 {
		return query
	}

	return strings.Join(tokens, " OR ")
}
