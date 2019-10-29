import psycopg2


def connect(name, usr, host, pwd):
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (name, usr, host, pwd))
        return conn, conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    except:
        print("fail to build connection")
        return None, None



def select(cur, table, condition):
    sql = """select * from %s where %s""" % (table, condition)
    cur.execute(sql)
    return cur.fetchall()

