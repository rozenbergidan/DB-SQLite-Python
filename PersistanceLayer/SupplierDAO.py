import sqlite3


class _SupplierDAO:
    def __init__(self, conn):
        self._conn = conn

    def get_supplier(self, supplier_id):
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