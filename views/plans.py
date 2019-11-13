import random
import string
import time
import datetime

from db import db
from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint


plans = Blueprint('plans', __name__)
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


def find_current_period(start_time, cycle):
    days = {"week": 1, "month": 30, "quarter": 90, "half-year": 180, "year": 365}
    cur = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "%Y-%m-%d %H:%M:%S")
    d1 = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    interval = (cur - d1).days
    p = interval / days[cycle]

    begin = (d1 + datetime.timedelta(days = p * days[cycle])).strftime("%Y-%m-%d %H:%M:%S")
    end = (d1 + datetime.timedelta(days = (p + 1) * days[cycle])).strftime("%Y-%m-%d %H:%M:%S")
    return begin, end


def to_valid_time(dt):
    if dt is None or dt == "":
        return dt
    dt = dt.split("T")
    dt[1] += ":00"
    return " ".join(dt)


@plans.route('/own_plans', methods=['GET', 'POST'])
def own_plans():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    plans = db.select(conn, 'plans', "*", {'aid': aid})
    return render_template("/plans/OwnPlans.html", plans = plans)


@plans.route('/adding_plan', methods=['GET', 'POST'])
def adding_plan():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    return render_template("/plans/AddingPlan.html")


@plans.route('/add_plans', methods=['GET', 'POST'])
def add_plans():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    plan = {'aid': aid, 'starting': to_valid_time(request.form.get("starting")), 'ending': to_valid_time(request.form.get("ending")),
            'cycle': request.form.get("cycle"), 'budget': request.form.get("budget")}
    pids = db.select(conn, 'plans', ['pid'], dict())
    pids = set([t['pid'] for t in pids])
    plan['pid'] = ''.join(random.choice(letters+numbers) for j in range(10))
    while plan['pid'] in pids:
        plan['pid'] = ''.join(random.choice(letters+numbers) for j in range(10))

    begin, end = find_current_period(plan['starting'], plan['cycle'])
    sql = """select SUM(amt) as total from records where aid = '%s' and time is not null and time >= '%s' and time <= '%s';""" % (aid, begin, end)
    existed_amt = db.special_select(sql)[0]['total']
    plan['credit'] = float(plan['budget']) - float(existed_amt)

    res = db.insert(conn, 'plans', plan)
    if res is True:
        return redirect(url_for(".own_plans"))
    else:
        return render_template("/plans/AddingPlan.html", msg = "illegal value")


@plans.route('/delete_plans', methods=['GET', 'POST'])
def delete_plans():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    db.delete(conn, 'plans', {'pid': request.form.get('pid')})
    return redirect(url_for(".own_plans"))


@plans.route('/modifing_plans', methods = ['GET', 'POST'])
def modifing_plans():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    pid = request.form.get("pid")
    plan = db.select(conn, "plans", "*", {'pid': pid})[0]
    return render_template("/plans/ModifyPlans.html", plan = plan)


@plans.route('/modify_plans', methods=['GET', 'POST'])
def modify_plans():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    plan = dict()
    pid = request.form.get("pid")
    plan['starting'] = to_valid_time(request.form.get("starting"))
    plan['ending'] = to_valid_time(request.form.get("ending"))
    plan['cycle'] = request.form.get("cycle")
    plan['budget'] = request.form.get("budget")

    old_budget = float(request.form.get("old_budget"))
    old_credit = float(request.form.get("old_credit"))
    plan['credit'] = float(plan['budget']) - (old_budget - old_credit)

    res = db.update(conn, 'plans', {"=": plan}, {'aid': aid})
    if res is False:
        plan = db.select(conn, "plans", "*", {'pid': pid})
        return render_template("/plans/ModifyPlans.html", plan = plan, msg = "illegal value")
    else:
        return redirect(url_for(".own_plans"))
