-- Table storing all ECS fields.
CREATE TABLE IF NOT EXISTS fields (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    version         TEXT NOT NULL,
    type            TEXT NOT NULL,
    level           TEXT NOT NULL,
    short           TEXT,
    description     TEXT,
    is_array        BOOLEAN NOT NULL,
    example         TEXT,
    search_text     TEXT NOT NULL
);

-- Table storing ECS fieldsets.
CREATE TABLE IF NOT EXISTS fieldsets (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    version      TEXT NOT NULL,
    short        TEXT,
    description  TEXT,
    top_level    BOOLEAN NOT NULL
);

-- Table storing ECS field to fieldset connections.
CREATE TABLE IF NOT EXISTS field_fieldsets (
    field_id     INTEGER NOT NULL,
    fieldset_id  INTEGER NOT NULL,
    FOREIGN KEY (field_id) REFERENCES fields(id),
    FOREIGN KEY (fieldset_id) REFERENCES fieldsets(id)
);

-- Table storing ECS field allowed values.
CREATE TABLE IF NOT EXISTS field_allowed_values (
    field_id     INTEGER NOT NULL,
    name         TEXT NOT NULL,
    description  TEXT NOT NULL,
    FOREIGN KEY (field_id) REFERENCES fields(id)
);

-- Table storing ECS expected event.category and event.type values.
CREATE TABLE IF NOT EXISTS expected_event_types (
    category TEXT NOT NULL,
    type     TEXT NOT NULL,
    version  TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS fields_fts USING fts5(
    search_text,
    content=fields,
    content_rowid=id,
    tokenize='porter unicode61'
);
