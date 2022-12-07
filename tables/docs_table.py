from dbtable import *


class DocsTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "docs"

    def columns(self):
        return {"id": ["integer", "PRIMARY KEY", "AUTOINCREMENT"],
                "person_id": ["integer", "REFERENCES people(id)"],
                "type": ["varchar(32)", "NOT NULL"],
                "serial": ["varchar(32)", "NOT NULL"],
                "number": ["varchar(32)", "NOT NULL"],
                "date": ["varchar(10)", "NOT NULL"]}

    def all_by_person_id(self, pid):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE person_id = :id"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()

        cur.execute(sql, {"id": str(pid)})
        return cur.fetchall()

    def check_docs(self, pid, cd):
        cur = self.dbconn.conn.cursor()
        cur.execute(f'SELECT id FROM {self.table_name()} WHERE person_id = :id', {'id': int(pid)})
        # print("pid")
        # print(pid)
        result = cur.fetchall()
        # print("result")
        # print(result)
        # print("******")
        for i in result:
            # print("i, cd")
            # print(i, cd)
            # print("cd, i[0]")
            # print(cd, i[0])
            if str(cd) == str(i[0]):
                return True
        return False

    def delete_docs_by_person(self, pid):
        cur = self.dbconn.conn.cursor()
        cur.execute(f'DELETE FROM {self.table_name()} WHERE person_id=:id', {'id': int(pid)})
        self.dbconn.conn.commit()
        return

    def delete_docs(self, cd):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE id=" + self.primary_key()[0]
        # print(sql)
        sql += " AND id=:tell"
        # sql+= " IN DocsTable.docs"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"tell": str(cd)})
        # {"offset": num - 1}
        # print(sql)
        self.dbconn.conn.commit()
        return

    def update_docs(self, cd, new_serial):
        cur = self.dbconn.conn.cursor()
        cur.execute(f"UPDATE {self.table_name()} SET serial=:new_serial WHERE id={self.primary_key()[0]} AND id=:cd", {'cd': str(cd), 'new_serial': str(new_serial)})
        # print(cur.execute(f"UPDATE {self.table_name()} SET serial=:new_serial WHERE id={self.primary_key()[0]} AND id=:cd",{'cd': str(cd), 'new_serial': str(new_serial)}))
        # print(self.primary_key())
        # print(f"UPDATE {self.table_name()} SET id=:cd WHERE person_id={self.primary_key()[0]} AND id=:new_cd", {'cd': str(cd), 'new_cd': str(new_serial)})
        self.dbconn.conn.commit()
        return
    def find_by_id(self, num):
        cur=self.dbconn.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name()} WHERE id=:id", {'id': int(num)})
        # print(f"SELECT * FROM {self.table_name()} WHERE id=:id", {'id': int(num)})
        return cur.fetchone()
    def update_docs_2(self, pid, vals):
        # vals=list(vals)
        # vals=vals.append(int(pid))
        vals = tuple(vals)
        # sql = "UPDATE " + self.table_name() + "("
        # sql += ", ".join(self.column_names_without_id()) + ") VALUES( "
        # sql += "?, " * len(vals)
        # sql = sql.removesuffix(', ')
        # sql += ')'
        # print(vals, vals[0],vals[1],vals[2],vals[3])
        # print(sql)
        # print(self.column_names_without_id())
        cur = self.dbconn.conn.cursor()
        sql = "UPDATE " + self.table_name() + " SET type=:type, serial=:serial, number=:number, date=:date WHERE id=:id"
        # print(sql)
        # cur.execute(sql)
        cur.execute(sql, {'type':str(vals[0]),'serial':str(vals[1]), 'number':str(vals[2]), 'date':str(vals[3]), 'id':int(pid)})
        # print(sql)
        self.dbconn.conn.commit()
        # return


        # cur.execute(sql, str(pid))
        print(cur.execute("SELECT * FROM prj_docs WHERE person_id=:id", {'id': int(2)}))
        return cur.fetchall()

