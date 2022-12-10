from dbtable import *


class PhonesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "phones"

    def columns(self):
        return {"person_id": ["integer", "REFERENCES people(id)"],
                "phone": ["varchar(12)", "NOT NULL"]}

    def primary_key(self):
        return ['person_id', 'phone']

    def table_constraints(self):
        return ["PRIMARY KEY(person_id, phone)"]

    def all_by_person_id(self, pid):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE person_id =:id"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"id": str(pid)})
        return cur.fetchall()

    def check_number(self, pid, tel):
        cur = self.dbconn.conn.cursor()
        cur.execute(f'SELECT phone FROM {self.table_name()} WHERE person_id =:id', {'id': int(pid)})
        result = cur.fetchall()
        for i in result:
            if str(tel) == i[0]:
                return True
        return False

    def delete_phones_by_person(self, pid):
        cur = self.dbconn.conn.cursor()
        cur.execute(f'DELETE FROM {self.table_name()} WHERE person_id =:id', {'id': int(pid)})
        self.dbconn.conn.commit()
        return

    def delete_phone(self, tel):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE person_id=" + self.primary_key()[0]
        sql += " AND phone=:tell"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"tell": str(tel)})
        self.dbconn.conn.commit()
        return

    def update_phone(self, tel, new_tel):
        cur = self.dbconn.conn.cursor()
        cur.execute(
            f"UPDATE {self.table_name()} SET phone=:new_tel WHERE person_id={self.primary_key()[0]} AND phone=:tel",
            {'tel': str(tel), 'new_tel': str(new_tel)})
        self.dbconn.conn.commit()
        return
