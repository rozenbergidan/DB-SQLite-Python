import sqlite3


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect(".\\database.db")

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS clinics (
                    id  INTEGER  PRIMARY KEY,
                    location STRING NOT NULL,
                    demand INTEGER  NOT NULL,
                    logistic INTEGER  REFERENCES logistics(id)
                );
            CREATE TABLE IF NOT EXISTS logistics(
                    id INTEGER PRIMARY KEY,
                    name STRING NOT NULL,
                    count_sent INTEGER NOT NULL,
                    count_received INTEGER NOT NULL
                );
            CREATE TABLE IF NOT EXISTS suppliers (
                    id      INTEGER     PRIMARY KEY,
                    name    STRING      NOT NULL,
                    logistic INTEGER REFERENCES logistics(id)
                );
            CREATE TABLE IF NOT EXISTS vaccines (
                    id      INTEGER   PRIMARY KEY,
                    date    DATE      NOT NULL,
                    supplier INTEGER REFERENCES suppliers(id),
                    quantity INTEGER  NOT NULL
                );
            """)
        pass

    def get_config_file(self, conn, config_file_path):


