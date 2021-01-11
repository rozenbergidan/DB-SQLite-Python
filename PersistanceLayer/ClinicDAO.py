import sqlite3


class _ClinicDAO:
    def __init__(self, conn):
        self._conn = conn

    def get_clinic(self, clinic_id):
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




