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
        sql += ", ".join(self.primary_key())  # join string split by ', ', '[aa, bb, ss] ex.: aa, bb, ss
        sql += " LIMIT 1 OFFSET :offset"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()

    def find_by_id(self, num):
        cur = self.dbconn.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name()} WHERE id=:id", {'id': int(num)})
        return cur.fetchone()

    def delete(self, pid):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE id=:del"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"del": int(pid)})
        self.dbconn.conn.commit()
        return

    def update(self, pid, vals):
        vals = tuple(vals)
        cur = self.dbconn.conn.cursor()
        sql = "UPDATE " + self.table_name() + " SET last_name=:last_name, first_name=:first_name, second_name=:second_name WHERE id=:id"
        cur.execute(sql, {'last_name': str(vals[0]), 'first_name': str(vals[1]), 'second_name': str(vals[2]),
                          'id': int(pid)})
        self.dbconn.conn.commit()
        return

    def print_list(self, limit, offset):
        cur = self.dbconn.conn.cursor()
        cur.execute(
            f"SELECT * FROM {self.table_name()} ORDER BY {', '.join(self.primary_key())} LIMIT :limit OFFSET :offset",
            {"limit": limit, "offset": offset})
        return cur.fetchall()

    def count_check(self):
        cur = self.dbconn.conn.cursor()
        cur.execute(f"SELECT count(*) FROM {self.table_name()}")
        return cur.fetchone()
