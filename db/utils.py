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
