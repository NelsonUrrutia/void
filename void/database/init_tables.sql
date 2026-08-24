PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    date_created TEXT DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_categories_name
    ON categories(name) WHERE is_active = 1;

CREATE TABLE IF NOT EXISTS void_note(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_date TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    date_created TEXT DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_void_note_note_date
    ON void_note(note_date) WHERE is_active = 1;

CREATE TABLE IF NOT EXISTS activities(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  is_active INTEGER DEFAULT 1,
  date_created TEXT DEFAULT (datetime('now')),
  category_id INTEGER NOT NULL,
  FOREIGN KEY (category_id)
    REFERENCES categories (id)
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_activities_name_category
    ON activities(name, category_id) WHERE is_active = 1;

CREATE TABLE IF NOT EXISTS void_note_details (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  notes TEXT,
  is_active INTEGER DEFAULT 1,
  date_created TEXT DEFAULT (datetime('now')),
  void_note_id INTEGER NOT NULL,
  activity_id INTEGER NOT NULL,
    FOREIGN KEY (void_note_id)
    REFERENCES void_note (id),
    FOREIGN KEY (activity_id)
    REFERENCES activities(id)
);
