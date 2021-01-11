class ClinicDAO:
    def __init__(self, conn):
        self._conn= conn

    def get_clinic(self, clinic_id):
        cur = self._conn.cursor()
        cur.execute("""SELECT * FROM clinics where id = ? """,(int(clinic_id)))
        return list(cur.fetchone())

