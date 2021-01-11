import sqlite3


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _SupplierDAO(metaclass=Singleton):
    def __init__(self, conn):
        self._conn = conn

    def find(self, supplier_id):
        cur = self._conn.cursor()
        cur.execute("""SELECT * FROM suppliers where id = ? """, (int(supplier_id)))
        return list(cur.fetchone())

    def insert(self, supplierDTO):
        try:
            cur = self._conn.cursor()
            cur.execute("""INSERT INTO suppliers (id, name, logistic) VALUES (?,?,?)""", (supplierDTO.id, supplierDTO.name, supplierDTO.logistic))
            self._conn.commit()
        except sqlite3.Error:
            print("error in supplier")
    pass