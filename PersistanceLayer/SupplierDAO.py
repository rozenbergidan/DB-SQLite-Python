import sqlite3


class _SupplierDAO:
    def __init__(self, conn):
        self._conn = conn

    def get_supplier(self, supplier_id):
        cur = self._conn.cursor()
        cur.execute("""SELECT * FROM suppliers where id = ? """, (int(supplier_id)))
        return list(cur.fetchone())

    def insert(self, args):
        # try:
            print(args)
            cur = self._conn.cursor()
            cur.execute("""INSERT INTO suppliers (id, name, logistic) VALUES (?,?,?)""", (str(args[0]), str(args[1]), str(args[2])))
            self._conn.commit()
        # except sqlite3.Error:
        #     print("error in supplier")
    pass