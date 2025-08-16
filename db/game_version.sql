CREATE TABLE IF NOT EXISTS game_version (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    signature TEXT UNIQUE NOT NULL,
    region_id INTEGER,
    languages TEXT,
    type TEXT,
    title TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (region_id) REFERENCES region(id)
);
