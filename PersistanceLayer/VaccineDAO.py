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


    def insert(self, vaccineDTO):
        try:
            cur = self._conn.cursor()
            cur.execute("""INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)""", (vaccineDTO.id, vaccineDTO.date, vaccineDTO.supplier, vaccineDTO.quantity))
            self._conn.commit()
        except sqlite3.Error:
            print("error in vaccines")
    pass