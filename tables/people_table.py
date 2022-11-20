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
        # print(sql)
        return cur.fetchone()

    def find_by_id(self, num):
        cur=self.dbconn.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name()} WHERE id=:id", {'id': int(num)})
        print(f"SELECT * FROM {self.table_name()} WHERE id=:id", {'id': int(num)})
        return cur.fetchone()

    def delete(self, pid):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE id=:del"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"del": int(pid)})
        # print(sql)
        self.dbconn.conn.commit()
        return

    def update(self,pid, vals):
        # vals=list(vals)
        # vals=vals.append(int(pid))
        vals = tuple(vals)
        # sql = "UPDATE " + self.table_name() + "("
        # sql += ", ".join(self.column_names_without_id()) + ") VALUES( "
        # sql += "?, " * len(vals)
        # sql = sql.removesuffix(', ')
        # sql += ')'
        print(vals, vals[0], vals[1], vals[2])
        # print(sql)

        # print(self.column_names_without_id())
        cur = self.dbconn.conn.cursor()
        sql = "UPDATE " + self.table_name() + " SET last_name=:last_name, first_name=:first_name, second_name=:second_name WHERE id=:id"
        print(sql)
        # cur.execute(sql)
        cur.execute(sql, {'last_name':str(vals[0]), 'first_name':str(vals[1]), 'second_name':str(vals[2]), 'id':int(pid)})
        # print(sql)
        self.dbconn.conn.commit()
        return

