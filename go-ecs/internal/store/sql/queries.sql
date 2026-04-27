-- name: InsertFieldset :one
INSERT INTO
    fieldsets (name, version, short, description, top_level)
VALUES (?, ?, ?, ?, ?)
RETURNING id;

-- name: InsertField :one
INSERT INTO
    fields (name, version, type, level, short, description, is_array, example, search_text)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    RETURNING id;

-- name: InsertFieldFieldset :exec
INSERT INTO
    field_fieldsets (fieldset_id, field_id)
VALUES (?, ?);

-- name: InsertFieldAllowedValue :exec
INSERT INTO
    field_allowed_values (field_id, name, description)
VALUES (?, ?, ?);

-- name: InsertExpectedEventType :exec
INSERT INTO
    expected_event_types (category, type, version)
VALUES (?, ?, ?);
