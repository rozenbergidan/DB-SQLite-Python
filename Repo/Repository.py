import sqlite3
from PersistanceLayer.ClinicDAO import _ClinicDAO
from PersistanceLayer.LogisticDAO import _LogisticDAO
from PersistanceLayer.SupplierDAO import _SupplierDAO
from PersistanceLayer.Vaccines import _Vaccines


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect(".\\database.db")
        self.clean()
        self.create_tables()
        self.get_config_file("config.txt")

    def clean(self):
        cur = self._conn.cursor()
        cur.execute("""DROP TABLE vaccines;""")
        cur.execute("""DROP TABLE suppliers;""")
        cur.execute("""DROP TABLE clinics;""")
        cur.execute("""DROP TABLE logistics;""")

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
        self._conn.commit()

        pass

    def get_config_file(self, config_file_path):
        cur = self._conn.cursor()
        with open(".\\"+config_file_path, "r",encoding ="utf-8") as configFile:
            rows = configFile.read().split("\n")
            data = rows[0].split(",")

            vaccines = (1, int(data[0]))
            suppliers = (1+vaccines[1], vaccines[1]+int(data[1]))
            clinics = (1+suppliers[1],  suppliers[1]+int(data[2]))
            logistics = (1+clinics[1], clinics[1]+int(data[3]))

            # print(vaccines)
            # print(suppliers)
            # print(clinics)
            # print(logistics)



            for line in rows[logistics[0]:1+logistics[1]]:
                logDao = _LogisticDAO(self._conn)
                logDao.insert(line.split(","))

            for line in rows[clinics[0]:1+clinics[1]]:
                clinDao = _ClinicDAO(self._conn)
                clinDao.insert(line.split(","))

            for line in rows[suppliers[0]:1+suppliers[1]]:
                supDao = _SupplierDAO(self._conn)
                supDao.insert(line.split(","))
            for line in rows[vaccines[0]:1+vaccines[1]]:
                vacDao = _Vaccines(self._conn)
                vacDao.insert(line.split(","))

            pass












