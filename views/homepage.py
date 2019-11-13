import random
import string
import time
from datetime import datetime
from flask import request, redirect, session, url_for, render_template, Blueprint

from db.db import conn
from db import db
from db.utils import *


def check_time(start_time, t, cycle):
    days = {"week": 1, "month": 30, "quarter": 90, "half-year": 180, "year": 365}
    start_time = start_time.split(" ")[0]
    d1 = datetime.strptime(start_time, '%Y-%m-%d')
    d2 = datetime.strptime(t, '%Y-%m-%d')
    d3 = datetime.strptime(time.strftime("%Y-%m-%d", time.localtime()), '%Y-%m-%d')
    interval1 = (d2 - d1).days
    interval2 = (d3 - d1).days
    if interval1 / days[cycle] == interval2 / days[cycle]:
        return True
    else:
        return False


homepage = Blueprint('homepage', __name__)
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


def to_valid_time(dt):
    if dt is None or dt == "":
        return dt
    dt = dt.split("T")
    dt[1] += ":00"
    return " ".join(dt)


@homepage.route('/all_records', methods=['GET', 'POST'])
def all_records():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    records = db.select(conn, 'records', "*", {'aid': aid}, special = "ORDER BY time DESC")
    return render_template("/homepage/HomePage.html", records = records)


@homepage.route('/adding_record', methods=['GET', 'POST'])
def adding_record():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    return render_template("/homepage/AddingRecord.html")


@homepage.route('/add_record', methods=['GET', 'POST'])
def add_record():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    record = dict()
    record['name'] = request.form.get("name")
    record['be_from'] = request.form.get("be_from")
    record['be_to'] = request.form.get("be_to")
    record['amt'] = request.form.get("amt")
    record['tag'] = request.form.get("tag")
    record['time'] = to_valid_time(request.form.get("time"))
    record['remark'] = request.form.get("remark")
    record['aid'] = request.cookies.get("aid")

    reids = db.select(conn, 'records', ['reid'], dict())
    reids = [t['reid'] for t in reids]

    record['reid'] = ''.join(random.choice(letters + numbers) for j in range(10))
    while record['reid'] in reids:
        record['reid'] = ''.join(random.choice(letters + numbers) for j in range(10))

    res = db.insert(conn, 'records', record)
    if res is True:
        # influence plans
        if record['time'] == "":
            record_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            record_time = record['time']
        sql = """select * from plans where aid = '%s' and (ending > '%s' or ending is null);""" % (aid, record_time)
        plans = db.special_select(sql)
        for plan in plans:
            if check_time(plan['starting'].strftime("%Y-%m-%d %H:%M:%S").split(" ")[0], record_time.split(" ")[0], plan['cycle']):
                new_credit = float(plan['credit']) + float(record['amt'])
                db.update(conn, "plans", {"=": {'credit': new_credit}}, {'pid': plan['pid']})

        # influence win_honor
        valid_honor(conn, aid)

        return redirect(url_for('homepage.all_records'))
    else:
        return render_template("/homepage/AddingRecord.html", msg = "illegal values")


@homepage.route('/delete_record', methods = ['GET', 'POST'])
def delete_record():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))

    old_amt = float(request.form.get('old_amt'))
    t = request.form.get('time')
    db.delete(conn, 'records', {'reid': request.form.get('reid')})

    # influence plans
    if t == "":
        record_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    else:
        record_time = t
    sql = """select * from plans where aid = '%s' and (ending > '%s' or ending is null);""" % (aid, record_time)
    plans = db.special_select(sql)
    for plan in plans:
        if check_time(plan['starting'].strftime("%Y-%m-%d %H:%M:%S").split(" ")[0], record_time.split(" ")[0], plan['cycle']):
            new_credit = float(plan['credit']) - old_amt
            db.update(conn, "plans", {"=": {'credit': new_credit}}, {'pid': plan['pid']})

    # influence win_honor
    valid_honor(conn, aid)

    return redirect(url_for(".all_records"))


@homepage.route('/modifing_record', methods = ['GET', 'POST'])
def modifing_record():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    reid = request.form.get("reid")
    record = db.select(conn, "records", "*", {'reid': reid})[0]
    return render_template("/homepage/ModifyRecord.html", record = record)


@homepage.route('/modify_record', methods=['GET', 'POST'])
def modify_record():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    record = dict()
    reid = request.form.get("reid")
    record['name'] = request.form.get("name")
    record['be_from'] = request.form.get("be_from")
    record['be_to'] = request.form.get("be_to")
    record['amt'] = request.form.get("amt")
    record['time'] = to_valid_time(request.form.get("time"))
    record['tag'] = request.form.get("tag")
    record['remark'] = request.form.get("remark")

    old_amt = float(request.form.get('old_amt'))
    old_time = request.form.get('old_time')
    res = db.update(conn, 'records', {"=": record}, {'aid': aid})
    if res is True:
        # influence plans
        if record['time'] == "":
            record_time = old_time
        else:
            record_time = record['time']
        sql = """select * from plans where aid = '%s' and (ending > '%s' or ending is null);""" % (aid, record_time)
        plans = db.special_select(sql)
        for plan in plans:
            if record['amt'] != "" and check_time(plan['starting'].strftime("%Y-%m-%d %H:%M:%S").split(" ")[0], record_time.split(" ")[0], plan['cycle']):
                new_credit = plan['credit'] - old_amt + float(record['amt'])
                db.update(conn, "plans", {"=": {'credit': new_credit}}, {'pid': plan['pid']})

        # influence win_honor
        valid_honor(conn, aid)

        return redirect(url_for(".all_records"))
    else:
        record = db.select(conn, "records", "*", {'reid': reid})[0]
        return render_template("/homepage/ModifyRecord.html", record = record, msg = "illegal value")
