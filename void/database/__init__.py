"""Database module """

from void.database.connection import DB_PATH, Connection


def initialize_database():
    """Create void.db and its schema the first time the app runs.

    Does nothing once void.db already exists, so it's safe to call on
    every startup.
    """
    if DB_PATH.exists():
        return

    with Connection() as db:
        db.create_tables()
