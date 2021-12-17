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

    def get_exist(self, owner_id, mediaid) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            '''SELECT EXISTS
                    (SELECT
                        1
                    FROM
                        InstagramLogs
                    WHERE
                        OwnerId = ?
                        AND MediaId = ?
                    )''',
            (int(owner_id), int(mediaid)))
        return cursor.fetchone()

    def is_empty(self, owner_id) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            '''SELECT
                    COUNT(*)
                FROM
                    InstagramLogs
                WHERE
                    OwnerId = ?''',
            (int(owner_id),))
        return cursor.fetchone() == 0

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
