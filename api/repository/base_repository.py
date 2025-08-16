from datetime import datetime
import sqlite3

class BaseRepository:
    table_name = None

    def __init__(self, db_path='library.db'):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _get_now(self):
        return datetime.utcnow().isoformat()

    def list_all(self):
        with self._get_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM {self.table_name}")
            return cursor.fetchall()

    def get_by_id(self, id_):
        with self._get_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (id_,))
            return cursor.fetchone()

    def create(self, **kwargs):
        now = self._get_now()
        if 'created_at' not in kwargs:
            kwargs['created_at'] = now
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = now

        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?'] * len(kwargs))
        values = tuple(kwargs.values())

        with self._get_connection() as conn:
            cursor = conn.execute(
                f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})",
                values
            )
            conn.commit()
            return cursor.lastrowid

    def update(self, id_, **kwargs):
        now = self._get_now()
        kwargs['updated_at'] = now

        fields = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = tuple(kwargs.values()) + (id_,)

        with self._get_connection() as conn:
            cursor = conn.execute(
                f"UPDATE {self.table_name} SET {fields} WHERE id = ?",
                values
            )
            conn.commit()
            return cursor.rowcount

    def delete(self, id_):
        with self._get_connection() as conn:
            conn.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id_,))
            conn.commit()
