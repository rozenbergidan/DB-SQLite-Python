import sqlite3


class _LogisticDAO:
    def __init__(self, conn):
        self._conn = conn

    def get_logistic(self, logistic_id):
        cur = self._conn.cursor()
        cur.execute("""SELECT * FROM logistics where id = ? """, (int(logistic_id)))
        return list(cur.fetchone())

    def insert(self, logisticDTO):
        try:
            cur = self._conn.cursor()
            cur.execute("""INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?,?,?,?)""", (logisticDTO.id, logisticDTO.name, logisticDTO.count_sent, logisticDTO.count_received))
            self._conn.commit()
        except sqlite3.Error:
            print("error in logistic")
    pass
