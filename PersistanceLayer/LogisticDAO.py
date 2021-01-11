import sqlite3


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _LogisticDAO(metaclass=Singleton):

    def __init__(self, conn):
        self._conn = conn

    def find(self, logistic_id):
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

    def update_received(self, logisticDTO):
        cur = self._conn.cursor()
        cur.execute("""UPDATE logistics SET count_received = (?) WHERE id = (?)""", (logisticDTO.count_received, logisticDTO.id))
        self._conn.commit()
    pass

    def update_sent(self, logisticDTO):
        cur = self._conn.cursor()
        cur.execute("""UPDATE logistics SET count_sent = (?) WHERE id = (?)""", (logisticDTO.count_sent, logisticDTO.id))
        self._conn.commit()
    pass