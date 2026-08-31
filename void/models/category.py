from void.database.connection import Connection


class Category:

    def __enter__(self):
        """Allow `with Category() as category:`; returns this instance."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
          """Close the model when the `with` block ends, even on error."""

    def get_active_categories_for_activities(self):
        with Connection() as db:
            sql = """
                SELECT
                    categories.id as "id",
                    categories.name as "category"
                FROM categories
                WHERE categories.is_active = 1
            """
            result = db.querying(sql)
            return result
