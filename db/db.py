import psycopg2
from psycopg2.extras import RealDictCursor

from db.utils import condition_to_sql, columns_to_sql, values_to_sql


def connect(name, usr, host, pwd):
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (name, usr, host, pwd))
        return conn
    except:
        print("fail to build connection")
        return None


def select(conn, table, columns, condition, special = ""):
    cur = conn.cursor(cursor_factory = RealDictCursor)

    cond_sql = condition_to_sql(condition)
    if cond_sql == "":
        sql = """SELECT %s FROM %s %s;""" % (
            columns_to_sql(columns), table, special)
    else:
        sql = """SELECT %s FROM %s WHERE %s %s;""" % (columns_to_sql(columns), table, cond_sql, special)
    print(sql)
    cur.execute(sql)
    return cur.fetchall()


def insert(conn, table, data):
    cur = conn.cursor(cursor_factory = RealDictCursor)

    cols = ",".join([t for t in data.keys() if data[t] != ""])
    cols = "(%s)" % cols
    vals = ["""'%s'""" % t for t in data.values() if t != ""]
    vals = ", ".join(vals)
    vals = "(%s)" % vals

    sql = "INSERT INTO %s %s VALUES %s;" % (table, cols, vals)
    print(sql)
    cur.execute(sql)
    conn.commit()


def delete(conn, table, condition):
    cur = conn.cursor(cursor_factory = RealDictCursor)

    sql = "DELETE FROM %s WHERE %s;" % (table, condition_to_sql(condition))
    print(sql)
    cur.execute(sql)
    conn.commit()


def update(conn, table, new_values, condition):
    cur = conn.cursor(cursor_factory = RealDictCursor)

    vals = values_to_sql(new_values)
    sql = "UPDATE %s SET %s WHERE %s;" % (table, vals, condition_to_sql(condition))
    print(sql)
    cur.execute(sql)
    conn.commit()


def special_select(sql):
    cur = conn.cursor(cursor_factory = RealDictCursor)
    cur.execute(sql)
    return cur.fetchall()


conn = connect(name = "proj1part2", usr = "yl4323", host = "35.243.220.243", pwd = "2262")
