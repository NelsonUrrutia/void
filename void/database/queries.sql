-- Select active categories
SELECT * FROM categories WHERE is_active == 1;

-- Select active activities
SELECT * FROM activities WHERE is_active == 1;

-- Select active activities and their categories
SELECT
    activities.id as "ID",
    activities.name as "ACTIVITY",
    categories.name as "CATEGORY"
FROM activities
INNER JOIN
    categories on categories.id = activities.category_id
WHERE activities.is_active == 1
AND
    categories.is_active == 1;

-- Select void notes with it details
SELECT
    activities.name as "Activity",
    void_note.note_date as "Note Date",
    void_note_details.notes as "Notes"
FROM void_note_details
INNER JOIN
    void_note ON void_note.id = void_note_details.void_note_id
INNER JOIN
    activities ON activities.id = void_note_details.activity_id;

-- Select a void note with details
    SELECT
         activities.name as "Activity",
        void_note.note_date as "Note Date",
        void_note_details.notes as "Notes"
    FROM void_note_details
    INNER JOIN
        void_note ON void_note.id = void_note_details.void_note_id
    INNER JOIN
        activities ON activities.id = void_note_details.activity_id
        WHERE
        void_note.id = 1
        ;

-- Select the void note of a given day with its details and activity name
SELECT
    void_note.id as "Note ID",
    void_note.note_date as "Note Date",
    void_note_details.id as "Detail ID",
    activities.name as "Activity",
    void_note_details.notes as "Notes"
FROM void_note
INNER JOIN
    void_note_details ON void_note_details.void_note_id = void_note.id
INNER JOIN
    activities ON activities.id = void_note_details.activity_id
WHERE void_note.note_date = date('now', 'localtime')  -- or ? to pass any day
AND void_note.is_active = 1
AND void_note_details.is_active = 1;
