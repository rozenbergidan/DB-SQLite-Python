import sqlite3


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _VaccineDAO(metaclass=Singleton):
    def __init__(self, conn):
        self._conn = conn


    def find(self, vaccine_id):
        cur = self._conn.cursor()
        cur.execute("""SELECT * FROM vaccines where id = ? """, (int(vaccine_id)))
        return list(cur.fetchone())

    def insert(self, vaccineDTO):
        try:
            cur = self._conn.cursor()
            cur.execute("""INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)""", (vaccineDTO.id, vaccineDTO.date, vaccineDTO.supplier, vaccineDTO.quantity))
            self._conn.commit()
        except sqlite3.Error:
            print("error in vaccines")
    pass

    def update(self, vaccineDTO):
        cur = self._conn.cursor()
        cur.execute("""UPDATE vaccines SET quantity = (?) WHERE id = (?)""",
                    (vaccineDTO.quantity, vaccineDTO.id))
        self._conn.commit()
    pass

    def delete(self, vaccineDTO):
        cur = self._conn.cursor()
        cur.execute("""DELETE FROM vaccines WHERE id = (?)""",(vaccineDTO.id))
        self._conn.commit()
    pass