from void.database.connection import Connection

class Activity:

    def __enter__(self):
        """Allow `with Activity() as activity:`; returns this instance."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the model when the `with` block ends, even on error."""

    def get_active_activities(self):
        with Connection() as db:
            sql = """
                SELECT
                    activities.id as "id",
                    activities.name as "activity",
                    categories.name as "category"
                FROM activities
                INNER JOIN
                    categories on categories.id = activities.category_id
                WHERE activities.is_active == 1
                AND
                    categories.is_active == 1;"""
            result = db.querying(sql)
            return result
