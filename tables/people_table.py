from dbtable import *


class PeopleTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "people"

    def columns(self):
        return {"id": ["integer", "PRIMARY KEY", "AUTOINCREMENT"],
                "last_name": ["varchar(32)", "NOT NULL"],
                "first_name": ["varchar(32)", "NOT NULL"],
                "second_name": ["varchar(32)"]}

    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())  # join элементов в [] через ', ' ex.: aa, bb, ss
        sql += " LIMIT 1 OFFSET :offset"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        # print(sql)
        return cur.fetchone()

    def delete(self, pid):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE id=:del"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"del": pid})
        # print(sql)
        self.dbconn.conn.commit()
        return
