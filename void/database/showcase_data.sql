-- Showcase data for screenshots. Load into a fresh database:
--   rm void/database/void.db
--   sqlite3 void/database/void.db < void/database/init_tables.sql
--   sqlite3 void/database/void.db < void/database/showcase_data.sql
-- Dates are relative to today, so VOID DAY always has a filled-in note.

INSERT INTO categories (name) VALUES
    ('Deep Work'),
    ('Body'),
    ('Mind'),
    ('Craft');

INSERT INTO activities (name, category_id) VALUES
    ('Coding',        (SELECT id FROM categories WHERE name = 'Deep Work')),
    ('Writing',       (SELECT id FROM categories WHERE name = 'Deep Work')),
    ('Research',      (SELECT id FROM categories WHERE name = 'Deep Work')),
    ('Running',       (SELECT id FROM categories WHERE name = 'Body')),
    ('Lifting',       (SELECT id FROM categories WHERE name = 'Body')),
    ('Sleep 8h',      (SELECT id FROM categories WHERE name = 'Body')),
    ('Meditation',    (SELECT id FROM categories WHERE name = 'Mind')),
    ('Reading',       (SELECT id FROM categories WHERE name = 'Mind')),
    ('Journaling',    (SELECT id FROM categories WHERE name = 'Mind')),
    ('Guitar',        (SELECT id FROM categories WHERE name = 'Craft')),
    ('Photography',   (SELECT id FROM categories WHERE name = 'Craft')),
    ('Sketching',     (SELECT id FROM categories WHERE name = 'Craft'));

INSERT INTO void_note (note_date) VALUES
    (date('now', 'localtime')),
    (date('now', 'localtime', '-1 day')),
    (date('now', 'localtime', '-2 days')),
    (date('now', 'localtime', '-3 days')),
    (date('now', 'localtime', '-4 days')),
    (date('now', 'localtime', '-5 days')),
    (date('now', 'localtime', '-6 days')),
    (date('now', 'localtime', '-7 days')),
    (date('now', 'localtime', '-8 days'));

-- (days ago, activity, notes); '' becomes NULL so "No notes written." shows too
WITH entries(days_ago, activity, notes) AS (VALUES
    (0, 'Coding',      'Shipped the welcome screen, logo looks sharp'),
    (0, 'Research',    'Textual grid layouts and CSS variables'),
    (0, 'Running',     '7.2k along the river, sunrise pace'),
    (0, 'Sleep 8h',    ''),
    (0, 'Meditation',  '15 min, box breathing'),
    (0, 'Reading',     'Deep Work, ch. 3 — "Deep work is valuable"'),
    (0, 'Guitar',      'Finally nailed the Blackbird fingerpicking'),

    (1, 'Coding',      'Refactored the note queries into one SELECT'),
    (1, 'Writing',     'Drafted the README intro'),
    (1, 'Lifting',     'Deadlift 5x5, new PR'),
    (1, 'Journaling',  'Three wins, one lesson'),
    (1, 'Photography', 'Golden hour on the rooftop, 36 frames'),

    (2, 'Coding',      'Partial unique indexes for soft deletes'),
    (2, 'Running',     'Easy 5k recovery'),
    (2, 'Sleep 8h',    ''),
    (2, 'Reading',     'The Pragmatic Programmer, tracer bullets'),

    (3, 'Research',    'Offline-first apps and SQLite WAL mode'),
    (3, 'Writing',     'Blog post: why I journal in the terminal'),
    (3, 'Meditation',  '20 min, body scan'),
    (3, 'Sketching',   'Ink studies of hands'),
    (3, 'Guitar',      'Scales, 30 min'),

    (4, 'Coding',      'Activities tab: edit and suspend'),
    (4, 'Lifting',     'Push day'),
    (4, 'Journaling',  'Planned the week ahead'),

    (5, 'Running',     'Trail run, 12k, muddy and perfect'),
    (5, 'Photography', 'Street walk downtown, film camera'),
    (5, 'Reading',     'Finished Atomic Habits'),
    (5, 'Sleep 8h',    ''),

    (6, 'Coding',      'Collection view grid, 3 columns'),
    (6, 'Research',    'Color theory for terminal UIs'),
    (6, 'Meditation',  '10 min before bed'),

    (7, 'Writing',     'Outlined the VOID roadmap'),
    (7, 'Lifting',     'Squat 5x5'),
    (7, 'Guitar',      'Learned the intro to Wish You Were Here'),
    (7, 'Journaling',  'Why "Vital Offline Information Diary"'),

    (8, 'Coding',      'Day one: textual hello world'),
    (8, 'Running',     'First run in weeks, 3k'),
    (8, 'Sketching',   'Designed the VOID logo on paper')
)
INSERT INTO void_note_details (notes, void_note_id, activity_id)
SELECT
    NULLIF(entries.notes, ''),
    void_note.id,
    activities.id
FROM entries
INNER JOIN void_note
    ON void_note.note_date = date('now', 'localtime', '-' || entries.days_ago || ' days')
INNER JOIN activities
    ON activities.name = entries.activity;
