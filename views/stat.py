import time

from db import db
from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint


stat = Blueprint('stat', __name__)


def to_valid_form(data, daily = True):
    t = time.strftime("%Y-%m-%d", time.localtime()).split("-")
    month = int(t[1])
    day = int(t[2])

    t_set = set([int(t['x']) for t in data])
    t_dict = dict()
    for item in data:
        t_dict[int(item['x'])] = item['y']

    res = []
    if daily is True:
        upbound = day + 1
    else:
        upbound = month + 1
    for i in range(1, upbound):
        if i in t_set:
            res.append({'x': i, 'y': t_dict[i]})
        else:
            res.append({'x': i, 'y': 0})
    return res


def predict_total_amt(data, daily = True):
    res = 0
    for item in data:
        res += float(item['y'])
    res /= len(data)
    t = time.strftime("%Y-%m-%d", time.localtime()).split("-")
    month = t[1]
    if daily:
        month_day = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31}
        nxt_t = (int(data[-1]['x']) + 1) % month_day[month]
        if nxt_t == 0:
            nxt_t = month_day[str(int(data[-1]['x']))]
    else:
        nxt_t = (int(data[-1]['x']) + 1) % 12
        if nxt_t == 0:
            nxt_t = 12
    nxt = {'x': str(nxt_t) + "(predicted)", 'y': res}
    return nxt


@stat.route('/statistic', methods=['GET', 'POST'])
def statistic():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    t = time.strftime("%Y-%m-%d", time.localtime()).split("-")
    year = t[0]
    month = t[1]
    day = t[2]
    data = dict()
    sql = """select tag as x, COUNT(tag) as y from records where aid = '%s' group by tag;""" % aid
    data['tag_num'] = db.special_select(sql)

    sql = """select be_from as x, COUNT(be_from) as y from records where aid = '%s' group by be_from;""" % aid
    data['source_num'] = db.special_select(sql)

    sql = """select be_to as x, COUNT(be_to) as y from records where aid = '%s' group by be_to;""" % aid
    data['receiver_num'] = db.special_select(sql)

    sql = """select date_part('day', time) as x, SUM(amt) as y from records where aid = '%s' and date_part('day', time) is not null and date_part('month', time) = '%s' and date_part('day', time) <= '%s' group by date_part('day', time) order by x;""" % (aid, month, day)
    data['amt_daily'] = to_valid_form(db.special_select(sql), daily = True)
    data['amt_daily'].append(predict_total_amt(data['amt_daily'], daily = True))

    sql = """select date_part('month', time) as x, SUM(amt) as y from records where aid = '%s' and date_part('month', time) is not null and date_part('year', time) = '%s' and date_part('month', time) <= '%s' group by date_part('month', time) order by x;""" % (aid, year, month)
    data['amt_monthly'] = to_valid_form(db.special_select(sql), daily = False)
    data['amt_monthly'].append(predict_total_amt(data['amt_monthly'], daily = False))

    return render_template("/stat/Statistic.html", data = data)
