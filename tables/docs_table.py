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
                "date": ["varchar(32)", "NOT NULL"]}

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
        cur.execute(f'SELECT docs FROM {self.table_name()} WHERE person_id = :id', {'id': int(pid)})
        result = cur.fetchall()
        # print(result)
        for i in result:
            # print(i, cd)
            if str(cd) == i[0]:
                return True
        return False

    def delete_docs_by_person(self, pid):
        cur = self.dbconn.conn.cursor()
        cur.execute(f'DELETE FROM {self.table_name()} WHERE person_id=:id', {'id': int(pid)})
        self.dbconn.conn.commit()
        return

    def delete_docs(self, cd):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE person_id=" + self.primary_key()[0]
        # print(sql)
        sql += " AND docs=:tell"
        # sql+= " IN DocsTable.docs"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"tell": str(cd)})
        # {"offset": num - 1}
        # print(sql)
        self.dbconn.conn.commit()
        return

    def update_docs(self, cd, new_cd):
        cur = self.dbconn.conn.cursor()
        cur.execute(f"UPDATE {self.table_name()} SET docs=:new_cd WHERE person_id={self.primary_key()[0]} AND docs=:cd", {'cd': str(cd), 'new_cd': str(new_cd)})
        print(self.primary_key())
        print(f"UPDATE {self.table_name()} SET docs=:cd WHERE person_id={self.primary_key()[0]} AND docs=:new_cd", {'cd': str(cd), 'new_cd': str(new_cd)})
        self.dbconn.conn.commit()
        return

