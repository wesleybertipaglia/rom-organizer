CREATE TABLE IF NOT EXISTS game_version (
    id INTEGER PRIMARY KEY AUTOINCREMENT,    
    signature TEXT UNIQUE NOT NULL,
    game_id INTEGER NOT NULL,
    system_id INTEGER NOT NULL,
    region_id INTEGER,
    year INTEGER,
    languages TEXT,
    type TEXT,
    title TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (system_id) REFERENCES system(id),
    FOREIGN KEY (region_id) REFERENCES region(id)
);
