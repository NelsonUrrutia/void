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

    def create_activity(self, activity, category_id):
        with Connection() as db:
            data = (activity, category_id)
            sql = "INSERT INTO activities (name, category_id) VALUES(?, ?)"
            db.execute(sql, data)
