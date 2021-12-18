import os
import sqlite3
from pathlib import Path


class DB:
    db_path = os.path.join(
        Path(__file__).parent.parent.resolve(), 'db', 'InstagramLogs.sqlite')

    @staticmethod
    def init_db():
        Path(DB.db_path).parent.mkdir(
            parents=True, exist_ok=True)
        conn = sqlite3.connect(DB.db_path)
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS   InstagramLogs
                (OwnerId       UNSIGNED BIG INT     NOT NULL,
                MediaId        UNSIGNED BIG INT     NOT NULL);'''
        )
        conn.commit()
        conn.close()

    def __init__(self, readonly=True):
        self.conn = sqlite3.connect(
            "file://%s%s" % (DB.db_path, "?mode=ro" if readonly else ""), uri=True
        )

    def __enter__(self):
        return self

    def insert(self, owner_id, mediaid):
        self.conn.execute(
            '''INSERT INTO InstagramLogs
                    (OwnerId, MediaId)
                VALUES
                    (?, ?)''',
            (int(owner_id), int(mediaid)))
        self.conn.commit()

    def get_exist(self, owner_id, mediaid=None) -> bool:
        cursor = self.conn.cursor()
        sql = '''SELECT EXISTS
                    (SELECT
                        1
                    FROM
                        InstagramLogs
                    WHERE
                        OwnerId = ?
            '''

        if mediaid:
            sql += ' AND MediaId = ? '
            sql += ' );'
            cursor.execute(
                sql,
                (int(owner_id), int(mediaid)))
        else:
            sql += ' );'
            cursor.execute(
                sql,
                (int(owner_id),))

        result = cursor.fetchone()
        return result[0]

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
