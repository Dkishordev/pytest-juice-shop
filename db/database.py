import sqlite3
from contextlib import contextmanager

from config.settings import settings


class Database:

    def __init__(self, db_path=None):
        self.db_path = db_path or settings.DB_PATH

    @contextmanager
    def connection(self, readonly=True):
        mode = "ro" if readonly else "rw"
        database = f"file:{self.db_path}?mode={mode}"

        conn = sqlite3.connect(database, uri=True)
        conn.row_factory = sqlite3.Row

        try:
            yield conn
        finally:
            conn.close()

    def query(self, sql, params=()):
        with self.connection() as conn:
            result = conn.execute(sql, params)
            rows = result.fetchall()

            return [dict(row) for row in rows]

    def query_one(self, sql, params=()):
        rows = self.query(sql, params)

        if rows:
            return rows[0]

        return None

    def get_user_by_email(self, email):
        sql = "SELECT * FROM Users WHERE email = ?"
        return self.query_one(sql, (email,))

    def list_tables(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        rows = self.query(sql)

        return [row["name"] for row in rows]

    def get_product_by_id(self, product_id):
        sql = "SELECT * FROM Products WHERE id = ?"
        return self.query_one(sql, (product_id,))

    def count_feedback_containing(self, text):
        sql = "SELECT COUNT(*) as c FROM Feedbacks WHERE comment LIKE ?"

        rows = self.query(sql, (f"%{text}%",))
        if rows:
            return rows[0]["c"]

        return 0

    def get_baskets_for_user(self, user_id):
        sql = "SELECT * FROM Baskets WHERE UserId = ?"
        return self.query(sql, (user_id,))

    def user_count(self):
        sql = "SELECT COUNT(*) as c FROM Users"

        row = self.query_one(sql)

        if row:
            return row["c"]

        return 0
