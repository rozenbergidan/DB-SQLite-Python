import sqlite3
from PersistanceLayer.ClinicDAO import _ClinicDAO
from PersistanceLayer.LogisticDAO import _LogisticDAO
from PersistanceLayer.SupplierDAO import _SupplierDAO
from PersistanceLayer.VaccineDAO import _VaccineDAO
from ApplicationLayer.LogisticDTO import LogisticDTO
from ApplicationLayer.ClinicDTO import ClinicDTO
from ApplicationLayer.SupplierDTO import SupplierDTO
from ApplicationLayer.VaccineDTO import VaccineDTO


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _Repository(metaclass=Singleton):
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.clean()
        self.create_tables()

    def clean(self):
        cur = self._conn.cursor()
        cur.execute("""DROP TABLE IF EXISTS vaccines;""")
        cur.execute("""DROP TABLE IF EXISTS suppliers;""")
        cur.execute("""DROP TABLE IF EXISTS clinics;""")
        cur.execute("""DROP TABLE IF EXISTS logistics;""")

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS clinics (
                    id  INTEGER AUTO_INCREMENT PRIMARY KEY,
                    location STRING NOT NULL ,
                    demand INTEGER  NOT NULL,
                    logistic INTEGER  REFERENCES logistics(id)
                );
            CREATE TABLE IF NOT EXISTS logistics(
                    id INTEGER AUTO_INCREMENT PRIMARY KEY,
                    name STRING NOT NULL,
                    count_sent INTEGER NOT NULL,
                    count_received INTEGER NOT NULL
                );
            CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER AUTO_INCREMENT PRIMARY KEY,
                    name STRING NOT NULL,
                    logistic INTEGER REFERENCES logistics(id)
                );
            CREATE TABLE IF NOT EXISTS vaccines (
                    id      INTEGER AUTO_INCREMENT PRIMARY KEY,
                    date    DATE NOT NULL,
                    supplier INTEGER REFERENCES suppliers(id),
                    quantity INTEGER NOT NULL
                );
            """)
        self._conn.commit()
        pass

    def dates_sorted(self):
        cur=self._conn.cursor()
        cur.execute("""SELECT id FROM vaccines ORDER BY date ASC""")
        out = list(cur.fetchall())
        return out

    def get_config_file(self, config_file_path, vaccines1, suppliers1, clinics1, logistics1):
        with open(config_file_path, "r", encoding ="utf-8") as configFile:
            rows = configFile.read().split("\n")
            data = rows[0].split(",")

            vaccines = (1, int(data[0]))
            suppliers = (1+vaccines[1], vaccines[1]+int(data[1]))
            clinics = (1+suppliers[1],  suppliers[1]+int(data[2]))
            logistics = (1+clinics[1], clinics[1]+int(data[3]))


            for line in rows[logistics[0]:1+logistics[1]]:
                data = line.split(",")
                log = LogisticDTO(data[0],data[1],data[2],data[3])
                logistics1[log.id]=log
                logDao = _LogisticDAO(self._conn)
                logDao.insert(log)

            for line in rows[clinics[0]:1+clinics[1]]:
                data = line.split(",")
                clnc = ClinicDTO(data[0], data[1], data[2], data[3])
                clinics1[clnc.id]=clnc
                clinDao = _ClinicDAO(self._conn)
                clinDao.insert(clnc)

            for line in rows[suppliers[0]:1+suppliers[1]]:
                data = line.split(",")
                sup = SupplierDTO(data[0], data[1], data[2])
                suppliers1[sup.id]=sup
                supDao = _SupplierDAO(self._conn)
                supDao.insert(sup)

            for line in rows[vaccines[0]:1+vaccines[1]]:
                data = line.split(",")
                # TODO: i changed here
                jibrish = data[1]
                jibrish = jibrish.replace("גˆ’", "-")
                data[1]=jibrish
                vcn = VaccineDTO(data[0], data[1], data[2], data[3])
                vaccines1[vcn.id]=vcn
                vacDao = _VaccineDAO(self._conn)
                vacDao.insert(vcn)

            pass

    def load_project(self, Session, config):
        self.get_config_file(config, Session.Vaccines, Session.Suppliers, Session.Clinics, Session.Logistics)
        pass

    def total_vaccines(self):
        cur = self._conn.cursor()
        cur.execute("""SELECT sum(quantity) FROM vaccines """)
        out = cur.fetchall()
        return out

    def total_demand(self):
        cur = self._conn.cursor()
        cur.execute("""SELECT sum(demand) FROM clinics""")
        out = cur.fetchall()
        return out

    def total_received(self):
        cur = self._conn.cursor()
        cur.execute("""SELECT sum(count_received) FROM logistics""")
        out = cur.fetchall()
        return out

    def total_sent(self):
        cur = self._conn.cursor()
        cur.execute("""SELECT sum(count_sent) FROM logistics""")
        out = cur.fetchall()
        return out






