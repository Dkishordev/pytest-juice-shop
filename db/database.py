import sqlite3
from contextlib import contextmanager
from typing import Any

from config.settings import settings

class Database:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or settings.DB_PATH

    @contextmanager
    def _connection(self, readonly: bool = True):
        uri = f"file:{self.db_path}?mode={'ro' if readonly else 'rw'}"
        conn = sqlite3.connect(uri, uri=True)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def query(self, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
        with self._connection(readonly=True) as conn:
            cur = conn.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]

    def query_one(self, sql: str, params: tuple = ()) -> dict[str, Any] | None:
        rows = self.query(sql, params)
        return rows[0] if rows else None

    def get_user_by_email(self, email: str) -> dict[str, Any] | None:
        return self.query_one("SELECT * FROM Users WHERE email = ?", (email,))

    def list_tables(self) -> list[str]:
        rows = self.query("SELECT name FROM sqlite_master WHERE type='table'")
        return [r["name"] for r in rows]

    def get_product_by_id(self, product_id: int) -> dict[str, Any] | None:
        return self.query_one("SELECT * FROM Products WHERE id = ?", (product_id,))

    def count_feedback_containing(self, text: str) -> int:
        rows = self.query(
            "SELECT COUNT(*) as c FROM Feedbacks WHERE comment LIKE ?", (f"%{text}%",)
        )
        return rows[0]["c"] if rows else 0

    def get_baskets_for_user(self, user_id: int) -> list[dict[str, Any]]:
        return self.query("SELECT * FROM Baskets WHERE UserId = ?", (user_id,))

    def user_count(self) -> int:
        row = self.query_one("SELECT COUNT(*) as c FROM Users")
        return row["c"] if row else 0
