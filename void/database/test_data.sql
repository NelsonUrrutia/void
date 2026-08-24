-- Seed data for manual/dev testing. Run after queries.sql:
--   sqlite3 void/database/void.db < void/database/queries.sql
--   sqlite3 void/database/void.db < void/database/test_data.sql

INSERT INTO categories (name) VALUES
    ('Work'),
    ('Health'),
    ('Hobbies');

-- one hidden category, to exercise the partial unique index (name free for reuse)
INSERT INTO categories (name, is_active) VALUES ('Old Category', 0);
INSERT INTO categories (name) VALUES ('Old Category');

INSERT INTO activities (name, category_id) VALUES
    ('Coding',    (SELECT id FROM categories WHERE name = 'Work')),
    ('Meeting',   (SELECT id FROM categories WHERE name = 'Work')),
    ('Exercise',  (SELECT id FROM categories WHERE name = 'Health')),
    ('Sleep',     (SELECT id FROM categories WHERE name = 'Health')),
    ('Reading',   (SELECT id FROM categories WHERE name = 'Hobbies')),
    -- same activity name as Work's, but under a different category: allowed
    ('Meeting',   (SELECT id FROM categories WHERE name = 'Hobbies'));

INSERT INTO void_note (note_date) VALUES
    ('2026-08-23'),
    ('2026-08-24');

INSERT INTO void_note_details (notes, void_note_id, activity_id) VALUES
    ('Fixed the queries.sql schema bugs',
        (SELECT id FROM void_note WHERE note_date = '2026-08-23'),
        (SELECT id FROM activities WHERE name = 'Coding' AND category_id = (SELECT id FROM categories WHERE name = 'Work'))),
    ('Sprint planning',
        (SELECT id FROM void_note WHERE note_date = '2026-08-23'),
        (SELECT id FROM activities WHERE name = 'Meeting' AND category_id = (SELECT id FROM categories WHERE name = 'Work'))),
    ('Morning run, 5k',
        (SELECT id FROM void_note WHERE note_date = '2026-08-23'),
        (SELECT id FROM activities WHERE name = 'Exercise' AND category_id = (SELECT id FROM categories WHERE name = 'Health'))),
    -- second Coding entry same day/activity, proving duplicates are allowed
    ('More coding after dinner',
        (SELECT id FROM void_note WHERE note_date = '2026-08-23'),
        (SELECT id FROM activities WHERE name = 'Coding' AND category_id = (SELECT id FROM categories WHERE name = 'Work'))),
    ('Finished chapter 4 of a book',
        (SELECT id FROM void_note WHERE note_date = '2026-08-24'),
        (SELECT id FROM activities WHERE name = 'Reading' AND category_id = (SELECT id FROM categories WHERE name = 'Hobbies')));
