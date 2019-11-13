

def condition_to_sql(condition):
    res = ["""%s = '%s'""" % (k, condition[k]) for k in condition]
    res = " AND ".join(res)
    return res


def columns_to_sql(columns):
    if columns == "*":
        return "*"
    res = ", ".join(columns)
    return res


def values_to_sql(values):
    vals = []
    for t in values:
        if t == "=":
            vals = ["%s = '%s'" % (k, values[t][k]) for k in values[t] if values[t][k] != ""]
        else:
            vals = ["%s = %s %s '%s'" % (k, k, t, values[t][k]) for k in values[t] if values[t][k] != ""]
    return ", ".join(vals)


def valid_honor(conn, aid):
    formed_aid = "'%s'" % (aid)
    sql = '''
    DELETE FROM win_honor WHERE aid=''' + formed_aid + ''';
    INSERT INTO win_honor (aid, hid)
    SELECT records.aid, honors.hid
    FROM records, honors 
    WHERE records.aid= ''' + formed_aid + \
    ''' AND (honors.starting IS NULL OR records.time >= honors.starting)
        AND (honors.ending IS NULL OR records.time <= honors.ending)
        AND (honors.tag IS NULL OR records.tag = honors.tag)
    GROUP BY honors.hid
    HAVING CASE WHEN honors.type = 'beq' THEN SUM(records.amt) >= honors.amt ELSE SUM(records.amt) <= honors.amt END; 
    '''
    print(sql)
    trans = conn.begin()
    try:
        conn.execute(sql)
        trans.commit()
    except:
        trans.rollback()
