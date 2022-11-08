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
        sql += " WHERE person_id = :id"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"id": str(pid)})
        return cur.fetchall()

    # def find_by_(self, tel):
    #     sql = "DELETE FROM " + self.table_name()
    #     sql+= " WHERE id=" + self.primary_key()[1] + ", phone=:tel"
    #     cur = self.dbconn.conn.cursor()
    #     cur.execute(sql, {"tel":tel})
    #     # print(sql)
    #     return cur.fetch

    def check_number(self, pid, tel):
        cur = self.dbconn.conn.cursor()
        cur.execute(f'SELECT phone FROM {self.table_name()} WHERE person_id = :id', {'id': int(pid)})
        result = cur.fetchall()
        print(result)
        for i in result:
            # print(i, tel)
            if str(tel) == i[0]:
                return True
        return False

    def delete_phones_by_person(self, pid):
        cur = self.dbconn.conn.cursor()
        cur.execute(f'DELETE FROM {self.table_name()} WHERE person_id=:id', {'id': int(pid)})
        self.dbconn.conn.commit()
        return

    def delete_phone(self, tel):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE person_id=" + self.primary_key()[0]
        print(sql)
        sql += " AND phone=:tell"
        # sql+= " IN PhonesTable.phone"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"tell": str(tel)})
        # {"offset": num - 1}
        print(sql)
        self.dbconn.conn.commit()
        return
