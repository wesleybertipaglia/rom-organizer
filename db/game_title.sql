CREATE TABLE IF NOT EXISTS game_title (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id INTEGER NOT NULL,
    year INTEGER,
    title TEXT NOT NULL,
    synopsis TEXT,
    genre_id INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES system(id),
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);
