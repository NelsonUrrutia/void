
from void.database.connection import Connection


class Note:

    def __enter__(self):
        """Allow `with Note() as note:`; returns this instance."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
          """Close the model when the `with` block ends, even on error."""

    def save_note(self, date_str):
        with Connection() as db:
            data = (date_str,)
            sql = """
                INSERT INTO
                    void_note(note_date)
                VALUES(?)
            """
            return db.execute(sql, data)

    def save_note_detail(self, note_id, activity_info, activity_note):
        activity_id, _ = activity_info.split("::")
        with Connection() as db:
            data = (activity_note, note_id, activity_id)
            sql = """
                INSERT INTO
                    void_note_details(notes,  void_note_id, activity_id)
                VALUES(?, ?, ?)
            """
            return db.execute(sql, data)

    NOTE_SQL = """
        SELECT
            void_note.id as "note_id",
            void_note.note_date as "note_date",
            void_note_details.id as "detail_id",
            activities.name as "activity",
            categories.name as "category",
            void_note_details.notes as "notes"
        FROM void_note
        INNER JOIN
            void_note_details
                ON void_note_details.void_note_id = void_note.id
        INNER JOIN
            activities ON activities.id = void_note_details.activity_id
        INNER JOIN
            categories ON categories.id = activities.category_id
        WHERE void_note.is_active = 1
        AND void_note_details.is_active = 1
    """

    def get_day_note(self, date_str):
        with Connection() as db:
            sql = self.NOTE_SQL + " AND void_note.note_date = ? ORDER BY categories.name, activities.name"
            return db.querying(sql, (date_str,))

    def get_notes(self):
        """Every saved note detail, newest day first."""
        with Connection() as db:
            return db.querying(self.NOTE_SQL + " ORDER BY void_note.note_date DESC, void_note_details.id")
