import sqlite3

class _VaccineDAO:
    def __init__(self, conn):
        self._conn = conn


    def insert(self, vaccineDTO):
        try:
            cur = self._conn.cursor()
            cur.execute("""INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)""", (vaccineDTO.id, vaccineDTO.date, vaccineDTO.supplier, vaccineDTO.quantity))
            self._conn.commit()
        except sqlite3.Error:
            print("error in vaccines")
    pass