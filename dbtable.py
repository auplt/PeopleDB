from dbconnection import *


class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        return self.dbconn.prefix + "table"

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        return self.columns().keys()

    def primary_key(self):
        return ['id']

    def column_names_without_id(self):
        res = list(self.columns().keys())
        if 'id' in res:
            res.remove('id')
        return res

    def table_constraints(self):
        return []

    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name()
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def insert_one(self, vals):
        # print(self.column_names_without_id())
        # for i in range(0, len(vals)):
        #     if type(vals[i]) == str:
        #         vals[i] = "'" + vals[i] + "'"
        #     else:
        #         vals[i] = str(vals[i])
        # sql = "INSERT INTO " + self.table_name() + "("
        # sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        # sql += ", ".join(vals) + ")"
        # print(self.column_names_without_id())
        # print(vals)
        vals = tuple(vals)
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES( "
        sql += "?, " * len(vals)
        sql = sql.removesuffix(', ')
        sql += ')'

        # print(vals)
        vals = tuple(vals)
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES( "
        sql += "?, " * len(vals)
        sql = sql.removesuffix(', ')
        sql += ')'
        print(vals)
        print(sql)

        # print(self.column_names_without_id())
        cur = self.dbconn.conn.cursor()
        # cur.execute(sql)
        cur.execute(sql, vals)
        # print(sql)
        self.dbconn.conn.commit()
        return



    def first(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def last(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join([x + " DESC" for x in self.primary_key()])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def all(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        # print(sql)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()