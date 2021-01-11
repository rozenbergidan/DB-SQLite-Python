import sqlite3

class _Vaccines:
    def __init__(self, conn):
        self._conn = conn


    def insert(self, args):
        # try:
            print(args)
            cur = self._conn.cursor()
            cur.execute("""INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)""",
                        (str(args[0]), str(args[1]), str(args[2]), str(args[3])))
            self._conn.commit()
        # except sqlite3.Error:
        #     print("error in vaccines")
    pass