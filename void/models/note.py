
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
