def condition_to_sql(condition):
    res = []
    for t in condition:
        for k in condition[t]:
            res.append("%s.%s = '%s'" % (t, k, condition[t][k]))
    res = " AND ".join(res)
    return res


def tables_to_sql(tables):
    res = []
    i = 1
    for join_type in tables:
        tmp = []
        for table in tables[join_type]:
            tmp.append("%s as T%s" % (table, str(i)))
            i += 1
        tmp_s = " %s " % join_type
        res.append(tmp_s.join(tmp))
    res = ", ".join(res)
    return res


def columns_to_sql(columns):
    tmp = []
    if columns == "*":
        return "*"
    for t in columns:
        for col in columns[t]:
            tmp.append("%s.%s" % (t, col))
    res = ", ".join(tmp)
    return res
