import sqlite3


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _ClinicDAO(metaclass=Singleton):

    def __init__(self, conn):
        self._conn = conn

    def find(self, clinic_id):
        cur = self._conn.cursor()
        cur.execute("""SELECT * FROM clinics where id = ? """, (int(clinic_id)))
        return list(cur.fetchone())

    def insert(self, clinicDTO):
        try:
            cur = self._conn.cursor()
            cur.execute("""INSERT INTO clinics (id, location, demand, logistic) VALUES (?,?,?,?)""", (clinicDTO.id, clinicDTO.location, clinicDTO.demand, clinicDTO.logistic))
            self._conn.commit()
        except sqlite3.Error:
            print("error in clinic")
    pass

    def update(self, clinicDTO):
        cur = self._conn.cursor()
        cur.execute("""UPDATE clinics SET demand = (?) WHERE id = (?)""",
                    (clinicDTO.demand, clinicDTO.id))
        self._conn.commit()



