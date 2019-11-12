import random
import string
import time

from db import db
from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint


plans = Blueprint('plans', __name__)
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


@plans.route('/own_plans', methods=['GET', 'POST'])
def own_plans():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    plans = db.select(conn, 'plans', "*", {'aid': aid})
    return render_template("/plans/OwnPlans.html", plans = plans)


@plans.route('/adding_plan', methods=['GET', 'POST'])
def adding_plan():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    return render_template("/plans/AddingPlan.html")


@plans.route('/add_plans', methods=['GET', 'POST'])
def add_plans():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    plan = {'aid': aid, 'starting': request.form.get("starting"), 'ending': request.form.get("ending"),
            'cycle': request.form.get("cycle"), 'credit': request.form.get("budget"),
            'budget': request.form.get("budget")}
    pids = db.select(conn, 'plans', ['pid'], dict())
    pids = set([t['pid'] for t in pids])
    plan['pid'] = ''.join(random.choice(letters+numbers) for j in range(10))
    while plan['pid'] in pids:
        plan['pid'] = ''.join(random.choice(letters+numbers) for j in range(10))
    db.insert(conn, 'plans', plan)
    return redirect(url_for(".own_plans"))


@plans.route('/delete_plans', methods=['GET', 'POST'])
def delete_plans():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    db.delete(conn, 'plans', {'pid': request.form.get('pid')})
    return redirect(url_for(".own_plans"))
