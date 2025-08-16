CREATE TABLE IF NOT EXISTS game_title (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        
    title TEXT NOT NULL,
    synopsis TEXT,
    genre_id INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);
