from sqlalchemy import create_engine

from db.utils import condition_to_sql, columns_to_sql, values_to_sql


def connect(name, usr, host, pwd):
    try:
        conn = create_engine("postgres://%s:%s@%s/%s" % (usr, pwd, host, name)).connect()
        return conn
    except:
        print("fail to build connection")
        return None


def select(conn, table, columns, condition, special = ""):
    cond_sql = condition_to_sql(condition)
    if cond_sql == "":
        sql = """SELECT %s FROM %s %s;""" % (
            columns_to_sql(columns), table, special)
    else:
        sql = """SELECT %s FROM %s WHERE %s %s;""" % (columns_to_sql(columns), table, cond_sql, special)
    print(sql)
    trans = conn.begin()
    try:
        cur = conn.execute(sql)
        trans.commit()
        tmp = cur.fetchall()
        res = []
        for row in tmp:
            tmp_row = dict()
            for col in row._keymap.keys():
                tmp_row[col] = row[col]
            res.append(tmp_row)
        return res
    except:
        trans.rollback()
        return None


def insert(conn, table, data):

    cols = ",".join([t for t in data.keys() if data[t] != ""])
    cols = "(%s)" % cols
    vals = ["""'%s'""" % t for t in data.values() if t != ""]
    vals = ", ".join(vals)
    vals = "(%s)" % vals

    sql = "INSERT INTO %s %s VALUES %s;" % (table, cols, vals)
    print(sql)
    trans = conn.begin()
    try:
        conn.execute(sql)
        trans.commit()
        return True
    except:
        trans.rollback()
        return False


def delete(conn, table, condition):

    sql = "DELETE FROM %s WHERE %s;" % (table, condition_to_sql(condition))
    print(sql)
    trans = conn.begin()
    try:
        conn.execute(sql)
        trans.commit()
        return True
    except:
        trans.rollback()
        return False


def update(conn, table, new_values, condition):
    vals = values_to_sql(new_values)
    sql = "UPDATE %s SET %s WHERE %s;" % (table, vals, condition_to_sql(condition))
    print(sql)
    trans = conn.begin()
    try:
        conn.execute(sql)
        trans.commit()
        return True
    except:
        trans.rollback()
        return False


def special_select(sql):
    print(sql)
    trans = conn.begin()
    try:
        cur = conn.execute(sql)
        trans.commit()
        tmp = cur.fetchall()
        res = []
        for row in tmp:
            tmp_row = dict()
            for col in row._keymap.keys():
                tmp_row[col] = row[col]
            res.append(tmp_row)
        return res
    except:
        trans.rollback()
        return None


conn = connect(name = "proj1part2", usr = "yl4323", host = "35.243.220.243", pwd = "2262")
