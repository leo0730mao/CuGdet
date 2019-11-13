

class BaseEntity(object):
    table = "base"
    @classmethod
    def select(cls, conn, condition):
        sql = """SELECT * FROM %s WHERE %s;""" % (cls.table, condition)
        cur = conn.execute(sql)
        res = cur.fetchall()
        return res


    @classmethod
    def insert(cls, conn, value):
        sql = """INSERT INTO  VALUE();"""
        conn.execute(sql)
        conn.commit()

    @classmethod
    def delete(cls, conn, condition):
        sql = """DELETE * FROM %s WHERE %s;""" % (cls.table, condition)
        conn.execute(sql)
        conn.commit()

    @classmethod
    def update(cls):
        print(cls.table)
