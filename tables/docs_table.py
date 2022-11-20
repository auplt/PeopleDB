from dbtable import *


class DocsTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "docs"

    def columns(self):
        return {"person_id": ["integer", "REFERENCES people(id)"],
                "type": ["varchar(32)", "NOT NULL"],
                "series": ["varchar(32)", "NOT NULL"],
                "number": ["varchar(32)", "NOT NULL"],
                "department": ["varchar(64)", "NOT NULL"],
                "issue_date": ["varchar(11)", "NOT NULL"]}

    def primary_key(self):
        return ['person_id', 'type', 'series', 'number', 'department', 'issue_date']

    def table_constraints(self):
        return ["PRIMARY KEY(person_id, type, series, number, department, issue_date)"]

    def all_by_person_id(self, pid):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE person_id = :id"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        print(sql)
        cur = self.dbconn.conn.cursor()
        # cur.execute(sql, str(pid))
        print(cur.execute("SELECT * FROM prj_docs WHERE person_id=:id", {'id': int(2)}))
        return cur.fetchall()