// Licensed to Elasticsearch B.V. under one or more agreements.
// Elasticsearch B.V. licenses this file to you under the Apache 2.0 License.
// See the LICENSE file in the project root for more information.

package store

import (
	"context"
	"database/sql"
	"fmt"
	"log/slog"
	"os"
	"strings"

	"github.com/elastic/ecs/go-ecs/internal/field"

	_ "embed"
)

//go:generate sqlc generate -f sql/sqlc.yml

//go:embed sql/schema.sql
var DDL string

const batchSize = 10000

// NewDB creates a fresh SQLite database at dbFile (removing any existing file),
// populates it with the given ECS schema, and returns a read-only handle.
func NewDB(ctx context.Context, dbFile string, schemas []*field.Schema) (*sql.DB, error) {
	// Remove existing DB if it exists. Create a new DB.
	datasource := fmt.Sprintf("file:%s", dbFile)
	if err := os.Remove(dbFile); err != nil && !os.IsNotExist(err) {
		return nil, fmt.Errorf("failed to remove existing DB: %w", err)
	}
	db, err := sql.Open("sqlite", datasource)
	if err != nil {
		return nil, fmt.Errorf("failed to open new DB: %w", err)
	}

	// Create tables.
	if _, err = db.ExecContext(ctx, DDL); err != nil {
		db.Close()
		return nil, fmt.Errorf("failed to create tables: %w", err)
	}

	// Write to DB.
	slog.Info("Adding schemas to database")

	for _, schema := range schemas {
		slog.Debug("Adding schema to database", slog.String("version", schema.Version), slog.Int("fieldsets", len(schema.Fieldsets)), slog.Int("fields", len(schema.Fields)))

		fieldsetIDs := make(map[string]int64, len(schema.Fieldsets))

		if err = runBatchedTransaction(ctx, db, schema.Fieldsets, func(ctx context.Context, q *Queries, fs *field.Fieldset) error {
			fieldsetIDs[fs.Name], err = q.InsertFieldset(ctx, InsertFieldsetParams{
				Name:        fs.Name,
				Version:     schema.Version,
				Short:       nullString(fs.Short),
				Description: nullString(fs.Description),
				TopLevel:    fs.TopLevel,
			})

			return err
		}); err != nil {
			return nil, err
		}

		if err = runBatchedTransaction(ctx, db, schema.Fields, func(ctx context.Context, q *Queries, v *field.Field) error {
			searchText := strings.ReplaceAll(v.Name, ".", " ") + " " + v.Description

			insertParams := InsertFieldParams{
				Name:        v.Name,
				Version:     schema.Version,
				Type:        v.Type,
				Level:       v.Level,
				Short:       nullString(v.Short),
				Description: nullString(v.Description),
				IsArray:     v.IsArray,
				Example:     nullString(v.Example),
				SearchText:  searchText,
			}

			var id int64
			if id, err = q.InsertField(ctx, insertParams); err != nil {
				slog.Error("Failed to insert field", slog.String("version", schema.Version), slog.String("field", v.Name), slog.String("error", err.Error()))
				return err
			}

			for _, fs := range v.Fieldsets {
				if err = q.InsertFieldFieldset(ctx, InsertFieldFieldsetParams{
					FieldsetID: fieldsetIDs[fs.Name],
					FieldID:    id,
				}); err != nil {
					slog.Error("Failed to insert field fieldset reference", slog.String("version", schema.Version), slog.String("field", v.Name), slog.String("error", err.Error()))
					return err
				}
			}
			for _, av := range v.AllowedValues {
				if err = q.InsertFieldAllowedValue(ctx, InsertFieldAllowedValueParams{
					FieldID:     id,
					Name:        av.Name,
					Description: av.Description,
				}); err != nil {
					slog.Error("Failed to insert field allowed value", slog.String("version", schema.Version), slog.String("field", v.Name), slog.String("error", err.Error()))
					return err
				}
			}

			return nil
		}); err != nil {
			return nil, err
		}

		if err = runBatchedTransaction(ctx, db, schema.ExpectedEventTypes, func(ctx context.Context, q *Queries, v *field.ExpectedEventType) error {
			for _, vv := range v.Types {
				if err = q.InsertExpectedEventType(ctx, InsertExpectedEventTypeParams{
					Category: v.Category,
					Type:     vv,
					Version:  schema.Version,
				}); err != nil {
					slog.Error("Failed to insert field allowed value", slog.String("version", schema.Version), slog.String("category", v.Category), slog.String("type", vv), slog.String("error", err.Error()))
					return err
				}
			}

			return nil
		}); err != nil {
			return nil, err
		}

	}

	if _, err = db.ExecContext(ctx, `INSERT INTO fields_fts(fields_fts) VALUES('rebuild')`); err != nil {
		db.Close()
		return nil, fmt.Errorf("rebuilding ECS fields FTS: %w", err)
	}

	db.Close()

	slog.Info("Initialized database")

	// Open DB as read-only.
	datasource = fmt.Sprintf("file:%s?mode=ro", dbFile)
	db, err = sql.Open("sqlite", datasource)
	if err != nil {
		return nil, fmt.Errorf("failed to open read-only DB: %w", err)
	}

	return db, nil
}

// nullString converts a string to a sql.NullString. A string is null if it is empty.
func nullString(s string) sql.NullString {
	if s == "" {
		return sql.NullString{}
	}

	return sql.NullString{String: s, Valid: true}
}

func runTransaction(ctx context.Context, db *sql.DB, fn func(context.Context, *Queries) error) error {
	q := Queries{db: db}

	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %w", err)
	}

	qtx := q.WithTx(tx)

	if err = fn(ctx, qtx); err != nil {
		_ = tx.Rollback()
		return err
	}

	return tx.Commit()
}

func runBatchedTransaction[V any](ctx context.Context, db *sql.DB, items []V, fn func(ctx context.Context, q *Queries, item V) error) error {
	var i int
	for i < len(items) {
		if err := runTransaction(ctx, db, func(ctx context.Context, queries *Queries) error {
			for bi := 0; bi < batchSize && i < len(items); bi++ {
				if err := fn(ctx, queries, items[i]); err != nil {
					return err
				}
				i++
			}

			return nil
		}); err != nil {
			return err
		}
	}

	return nil
}
