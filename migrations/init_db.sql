-- migrations/init_db.sql
CREATE TABLE IF NOT EXISTS Files (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Tags (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    file_id INTEGER,
    FOREIGN KEY (file_id) REFERENCES Files(id)
);

CREATE TABLE IF NOT EXISTS Attributes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    tag_id INTEGER,
    FOREIGN KEY (tag_id) REFERENCES Tags(id)
);

-- Создаем индекс для ускорения поиска по имени тега
CREATE INDEX idx_tag_name ON Tags (name);