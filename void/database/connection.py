import sqlite3
from pathlib import Path


class Connection:
    def __init__(self):
        """Connect to void.db and configure results as name-accessible rows."""
        self.db_path = Path(__file__).parent / "void.db"
        self.tables_script = Path(__file__).parent /  "init_tables.sql"
        self.test_data_script = Path(__file__).parent / "test_data.sql"

        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def __enter__(self):
        """Allow `with Connection() as db:`; returns this instance."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection when the `with` block ends, even on error."""
        self.close()

    def create_tables(self):
        """Run init_tables.sql to create the schema. Safe to call more than
        once, every statement uses IF NOT EXISTS."""
        with open(self.tables_script) as f:
            sql = f.read()
            self.cursor.executescript(sql)
            self.connection.commit()

    def load_test_data(self):
        """Run test_data.sql to populate sample rows."""
        with open(self.test_data_script) as f:
            sql = f.read()
            self.cursor.executescript(sql)
            self.connection.commit()

    def querying(self, sql, params=()):
        """Run a parameterized SELECT and return the matching rows.

        params fills any `?` placeholders in sql, keeping values out of the
        SQL string itself (avoids SQL injection).
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def execute(self, sql, params=()):
        """Run a parameterized INSERT/UPDATE/DELETE, commit, and return the
        id of the inserted row (lastrowid; meaningless for UPDATE/DELETE)."""
        self.cursor.execute(sql, params)
        self.connection.commit()
        return self.cursor.lastrowid

    def close(self):
        """Close the database connection."""
        self.connection.close()
